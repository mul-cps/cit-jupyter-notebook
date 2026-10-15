# Standard CPU Compute/RTC candidate

This overlay qualifies only the existing CIT standard CPU image at
`sha256:7cbef42fe051178e209bf5e245d6811bc8f8c24dff1bd07a639e1d812adbfd63`.
It is not a release of the PyTorch/TensorFlow variants or a production rollout.
The upstream CIT source is `92f744fdc39c632b28309ddebdc20ab82042d11b`.

`requirements.in` selects the reviewed framework versions. Resolve it **against
the exact base image**, using a wheelhouse with the matching versioned lean SDK
and prebuilt addon. Record the resolver report, then generate `install.lock`
containing the SHA256-pinned additions/upgrades only. The Dockerfile installs
that lock offline with dependency resolution disabled and runs a full
`pip check`. Do not force-reinstall the base's unrelated dependencies.

The qualification wheel pair comes from compute source
`ab0202e56aa20d0e2d4671fb661637830b6bcafc`; the addon includes the dedicated
visitor-route compatibility fix and its compiled entry is
`static/remoteEntry.c7eaea5553822765e8f8.js`. No Hub adapter, gateway extras or
credentials belong in the notebook image.

Build with a context containing this `Dockerfile` and
`wheelhouse/{install.lock,*.whl}`. The wheels are a temporary build bind mount,
so they are not copied into the final image. No startup command, working
directory or environment is overridden; the final user remains `jovyan`.
Use OCI manifest format to match the exact source image's runtime configuration.
The local builder's Docker-format conversion otherwise introduces a healthcheck
that is absent from that source OCI configuration. On the Fedora qualification
host the temporary build uses `--security-opt label=disable`
to read the wheel bind mount; no runtime security option is baked into the image.

Run `inventory.py` in the exact base and candidate. Compare versions and all
recorded CIT feature/startup/config file hashes; any changed version must be
part of the explicit resolver report, and no distribution may disappear. Run
`verify_runtime.py --execute --server-probe` in the candidate with networking
disabled. It checks the actual installed modules, discovery/config, prebuilt
entry and composed PageConfig hook, ordinary Hera serialization, successful
and failed Papermill execution, and an actual local Lab startup/served entry.

The server probe supplies `/services/cit-compute-ui/api/compute/v1/` only in its
test process. Deployment must provide a trusted PageConfig binding and the
SDK's trusted HTTPS gateway/source/CA environment through the Hub adapter.
The ab0202 frontend also maps the reviewed legacy
`/services/cit-admin/api/compute/v1/` binding to the dedicated CIT visitor path;
it does not fall back to requesting access to the administration console.
The corresponding visitor service and OAuth access must already be active.
Installing packages does not activate or qualify that live API/OAuth path.

Existing servers need a normal, user-coordinated restart to pick up a changed
image and newly enabled RTC server extensions. This candidate preparation does
not restart users or alter either Hub's configuration.
