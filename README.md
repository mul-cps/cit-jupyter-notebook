# CIT Jupyter Notebooks

[![Build & Publish ML Variants](https://github.com/mul-cps/cit-jupyter-notebook/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/mul-cps/cit-jupyter-notebook/actions/workflows/docker-publish.yml)

This repository contains customized Jupyter Notebook Docker images tailored for machine learning and data science workloads at the Chair of Cyber-Physical Systems (CPS).

## 🚀 Images & Build Artifacts

Images are automatically built and published to the GitHub Container Registry (GHCR).

**Registry:** `ghcr.io/mul-cps/cps-jupyter-notebook`

| Variant | Tag Suffix | Description |
| :--- | :--- | :--- |
| **Standard CPU** | `standard-cpu` | Based on `jupyter/datascience-notebook`. Includes basic data science tools. |
| **PyTorch GPU** | `pytorch-code` | Based on `gpu-jupyter` with CUDA 12.x. Includes PyTorch 2.4, Transformers, and BoW. |
| **TensorFlow GPU** | `tf-code` | Based on `gpu-jupyter` with CUDA 12.x. Includes TensorFlow 2.17 and Keras. |

### Tags
- `latest-<suffix>`: Latest build from the `main` branch.
- `<branch>-<suffix>`: Build from a specific branch.
- `sha-<commit>-<suffix>`: Specific commit build.

---

## 🛠 Intended Usage

These images are designed to be used in:
1. **JupyterHub**: As spawned environments for students and researchers.
2. **Standalone Docker**: For local development or remote server execution.

### How to Use

#### Run locally (Standard CPU)
```bash
docker run -it --rm -p 8888:8888 ghcr.io/mul-cps/cps-jupyter-notebook:latest-standard-cpu
```

#### Run with GPU support (PyTorch)
```bash
docker run --gpus all -it --rm -p 8888:8888 ghcr.io/mul-cps/cps-jupyter-notebook:latest-pytorch-code
```

---

## 📦 What's Included?

All images share a common base of productivity tools:
- **Extensions**: `jupyterlab-git`, `nbgitpuller`, `jupyterlab-horizon-theme`, `catppuccin-jupyterlab`.
- **Utilities**: `gh`, `btop`, `tmux`, `jq`, `nodejs/npm`.
- **Proxies**: `jupyter-server-proxy`, `jupyter-glances-proxy`.
- **GPU Specific**: `nv-dashboard` for real-time monitoring.

---

## 🛠 Development

### Building Locally
You can build specific variants using the Dockerfiles in the `docker/` directory:

```bash
docker build -t local-jupyter:pytorch -f docker/Dockerfile.pytorch-code ./docker
```

### GitHub Actions
The [Build & Publish ML Variants](.github/workflows/docker-publish.yml) workflow handles multi-arch (currently amd64) builds and pushes to GHCR on changes to the `docker/` folder.
