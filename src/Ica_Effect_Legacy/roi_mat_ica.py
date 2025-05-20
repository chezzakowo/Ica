import os
import sys
import time
import random
import tempfile
import shutil
import requests
import pygame
from PIL import ImageGrab
import ctypes

# --- CẤU HÌNH ---
FALL_WAIT_MS   = 3000      # ms chờ trước khi thả
EXIT_WAIT_S    = 2.5       # s chờ trước khi exit
GRAVITY        = 9000.0    # px/s²
DRAG_SPEED     = 15000.0    # px/s   kéo nền + ảnh sau va chạm

# HWND_TOPMOST constants
HWND_TOPMOST = -1
SWP_NOSIZE   = 0x1
SWP_NOMOVE   = 0x2
SWP_SHOWWINDOW = 0x0040

# Ảnh “nặng”
images = [
    {"type": "url", "data": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpemPTnDyYh9QUIiff6_ukvJTR2vwTepE3Rw&s"},
]

# Âm thanh vine boom
sound_url = "https://www.myinstants.com/media/sounds/vine-boom-bass-boost-sound-effect.mp3"

# --- TẠO THƯ MỤC TẠM ---
tmpdir = os.path.join(tempfile.gettempdir(), "Ica_legacy")
os.makedirs(tmpdir, exist_ok=True)

def cleanup_temp():
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

def download_file(url, fname):
    path = os.path.join(tmpdir, fname)
    if not os.path.exists(path):
        r = requests.get(url); r.raise_for_status()
        with open(path, "wb") as f: f.write(r.content)
    return path

def download_image(item, idx):
    if item["type"] == "url":
        ext = os.path.splitext(item["data"])[1] or ".jpg"
        return download_file(item["data"], f"img_{idx}{ext}")
    else:
        import base64
        data = base64.b64decode(item["data"])
        path = os.path.join(tmpdir, f"img_{idx}.png")
        with open(path, "wb") as f: f.write(data)
        return path

try:
    # 1) Chụp màn hình
    screenshot = ImageGrab.grab()
    sw, sh = screenshot.size
    ss_path = os.path.join(tmpdir, "screenshot.png")
    screenshot.save(ss_path)

    # 2) Tải ảnh “nặng” và âm thanh
    img_paths  = [download_image(img, i) for i, img in enumerate(images)]
    sound_path = download_file(sound_url, "vineboom.mp3")

    # 3) Khởi Pygame fullscreen
    pygame.init(); pygame.mixer.init()
    screen = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN)
    pygame.display.set_caption("Drop & Drag Demo")

    # Lấy hwnd và set always-on-top
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0,0,0,0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

    # Load surfaces
    bg_surf = pygame.image.load(ss_path).convert()
    bg_surf = pygame.transform.scale(bg_surf, (sw, sh))

    img_path = random.choice(img_paths)
    img_surf = pygame.image.load(img_path).convert_alpha()
    iw, ih = img_surf.get_size()
    scale = min((sw*0.5)/iw, (sh*0.5)/ih)
    img_surf = pygame.transform.scale(img_surf, (int(iw*scale), int(ih*scale)))
    iw, ih = img_surf.get_size()

    impact = pygame.mixer.Sound(sound_path)

    # Vị trí/vận tốc ban đầu của ảnh
    img_x = (sw - iw) / 2
    img_y = (sh - ih) / 2
    v = 0.0
    y_target = sh - ih

    # 4) Vẽ screenshot + ảnh ngay
    screen.blit(bg_surf, (0, 0))
    screen.blit(img_surf, (img_x, img_y))
    pygame.display.flip()

    # 5) Chờ 3 giây trước khi thả
    pygame.time.delay(FALL_WAIT_MS)

    # 6) Vòng lặp rơi chỉ riêng ảnh
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0
        v += GRAVITY * dt
        img_y += v * dt

        if img_y >= y_target:
            img_y = y_target
            break

        # redraw nền tĩnh + ảnh
        screen.blit(bg_surf, (0, 0))
        screen.blit(img_surf, (img_x, img_y))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                raise KeyboardInterrupt

    # 7) Va chạm: play sound
    impact.play()

    # 8) Kéo cả nền + ảnh cùng xuống cho đến khi hết view
    bg_y = 0.0
    while bg_y < sh or img_y < sh:
        dt = clock.tick(60) / 1000.0
        move = DRAG_SPEED * dt
        bg_y   += move
        img_y  += move

        # redraw nền ở y=bg_y, ảnh ở img_y
        screen.fill((0,0,0))
        screen.blit(bg_surf, (0, bg_y))
        if img_y < sh:
            screen.blit(img_surf, (img_x, img_y))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                raise KeyboardInterrupt

    # 9) Chờ 2.5s rồi thoát
    time.sleep(EXIT_WAIT_S)

except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
    # Dọn temp ngầm
    cleanup_temp()
    sys.exit()
