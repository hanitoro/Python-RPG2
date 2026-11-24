"""Запускает локальную версию квеста с надёжным сохранением прогресса.

Не требует интернета; слушает только 127.0.0.1.
"""
import functools
import http.server
import os
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8765

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args):
        pass

if __name__ == "__main__":
    try:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    except OSError:
        print(f'Порт {PORT} занят. Возможно, квест уже запущен.')
        webbrowser.open(f'http://127.0.0.1:{PORT}/START_HERE.html')
        raise SystemExit(0)
    url = f'http://127.0.0.1:{PORT}/START_HERE.html'
    print('Академия Ауриона готова. Браузер открывается...')
    print('Работает без интернета:',url)
    print('Оставь это окно открытым на время игры. Для выхода закрой его.')
    threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.4)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
