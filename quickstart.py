import subprocess, sys, time, os, signal
from pathlib import Path

def start_server():
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "app.server:app", "--host", "127.0.0.1", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    proc = start_server()
    try:
        time.sleep(1.5)  # give uvicorn a moment
        # Run tests
        code = subprocess.call([sys.executable, "tests/run_tests.py"])
        if code != 0:
            sys.exit(code)
    finally:
        # terminate server
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    main()
