FROM quay.io/jupyter/datascience-notebook:lab-4.5.3 AS base

ENV PIP_ROOT_USER_ACTION=ignore

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade \
    jupyterlab-git \
    nbgitpuller \
    jupyter-resource-usage \
    catppuccin-jupyterlab \
    jupyterlab-horizon-theme \
    jupyter-server-proxy \
    jupyter-glances-proxy \
    notebook-intelligence \
    git-credential-helpers && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging

USER root
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    --no-install-recommends \
    gh \
    nodejs \
    npm \
    jq \
    btop \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -aG sudo jovyan

ENV username=jovyan

RUN --mount=type=secret,id=root_password \
    if [ -f /run/secrets/root_password ] && [ -s /run/secrets/root_password ]; then \
    echo "${NB_USER}:$(cat /run/secrets/root_password)" | chpasswd ; \
    else \
    echo "INFO: /run/secrets/root_password missing or empty, skipping password change"; \
    fi

RUN chown -R jovyan:users /home/jovyan

USER jovyan
WORKDIR /home/jovyan
