# AI Time Series GPU Metrics Collector

This project provides tools for collecting, testing, and visualizing GPU metrics, designed for AI time series workloads. It is suitable for deployment in Kubernetes clusters with GPU-powered nodes.

## Project Structure

- `gpu_metrics_collector.py`: Main script for collecting GPU metrics.
- `gpu_load_generator.py`, `gpu_load_test.py`: Scripts for generating and testing GPU load.
- `streamlit_dashboard.py`: Dashboard for visualizing collected metrics.
- `config/`: Contains configuration files for metrics collection, database, and load generation.
- `agent/`: Python package for agent logic, including metrics collection.
- `deployment/`: Contains Dockerfile and Kubernetes manifests for deploying the metrics collector.
- `requirements.txt`: Python dependencies.
- `run_all.py`, `main.py`: Entry points for running the suite.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the metrics collector locally**
   ```bash
   python gpu_metrics_collector.py
   ```

3. **Visualize metrics**
   ```bash
   streamlit run streamlit_dashboard.py
   ```

## Kubernetes Deployment

See `deployment/README.md` for instructions on containerizing and deploying the metrics collector in a Kubernetes cluster.

## Configuration

Edit files in the `config/` directory to customize collection intervals, batch sizes, and other parameters.

## License

Specify your license here.
