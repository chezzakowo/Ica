import pygame
import sys
import os
import requests
import tempfile
import time
import pyautogui
import ctypes
import atexit
import shutil
from pygame.locals import *

# ========== CẤU HÌNH ==========
GRAVITY_MAIN = 9200
GRAVITY_BG = 24000
EXIT_DELAY = 2.5
IMAGE_SIZE = (400, 400)
TEMPDIR = os.path.join(tempfile.gettempdir(), 'Ica')
os.makedirs(TEMPDIR, exist_ok=True)
# ==============================

HWND_TOPMOST = -1
SWP_NOSIZE = 0x1
SWP_NOMOVE = 0x2
SWP_SHOWWINDOW = 0x0040

def cleanup():
    shutil.rmtree(TEMPDIR, ignore_errors=True)

def download_resource(url, filename):
    path = os.path.join(TEMPDIR, filename)
    if not os.path.exists(path):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    return path

def run():
    """Chạy hiệu ứng rơi cửa sổ (console) và background."""
    atexit.register(cleanup)

    # chụp màn hình
    screenshot_path = os.path.join(TEMPDIR, "screenshot.jpg")
    pyautogui.screenshot().save(screenshot_path)

    sound_path = download_resource(
        "https://www.myinstants.com/media/sounds/vine-boom-bass-boost-sound-effect.mp3",
        "vine_boom.mp3"
    )

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), FULLSCREEN | NOFRAME)
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0,0,0,0,
                                      SWP_NOMOVE|SWP_NOSIZE|SWP_SHOWWINDOW)

    w, h = screen.get_size()
    background = pygame.transform.scale(
        pygame.image.load(screenshot_path), (w,h)
    ).convert()
    black = pygame.Surface((w,h)); black.fill((0,0,0))

    main_img = pygame.transform.scale(
        pygame.image.load(download_resource(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpemPTnDyYh9QUIiff6_ukvJTR2vwTepE3Rw&ss",
            "main_image.jpg"
        )), IMAGE_SIZE
    )
    rect = main_img.get_rect(center=(w//2, -IMAGE_SIZE[1]//2))

    clock = pygame.time.Clock()
    v_main = v_bg = bg_y = 0
    state = "falling_main"
    played = False

    running = True
    while running:
        dt = clock.tick(120) / 1000
        for ev in pygame.event.get():
            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                running = False

        if state == "falling_main":
            v_main += GRAVITY_MAIN * dt
            rect.y += v_main * dt
            if rect.top > h:
                rect.bottom = h
                state = "background_fall"

        elif state == "background_fall":
            if not played:
                pygame.mixer.Sound(sound_path).play()
                played = True
            v_bg += GRAVITY_BG * dt
            bg_y += v_bg * dt
            if bg_y > h:
                state = "exit"
                exit_t = time.time()

        elif state == "exit":
            if time.time() - exit_t > EXIT_DELAY:
                running = False

        screen.blit(black, (0,0))
        screen.blit(background, (0, bg_y))
        screen.blit(main_img, rect)
        pygame.display.flip()

    pygame.quit()
    cleanup()
