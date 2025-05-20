import time
import psutil
import multiprocessing

def cpu_stress_worker(run_flag):
    while run_flag.value:
        pass

def memory_stress_worker(memory_mb, run_flag):
    try:
        a = ' ' * (memory_mb * 1024 * 1024)  # Allocate memory
        while run_flag.value:
            time.sleep(1)
    except MemoryError:
        pass

def controlled_stress(Max_CPU_Load, Max_RAM_Usage, flag):
    cpu_processes = []
    memory_processes = []

    # Shared run flag for all worker processes
    run_flag = multiprocessing.Value('b', True)

    try:
        while flag.value:
            current_cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            current_ram_percent = mem.percent
            total_ram = mem.total / (1024 * 1024)  # in MB

            # CPU stress
            load_to_add = Max_CPU_Load - current_cpu - 10
            if load_to_add > 0:
                num_cores = psutil.cpu_count(logical=True)
                num_processes_to_add = int((load_to_add / 100) * num_cores)
                for _ in range(num_processes_to_add):
                    p = multiprocessing.Process(target=cpu_stress_worker, args=(run_flag,))
                    p.start()
                    cpu_processes.append(p)

            # RAM stress
            ram_to_add_percent = Max_RAM_Usage - current_ram_percent - 10
            if ram_to_add_percent > 0:
                ram_to_add_mb = int((ram_to_add_percent / 100) * total_ram)
                chunk_size = 256  # Each process tries to allocate 256MB
                num_chunks = ram_to_add_mb // chunk_size
                for _ in range(num_chunks):
                    p = multiprocessing.Process(target=memory_stress_worker, args=(chunk_size, run_flag))
                    p.start()
                    memory_processes.append(p)

            time.sleep(1)

    finally:
        print("🧹 Dọn dẹp các tiến trình stress...")
        run_flag.value = False  # Báo cho các tiến trình con dừng lại

        for p in cpu_processes + memory_processes:
            if p.is_alive():
                p.terminate()
            p.join()
        print("✅ Đã dừng tất cả tiến trình stress.")
