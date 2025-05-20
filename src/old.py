import psutil
import time
import random
import multiprocessing

def ktra_starrail():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == "StarRail.exe" or process.info['title']:
            return True
    return False

def xac_suat_spawn_ica():
    return random.random() < 0.50

def cpu_stress_worker():
    while True:
        pass  # Thực hiện phép tính vô hạn để tạo tải CPU

def memory_stress_worker(memory_mb):
    try:
        a = ' ' * (memory_mb * 1024 * 1024)  # Tạo chuỗi có kích thước memory_mb MB
        while True:
            time.sleep(1)  # Giữ chuỗi trong bộ nhớ
    except MemoryError:
        pass  # Xử lý khi không đủ bộ nhớ

def controlled_stress(Max_CPU_Load, Max_RAM_Usage, flag):
    cpu_processes = []
    memory_processes = []

    try:
        while flag.value:
            current_cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            current_ram_percent = mem.percent
            total_ram = mem.total / (1024 * 1024)  # Chuyển đổi sang MB

            load_to_add = Max_CPU_Load - current_cpu - 10  # Trừ đi 10% để chừa khoảng trống
            if load_to_add > 0:
                num_cores = psutil.cpu_count(logical=True)
                num_processes_to_add = int((load_to_add / 100) * num_cores)
                for _ in range(num_processes_to_add):
                    p = multiprocessing.Process(target=cpu_stress_worker)
                    p.start()
                    cpu_processes.append(p)

            ram_to_add_percent = Max_RAM_Usage - current_ram_percent - 10  # Trừ đi 10% để chừa khoảng trống
            if ram_to_add_percent > 0:
                ram_to_add_mb = int((ram_to_add_percent / 100) * total_ram)
                chunk_size = 256  # MB
                num_chunks = ram_to_add_mb // chunk_size
                for _ in range(num_chunks):
                    p = multiprocessing.Process(target=memory_stress_worker, args=(chunk_size,))
                    p.start()
                    memory_processes.append(p)

            time.sleep(1)  # Đợi trước khi kiểm tra lại
    finally:
        for p in cpu_processes + memory_processes:
            p.terminate()
            p.join()

if __name__ == '__main__':
    spawn_checked = False  # biến trạng thái, chưa kiểm tra

    while True:
        if ktra_starrail():
            print(f"✅🚂 Honkai: Star Rail đang chạy")
            if not spawn_checked:
                if xac_suat_spawn_ica():
                    print('✅🐎Ica trong lần khởi chạy này sẽ được spawn!')
                    print('⏳ Đợi 5 giây trước khi bắt đầu stress...')
                    time.sleep(5)  # Đợi 5 giây trước khi bắt đầu stress
                    Max_CPU_Load = 90# Mức sử dụng CPU tối đa cho phép (%)
                    Max_RAM_Usage = 75  # Mức sử dụng RAM tối đa cho phép (%)
                    flag = multiprocessing.Value('b', True)  # Cờ điều khiển

                    stress_process = multiprocessing.Process(target=controlled_stress, args=(Max_CPU_Load, Max_RAM_Usage, flag))
                    stress_process.start()
                    print('✅ Bắt đầu stress CPU và RAM')

                else:
                    print('❌🐎Ica trong lần khởi chạy này sẽ không được spawn!')
                spawn_checked = True
        else:
            print(f"❌🚂 Honkai: Star Rail đang không chạy")
            spawn_checked = False
        time.sleep(1.5)
