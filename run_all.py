import os
import subprocess
import sys
import time

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'tmp', 'gpu_metrics.db')
COLLECTOR_CMD = [sys.executable, os.path.join(BASE_DIR, 'main.py')]
STREAMLIT_CMD = [
    'streamlit', 'run', os.path.join(BASE_DIR, 'visualizaer', 'streamlit_dashboard.py')
]
GPU_LOAD_CMD = [sys.executable, os.path.join(BASE_DIR, 'gpu_load_generator.py')]

def start_gpu_load():
    print("Starting GPU load test...")
    return subprocess.Popen(GPU_LOAD_CMD)

def start_collector():
    print("Starting NVIDIA GPU metrics collector...")
    return subprocess.Popen(COLLECTOR_CMD)

def start_streamlit():
    print("Starting Streamlit dashboard...")
    return subprocess.Popen(STREAMLIT_CMD)

if __name__ == "__main__":
    # Clean up the SQLite DB before running everything
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed old database at {DB_PATH}")
    gpu_proc = start_gpu_load()
    # Wait a bit to let GPU load start
    time.sleep(2)
    collector_proc = start_collector()
    # Wait a bit to let collector start and populate DB
    time.sleep(2)
    streamlit_proc = start_streamlit()
    try:
        gpu_proc.wait()
        collector_proc.wait()
        streamlit_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        gpu_proc.terminate()
        collector_proc.terminate()
        streamlit_proc.terminate()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"Removed database at {DB_PATH} on exit.")
