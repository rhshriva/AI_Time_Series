"""
This module provides functions for collecting NVIDIA GPU metrics.

It is not intended to be run directly, but rather to be imported and used by other scripts.
"""
import subprocess
import sqlite3
import time
import yaml
import os
from datetime import datetime

def load_db_config(path=None):
    if path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, 'config', 'db_config.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_collector_config(path=None):
    if path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, 'config', 'metrics_collector_config.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Export the config loader functions for import in main.py
__all__ = [
    'load_db_config',
    'load_collector_config',
    'get_gpu_metrics',
    'init_db',
    'insert_metrics_batch'
]

def get_gpu_metrics():
    try:
        config = load_collector_config()
        query_fields = config.get('nvidia_query_fields', [
            'timestamp','name','utilization.gpu','utilization.memory','memory.total','memory.used','memory.free','temperature.gpu'])
        query_str = ','.join(query_fields)
        result = subprocess.check_output([
            'nvidia-smi',
            f'--query-gpu={query_str}',
            '--format=csv,noheader,nounits'
        ]).decode('utf-8').strip()
        metrics = result.split(', ')
        metrics_dict = {field.replace('.', '_'): (int(val) if val.isdigit() else val) for field, val in zip(query_fields, metrics)}
        return metrics_dict
    except Exception as e:
        print(f"Error collecting GPU metrics: {e}")
        return None

def init_db(db_path):
    collector_config = load_collector_config()
    query_fields = collector_config.get('nvidia_query_fields', [
        'timestamp','name','utilization.gpu','utilization.memory','memory.total','memory.used','memory.free','temperature.gpu'])
    # Map field names to SQL column names and types
    columns = []
    for field in query_fields:
        col = field.replace('.', '_')
        # Heuristic: if field contains 'utilization', 'memory', or 'temperature', use INTEGER, else TEXT
        if any(x in col for x in ['utilization', 'memory', 'temperature']):
            columns.append(f'{col} INTEGER')
        else:
            columns.append(f'{col} TEXT')
    columns_sql = ',\n        '.join(columns)
    sql = f'''CREATE TABLE IF NOT EXISTS gpu_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns_sql}
    )'''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def insert_metrics_batch(conn, batch):
    c = conn.cursor()
    # Dynamically get the fields from the first metric in the batch
    if not batch:
        return
    fields = list(batch[0].keys())
    placeholders = ', '.join(['?'] * len(fields))
    columns = ', '.join(fields)
    values = [tuple(m.get(f, None) for f in fields) for m in batch]
    c.executemany(f'''INSERT INTO gpu_metrics ({columns}) VALUES ({placeholders})''', values)
    conn.commit()
