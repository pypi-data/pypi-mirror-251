import time
import torch
from koi._runtime import lib, ffi
from koi.utils import void_ptr, quantize_tensor

T = 100
N = 2048
dtype = torch.float16
dev = "cuda"


def show_diff_result(label, ref_out, out_bfr, mean_limit, max_limit):
    diff = torch.abs(out_bfr.to(torch.float32) - ref_out.to(torch.float32))
    diff_mean = diff.mean().item()
    diff_max = diff.max().item()
    is_good = ("❌", "🟢")[diff_mean < mean_limit and diff_max < max_limit]
    print(
        f"Compare {label} to Torch ref: diff mean {diff_mean}, max {diff_max} {is_good}"
    )


def time_kernel(iters, stream, fn):
    for i in range(iters + 1):
        fn()
        if i == 0:
            stream.synchronize()
            t0 = time.time()
    stream.synchronize()
    return time.time() - t0


def test_lstms():
    with torch.no_grad():
        stream = torch.cuda.default_stream()
        stream_ptr = ffi.cast("void *", stream.cuda_stream)

        for C in [96, 128, 256, 384, 512, 768, 1024]:
            print(f"Running LSTM TNC {T}x{N}x{C}, dtype {dtype}")
            torch.cuda.empty_cache()
            tflop = (C * C * 8 * T * N * 2) / 1.0e12
            torch.manual_seed(42)
            in_bfr = torch.rand((T, N, C), device=dev, dtype=dtype) * 2 - 1

            ref_lstm = torch.nn.LSTM(C, C, device=dev, dtype=dtype)
            ref_out = ref_lstm.forward(in_bfr)[0]
            bias = ref_lstm.bias_ih_l0 + ref_lstm.bias_hh_l0
            weights = torch.concat((ref_lstm.weight_ih_l0.T, ref_lstm.weight_hh_l0.T), 0)

            #################################################################################
            ## LstmStep test
            #################################################################################
            in_out_bfr = torch.zeros((T + 1, N, 2, C), device=dev, dtype=dtype)
            in_out_bfr[:T, :, 0] = in_bfr
            out_bfr = in_out_bfr[1:, :, 1]
            state_buf = torch.zeros((N, C), device=dev, dtype=dtype)
            for t in range(T):
                gate_buf = torch.matmul(in_out_bfr[t].view((N, 2 * C)), weights)
                lib.host_lstm_step_f16(
                    stream_ptr,
                    N,
                    C,
                    void_ptr(bias),
                    void_ptr(gate_buf),
                    void_ptr(state_buf),
                    void_ptr(out_bfr[t]),
                )
            stream.synchronize()
            show_diff_result("LSTM step kernel", ref_out, out_bfr, 1e-4, 2e-3)

            #################################################################################
            ##  hma2/dp4a Kernel test
            #################################################################################
            if C in [96, 128]:
                weight_ih = ref_lstm.weight_ih_l0.T
                weight_hh = ref_lstm.weight_hh_l0.T.contiguous()
                q_scale, weight_hh_q = quantize_tensor(weight_hh)

                in_bfr_ntc = in_bfr.transpose(0, 1).contiguous()
                out_bfr_ntc = torch.empty_like(in_bfr_ntc)
                in_Wx = torch.matmul(in_bfr_ntc.view((-1, C)), weight_ih)
                in_Wx_rev = in_Wx.view((N, T, -1)).flip(1)
                iters = 100
                if C == 96:
                    tests = [
                        (False, 1),
                        (False, -1),
                        (True, 1),
                        (True, -1),
                    ]  # [HMA2|DP4A] x [fwd|rev]
                else:
                    tests = [(True, 1), (True, -1)]  # Test only DP4A fwd/rev for 128-wide
                for quantised, direction in tests:
                    t = time_kernel(
                        iters,
                        stream,
                        lambda: lib.host_small_lstm(
                            N,
                            T,
                            C,
                            direction,
                            void_ptr(in_Wx if direction == 1 else in_Wx_rev),
                            void_ptr(weight_hh_q if quantised else weight_hh),
                            void_ptr(bias),
                            void_ptr(q_scale) if quantised else ffi.cast("void *", 0),
                            void_ptr(out_bfr_ntc),
                        ),
                    )
                    out_bfr = out_bfr_ntc.transpose(0, 1)
                    if direction == -1:
                        out_bfr = out_bfr.flip(0)
                    dir_str = "fwd" if direction == 1 else "rev"
                    kernel_str = "DP4A" if quantised else "HMA2"
                    show_diff_result(
                        f"{kernel_str} Kernel {dir_str} {tflop * iters / t:.3f} Tflops",
                        ref_out,
                        out_bfr,
                        8e-4 if quantised else 2e-4,
                        9e-3 if quantised else 3e-3,
                    )

            #################################################################################
            ## Cutlass test
            #################################################################################
            props = torch.cuda.get_device_properties(dev)
            if props.major in (8, 9) and props.minor == 0 and (C % 64) == 0 and C > 128:
                state_buf = torch.empty((N, C), device=dev, dtype=dtype)
                workspace_buf = torch.empty((4096,), device=dev, dtype=torch.int8)
                cutlass_bias = bias.view((4, C)).T.contiguous()
                for cutlass_dtype, koi_type in [
                    (torch.float16, lib.KOI_F16),
                    (torch.int8, lib.KOI_I8),
                ]:
                    in_out_bfr = torch.zeros((T + 3, N, C), device=dev, dtype=cutlass_dtype)
                    for direction, dir_str in [(-1, "rev"), (1, "fwd")]:
                        # reorder weights as <igigigigfofofofo>, and flip IH/HH order if reverse
                        if cutlass_dtype == torch.int8:
                            scale, cutlass_weights = quantize_tensor(weights)
                            scale = scale.to(torch.float16)
                            in_bfr_cutlass = (
                                (in_bfr.clip(-1.0, 1.0) * 127).round().to(torch.int8)
                            )
                        else:
                            scale = torch.ones((C, 4), device=dev, dtype=dtype)
                            cutlass_weights = weights
                            in_bfr_cutlass = in_bfr

                        cutlass_weights = cutlass_weights.view((2, C, 2, 2, -1, 4))
                        if direction == -1:
                            cutlass_weights = cutlass_weights.flip(0)
                        cutlass_weights = (
                            cutlass_weights.permute(4, 2, 5, 3, 0, 1)
                            .contiguous()
                            .view((-1, 2 * C))
                        )

                        if direction == -1:
                            in_out_bfr[1:-2] = in_bfr_cutlass.flip(0)
                        else:
                            in_out_bfr[2:-1] = in_bfr_cutlass
                            out_bfr = in_out_bfr[1:-2]
                        state_buf[:] = 0
                        lib.host_cutlass_lstm(
                            stream_ptr,
                            koi_type,
                            0,
                            N,
                            C,
                            T,
                            direction,
                            in_out_bfr.stride(1),
                            void_ptr(in_out_bfr),
                            void_ptr(cutlass_weights),
                            void_ptr(cutlass_bias),
                            void_ptr(scale),
                            void_ptr(state_buf),
                            void_ptr(workspace_buf),
                            0,
                            0,
                        )
                        stream.synchronize()
                        if direction == -1:
                            out_bfr = in_out_bfr[2:-1].flip(0)
                        if cutlass_dtype == torch.int8:
                            out_bfr = out_bfr.to(torch.float16) * (1 / 127.0)
                        show_diff_result(
                            f"Cutlass LSTM {dir_str} {cutlass_dtype}",
                            ref_out,
                            out_bfr,
                            3e-3,
                            1e-2,
                        )
