from .kiem_tra_hsr import ktra_starrail
from .roi_con_ica import run as run_roi_con
from .roi_cua_so import run as run_roi_cua
from .roi_mat_ica import run as run_roi_mat
from .stress import controlled_stress
from .xac_suat_spawn_ica import xac_suat_spawn_ica

import random

__all__ = [
    "ktra_starrail",
    "controlled_stress",
    "xac_suat_spawn_ica",
    "random_spawn_effect",
    "roi_mat_ica",
    "roi_con_ica",
    "roi_cua_so"
]

def random_spawn_effect():
    """Chọn ngẫu nhiên 1 trong 3 hiệu ứng rơi, in tên và chạy nó."""
    funcs = {
        "roi_con_ica": run_roi_con,
        "roi_cua_so":  run_roi_cua,
        "roi_mat_ica": run_roi_mat,
    }
    name, func = random.choice(list(funcs.items()))
    print(f"🚀 Chạy hiệu ứng: {name}()")
    func()
