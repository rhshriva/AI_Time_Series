from agent.gpu_metrics_collector import load_db_config, load_collector_config, get_gpu_metrics, init_db, insert_metrics_batch
import sqlite3
import time

def main():
    db_config = load_db_config()
    collector_config = load_collector_config()
    db_path = db_config['sqlite_db_path']
    interval = collector_config['collection_interval_sec']
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    batch = []
    batch_size = 10
    try:
        while True:
            metrics = get_gpu_metrics()
            if metrics:
                batch.append(metrics)
                print(f"Collected metrics at {metrics.get('timestamp', 'unknown')}")
            if len(batch) >= batch_size:
                insert_metrics_batch(conn, batch)
                print(f"Inserted batch of {len(batch)} metrics.")
                batch.clear()
            time.sleep(interval)
    except KeyboardInterrupt:
        if batch:
            insert_metrics_batch(conn, batch)
            print(f"Inserted final batch of {len(batch)} metrics.")
        conn.close()
        print("Exiting and closed DB connection.")

if __name__ == "__main__":
    main()
