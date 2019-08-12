import threading
import time

exec_count = 0

def heart_beat():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))

    global exec_count
    exec_count += 1
    # 15秒后停止定时器
    if exec_count < 15:
        threading.Timer(1, heart_beat).start()

heart_beat()