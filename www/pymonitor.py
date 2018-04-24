import os
import subprocess
import sys
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def log(s):
    print('[Monitor] {}'.format(s))


class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, f):
        super().__init__()
        self.restart = f  # 传入restart_process函数

    def on_any_event(self, event):
        # 检测到py文件有改动, 调用传入的函数
        if event.src_path.endswith('.py'):
            log('Python source file changed: {}'.format(event.src_path))
            self.restart()


command = ['echo', 'ok']
process = None


def kill_process():  # 关闭进程
    global process
    if process:
        log('Kill process [{}]...'.format(process.pid))
        process.kill()
        process.wait()
        log('Process ended with code {}.'.format(process.returncode))
        process = None


def start_process():  # 启动进程
    global process, command
    log('Start process {}...'.format(' '.join(command)))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def restart_process():  # 重启进程
    kill_process()
    start_process()


def start_watch(path, callback):  # 监视path路径文件变化
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    log('Watching directory {}...'.format(path))
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()  # ctrl-c停止监视
    observer.join()


if __name__ == '__main__':
    argv = sys.argv[1:]  # 命令行参数
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python')
    command = argv
    path = os.path.abspath('.')  # 监视当前py文件所在目录
    start_watch(path, None)
