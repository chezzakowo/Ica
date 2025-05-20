import os
import time
import random
import tempfile
import shutil
import requests
import pygame
from PIL import ImageGrab
import ctypes

# --- CẤU HÌNH ---
FALL_WAIT_MS   = 3000       # ms chờ trước khi thả
EXIT_WAIT_S    = 2.5        # s chờ trước khi exit
GRAVITY        = 14000.0    # px/s²
DRAG_SPEED     = 9500.0     # px/s

# HWND_TOPMOST constants
HWND_TOPMOST   = -1
SWP_NOSIZE     = 0x1
SWP_NOMOVE     = 0x2
SWP_SHOWWINDOW = 0x0040

# Danh sách ảnh "nặng"
images = [
    {"type": "url", "data": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpemPTnDyYh9QUIiff6_ukvJTR2vwTepE3Rw&s"},
]

# Âm thanh vine boom
sound_url = "https://www.myinstants.com/media/sounds/tf2-heavy-pan-effect.mp3"

# Thư mục tạm
tmpdir = os.path.join(tempfile.gettempdir(), "Ica")

def cleanup_temp():
    shutil.rmtree(tmpdir, ignore_errors=True)

def download_file(url, fname):
    os.makedirs(tmpdir, exist_ok=True)
    path = os.path.join(tmpdir, fname)
    if not os.path.exists(path):
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    return path

def download_image(item, idx):
    os.makedirs(tmpdir, exist_ok=True)
    if item["type"] == "url":
        ext = os.path.splitext(item["data"])[1] or ".jpg"
        return download_file(item["data"], f"img_{idx}{ext}")
    else:
        import base64
        data = base64.b64decode(item["data"])
        path = os.path.join(tmpdir, f"img_{idx}.png")
        with open(path, "wb") as f:
            f.write(data)
        return path

def run():
    print("🚀 Chạy hiệu ứng: roi_mat_ica()")
    try:
        os.makedirs(tmpdir, exist_ok=True)

        # 1. Chụp màn hình
        screenshot = ImageGrab.grab()
        sw, sh = screenshot.size
        ss_path = os.path.join(tmpdir, "screenshot.png")
        screenshot.save(ss_path)

        # 2. Tải ảnh và âm thanh
        img_paths  = [download_image(img, i) for i, img in enumerate(images)]
        sound_path = download_file(sound_url, "vineboom.mp3")

        # 3. Init Pygame fullscreen
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN)
        pygame.display.set_caption("Drop & Drag Demo")

        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                          SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

        # 4. Load ảnh
        bg_surf = pygame.image.load(ss_path).convert()
        bg_surf = pygame.transform.scale(bg_surf, (sw, sh))

        img_path = random.choice(img_paths)
        img_surf = pygame.image.load(img_path).convert_alpha()
        iw, ih = img_surf.get_size()
        scale = min((sw*0.5)/iw, (sh*0.5)/ih)
        img_surf = pygame.transform.scale(img_surf, (int(iw*scale), int(ih*scale)))
        iw, ih = img_surf.get_size()

        impact = pygame.mixer.Sound(sound_path)

        img_x = (sw - iw) / 2
        img_y = (sh - ih) / 2
        v = 0.0
        y_target = sh - ih

        # Hiển thị ngay ảnh và nền
        screen.blit(bg_surf, (0, 0))
        screen.blit(img_surf, (img_x, img_y))
        pygame.display.flip()

        pygame.time.delay(FALL_WAIT_MS)

        # 5. Rơi tự do
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60) / 1000.0
            v += GRAVITY * dt
            img_y += v * dt
            if img_y >= y_target:
                img_y = y_target
                break
            screen.blit(bg_surf, (0, 0))
            screen.blit(img_surf, (img_x, img_y))
            pygame.display.flip()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    raise KeyboardInterrupt

        # 6. Âm thanh va chạm
        impact.play()

        # 7. Kéo cả nền + ảnh xuống
        bg_y = 0.0
        while bg_y < sh or img_y < sh:
            dt = clock.tick(60) / 1000.0
            move = DRAG_SPEED * dt
            bg_y  += move
            img_y += move

            screen.fill((0, 0, 0))
            screen.blit(bg_surf, (0, bg_y))
            if img_y < sh:
                screen.blit(img_surf, (img_x, img_y))
            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    raise KeyboardInterrupt

        time.sleep(EXIT_WAIT_S)

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        cleanup_temp()
