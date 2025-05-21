# Metrics Collector Kubernetes Deployment

This directory contains files to deploy the metrics collector in a Kubernetes cluster on GPU-powered nodes.

## Files
- `Dockerfile`: Containerizes the metrics collector.
- `metrics-collector-configmap.yaml`: Kubernetes ConfigMap for the collector's configuration.
- `metrics-collector-deployment.yaml`: Kubernetes Deployment manifest for the collector.

## Steps to Deploy

1. **Build and Push Docker Image**
   ```bash
   docker build -t <your-docker-repo>/metrics-collector:latest ..
   docker push <your-docker-repo>/metrics-collector:latest
   ```

2. **Apply ConfigMap and Deployment**
   ```bash
   kubectl apply -f metrics-collector-configmap.yaml
   kubectl apply -f metrics-collector-deployment.yaml
   ```

3. **Verify Deployment**
   ```bash
   kubectl get pods -l app=metrics-collector
   ```

**Note:**
- Replace `<your-docker-repo>` with your Docker registry path.
- The deployment is set to run only on nodes with GPUs (using `nvidia.com/gpu.present: "true"`).
- Adjust resource limits and environment variables as needed.
