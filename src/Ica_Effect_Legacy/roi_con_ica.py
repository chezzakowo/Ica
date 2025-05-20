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
GRAVITY_BG = 23000
EXIT_DELAY = 2.5
IMAGE_SIZE = (400, 400)
TEMPDIR = os.path.join(tempfile.gettempdir(), 'Ica_legacy')
os.makedirs(TEMPDIR, exist_ok=True)
# ==============================

# Cấu hình hiển thị trên cùng
HWND_TOPMOST = -1
SWP_NOSIZE = 0x1
SWP_NOMOVE = 0x2
SWP_SHOWWINDOW = 0x0040

def cleanup():
    """Xóa thư mục tạm và mọi thứ bên trong"""
    try:
        shutil.rmtree(TEMPDIR, ignore_errors=True)
    except Exception as e:
        pass

# Đăng ký hàm dọn dẹp khi thoát
atexit.register(cleanup)

def download_resource(url, filename):
    os.makedirs(TEMPDIR, exist_ok=True)
    path = os.path.join(TEMPDIR, filename)
    if not os.path.exists(path):
        try:
            r = requests.get(url, stream=True)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            print(f"Lỗi tải tài nguyên: {e}")
            sys.exit()
    return path

# Chụp màn hình
screenshot_path = os.path.join(TEMPDIR, "screenshot.jpg")
try:
    pyautogui.screenshot().save(screenshot_path)
except Exception as e:
    print(f"Không thể chụp màn hình: {e}")
    sys.exit()

# Tải âm thanh
sound_url = "https://www.myinstants.com/media/sounds/vine-boom-bass-boost-sound-effect.mp3"
sound_path = download_resource(sound_url, "vine_boom.mp3")

# Khởi tạo Pygame và cài đặt window topmost
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), FULLSCREEN | pygame.NOFRAME)

# Đặt cửa sổ lên trên cùng mọi thứ
hwnd = pygame.display.get_wm_info()['window']
ctypes.windll.user32.SetWindowPos(
    hwnd,
    HWND_TOPMOST,
    0, 0, 0, 0,
    SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
)

width, height = screen.get_size()

# Load hình ảnh
background = pygame.transform.scale(pygame.image.load(screenshot_path), (width, height)).convert()
black_surface = pygame.Surface((width, height)).convert()
black_surface.fill((0, 0, 0))

# Load ảnh chính
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpemPTnDyYh9QUIiff6_ukvJTR2vwTepE3Rw&s"
main_image = pygame.transform.scale(pygame.image.load(download_resource(image_url, "main_image.jpg")), IMAGE_SIZE)
main_rect = main_image.get_rect(center=(width//2, -IMAGE_SIZE[1]//2))

# Vật lý
clock = pygame.time.Clock()
velocity_main = 0
velocity_bg = 0
bg_y = 0
state = "falling_main"
sound_played = False

running = True
while running:
    dt = clock.tick(120) / 1000
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    if state == "falling_main":
        velocity_main += GRAVITY_MAIN * dt
        main_rect.y += velocity_main * dt
        
        if main_rect.top > height:
            main_rect.bottom = height
            state = "background_fall"
            
    elif state == "background_fall":
        if not sound_played:
            pygame.mixer.Sound(sound_path).play()
            sound_played = True
        velocity_bg += GRAVITY_BG * dt
        bg_y += velocity_bg * dt
        
        if bg_y > height:
            state = "exit"
            exit_time = time.time()
            
    elif state == "exit":
        if time.time() - exit_time > EXIT_DELAY:
            running = False

    # Vẽ frame
    screen.blit(black_surface, (0, 0))
    screen.blit(background, (0, bg_y))
    screen.blit(main_image, main_rect)
    pygame.display.update()

# Dọn dẹp cuối cùng
pygame.quit()
cleanup()
sys.exit()