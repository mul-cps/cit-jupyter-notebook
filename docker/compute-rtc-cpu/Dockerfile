# Qualified standard-CPU candidate only; preserve the existing CIT image contract.
FROM ghcr.io/mul-cps/cit-jupyter-notebook@sha256:7cbef42fe051178e209bf5e245d6811bc8f8c24dff1bd07a639e1d812adbfd63
USER root
# Install only the resolved, hash-locked additions/upgrades from the wheelhouse.
# A bind mount keeps wheels out of the final image and its layer history.
RUN --mount=type=bind,source=wheelhouse,target=/tmp/compute-wheelhouse,ro \
    python -m pip install --no-cache-dir --no-index --no-deps --require-hashes \
      --find-links=/tmp/compute-wheelhouse \
      -r /tmp/compute-wheelhouse/install.lock && \
    python -m pip check
USER jovyan
# Entrypoint, command, working directory and all CIT startup/config files are inherited.
