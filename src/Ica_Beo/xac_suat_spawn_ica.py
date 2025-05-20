import random

def xac_suat_spawn_ica():
    spawn_chance = 0.90  # Xác suất spawn (ví dụ: 50%)
    a = random.random()
    phan_tram = spawn_chance * 100
    print(f'🎲 Số được ngẫu nhiên: {a:.2f} |  Xác suất sẽ spawn: {phan_tram:.0f}%')
    
    if a <= spawn_chance:
        print("✅ Đã spawn!")
        return True
    else:
        print("❌ Không spawn.")
        return False
