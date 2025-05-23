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

## Docker & Kubernetes Deployment

### 1. Create Dockerfile

A script is provided to generate a Dockerfile in the `scripts/` directory:

```bash
./create_dockerfile.sh
```

This will create a Dockerfile at `scripts/Dockerfile` suitable for building your project image.

### 2. Build and Deploy to Kubernetes

To build the Docker image and deploy the application to your Kubernetes cluster, use:

```bash
./deploy_k8s.sh [image_tag]
```
- `image_tag` is optional (default: `ai-gpu-metrics-collector:latest`).
- This script will:
  - Build the Docker image using the generated Dockerfile.
  - Apply the Kubernetes manifests from the `deployment/` directory.

**Note:** Ensure you have Docker and `kubectl` installed and configured for your cluster.

### 3. Kubernetes Manifests

Kubernetes deployment and config files are in the `deployment/` directory:
- `metrics-collector-configmap.yaml`
- `metrics-collector-deployment.yaml`

You can customize these files as needed for your environment.

## Configuration

Edit files in the `config/` directory to customize collection intervals, batch sizes, and other parameters.

## License

This project is licensed under the terms of the LICENSE file found in the root of this repository.
