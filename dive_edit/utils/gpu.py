"""GPU worker selection for the analysis pipeline.

GPU Whisper runs are process-heavy because every worker loads its own model
copy. The packaged app therefore uses one GPU worker and lets CTranslate2
handle device-level parallelism. CPU fallback remains single-worker to avoid
freezing low-end office machines.
"""
from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable, Mapping

_VRAM_PER_WORKER_GB = 1.2
WORKERS_CAP = 8
_WORKERS_CAP = WORKERS_CAP  # backward-compat alias


def _workers_from_free_vram_mb(
    free_mb: int,
    *,
    cap: int = WORKERS_CAP,
    vram_per_worker_gb: float = _VRAM_PER_WORKER_GB,
) -> int:
    free_gb = max(0.0, float(free_mb) / 1024.0)
    return max(1, min(int(cap), int(free_gb / vram_per_worker_gb)))


def detect_optimal_workers() -> tuple[int, str]:
    """Detect free GPU VRAM and return an informational worker estimate."""
    if not shutil.which("nvidia-smi"):
        return 1, "nvidia-smi not found -> CPU single worker"
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        # Use the first GPU because the app does not expose device picking yet.
        free_mb = int(out.stdout.strip().splitlines()[0])
        free_gb = free_mb / 1024.0
        workers = _workers_from_free_vram_mb(free_mb, cap=_WORKERS_CAP)
        return workers, f"GPU free VRAM={free_gb:.1f}GB -> workers={workers}"
    except (subprocess.SubprocessError, ValueError, IndexError, OSError) as e:
        return 1, f"nvidia-smi failed ({e}) -> CPU single worker"


def select_pipeline_workers(
    *,
    env: Mapping[str, str | None] | None = None,
    detector: Callable[[], tuple[int, str]] = detect_optimal_workers,
) -> tuple[int, str]:
    """Return the worker count the backend should pass to the pipeline.

    Packaged exe startup writes DIVE_* status variables after probing CUDA DLLs.
    Dev mode may leave them unset, so an unset CUDA status must not force CPU.
    """
    status = env if env is not None else {}
    force_cpu = status.get("DIVE_FORCE_CPU") == "1"
    cuda_status = status.get("DIVE_CUDA_STATUS")
    cudnn_status = status.get("DIVE_CUDNN_STATUS", "ok") or "ok"
    if force_cpu:
        return 1, "force CPU requested"
    if cuda_status == "none":
        return 1, "CUDA unavailable"
    if cudnn_status.startswith("missing"):
        return 1, f"cuDNN unavailable: {cudnn_status}"
    auto_workers, msg = detector()
    if auto_workers > 1:
        return 1, f"{msg} | GPU worker capped at 1"
    return 1, msg
