import torch
import time
import os
import yaml

def load_config(path=None):
    if path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'config', 'gpu_load_config.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def gpu_matrix_multiply_test():
    config = load_config()
    duration_sec = config.get('duration_sec', 3600)
    size = config.get('matrix_size', 4096)
    print(f"Starting GPU load test for {duration_sec} seconds with matrix size {size}x{size}...")
    start = time.time()
    a = torch.randn(size, size, device='cuda')
    b = torch.randn(size, size, device='cuda')
    while time.time() - start < duration_sec:
        c = torch.mm(a, b)
        _ = c.sum().item()
    print("GPU load test completed.")

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp', 'gpu_metrics.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed old database at {db_path}")
    gpu_matrix_multiply_test()
