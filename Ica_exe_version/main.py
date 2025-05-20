import time
import argparse
import multiprocessing
from Ica_Beo import (
    ktra_starrail,
    controlled_stress,
    xac_suat_spawn_ica,
    random_spawn_effect,
)

# Kiểm tra và hiển thị cảnh báo nếu CPU/RAM vượt mức an toàn
def can_continue(cpu, ram):
    cpu_warning = cpu > 85
    ram_warning = ram > 80

    if cpu_warning and ram_warning:
        print(f"🚨 Phát hiện tải stress cho CPU và RAM quá cao (CPU: {cpu}% > 85, RAM: {ram}% > 80). Nếu như để cao quá sẽ ảnh hưởng đến hiệu năng của máy và có thể gây ra lỗi hệ thống bên trong hoặc crash máy! Hãy cân nhắc điều chỉnh lại trước khi tiếp tục. Nếu như bạn vẫn muốn tiếp tục chạy, hãy bấm \"y\"")
    elif cpu_warning:
        print(f"⚠️ Phát hiện tải stress cho CPU quá cao ({cpu}% > 85). Nếu như để cao quá sẽ ảnh hưởng đến hiệu năng của máy! Hãy cân nhắc điều chỉnh lại trước khi tiếp tục. Nếu như bạn vẫn muốn tiếp tục chạy, hãy bấm \"y\"")
    elif ram_warning:
        print(f"⚠️ Phát hiện tải stress cho RAM quá cao ({ram}% > 80). Nếu như để cao quá sẽ ảnh hưởng đến hiệu năng của máy! Hãy cân nhắc điều chỉnh lại trước khi tiếp tục. Nếu như bạn vẫn muốn tiếp tục chạy, hãy bấm \"y\"")
    else:
        return True

    choice = input("Bạn có muốn tiếp tục không? (y/N): ").strip().lower()
    return choice == "y"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chạy giám sát Honkai: Star Rail với stress test và hiệu ứng.")
    multiprocessing.freeze_support()
    parser.add_argument("--stress", type=lambda x: x.lower() == 'true', default=True, help="Bật/Tắt stress test (True/False)")
    parser.add_argument("--effect", type=lambda x: x.lower() == 'true', default=True, help="Bật/Tắt hiệu ứng (True/False)")
    parser.add_argument("--cpuLimit", type=int, default=60, help="Giới hạn CPU load (%)")
    parser.add_argument("--ramLimit", type=int, default=45, help="Giới hạn RAM load (%)")

    args, unknown = parser.parse_known_args()


    Max_CPU_Load = args.cpuLimit
    Max_RAM_Usage = args.ramLimit
    enable_stress = args.stress
    enable_effect = args.effect

    print(f"✅ Thông tin khởi động: Stress CPU đang để {Max_CPU_Load}%, Stress RAM đang để {Max_RAM_Usage}%, "
          f"Effect: {'Bật✅' if enable_effect else 'Tắt❌'}, Stress: {'Bật✅' if enable_stress else 'Tắt❌'}")

    # Cảnh báo nếu vượt giới hạn an toàn
    if enable_stress and not can_continue(Max_CPU_Load, Max_RAM_Usage):
        print("⛔ Đã huỷ khởi động do tải stress quá cao.")
        exit(1)

    ktra_ica = False
    stress_proc = None
    effect_proc = None
    flag = multiprocessing.Value('b', False)
    last_status = None

    while True:
        running = ktra_starrail()

        if running != last_status:
            print("✅🚂 Honkai: Star Rail đang chạy!" if running else "❌🚂 Honkai: Star Rail đang không chạy!")
            last_status = running

        if running and not ktra_ica:
            if xac_suat_spawn_ica():
                print("✅🦄 Ica sẽ xuất hiện! Đợi 5s…")
                time.sleep(5)

                # Start effect
                if enable_effect:
                    effect_proc = multiprocessing.Process(target=random_spawn_effect)
                    effect_proc.start()

                # Start stress
                if enable_stress:
                    flag.value = True
                    stress_proc = multiprocessing.Process(
                        target=controlled_stress,
                        args=(Max_CPU_Load, Max_RAM_Usage, flag)
                    )
                    stress_proc.start()
                    print("✅ Bắt đầu stress máy")

            else:
                print("❌🐎 Ica không spawn ở lần mở game này")

            ktra_ica = True

        if not running and ktra_ica:
            # Dừng stress
            if stress_proc and stress_proc.is_alive():
                print("🛑 Dừng stress…")
                flag.value = False
                stress_proc.join(5)
                if stress_proc.is_alive():
                    stress_proc.terminate()
                    stress_proc.join()
            stress_proc = None

            # Dừng effect
            if effect_proc and effect_proc.is_alive():
                print("🛑 Dừng effect…")
                effect_proc.terminate()
                effect_proc.join()
            effect_proc = None

            ktra_ica = False

        time.sleep(1.5)
