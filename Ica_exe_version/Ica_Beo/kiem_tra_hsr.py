import psutil

def ktra_starrail():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == "StarRail.exe":
            return True
    return False
