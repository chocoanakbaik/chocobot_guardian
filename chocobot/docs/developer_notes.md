# Chocobot Guardian - Developer Notes

## Development status

The repository is being developed incrementally. A feature must have real implementation and appropriate verification before it is treated as complete.

## 2026-09-11 - Device discovery foundation

### Implemented

`chocobot/engine/system/device_discovery.py` now provides a local, read-only device discovery layer built on top of the existing `sysinfo.py` engine.

The module currently collects and organizes:

- Operating-system identity and Windows build when available.
- System and Python process architecture.
- CPU identity and logical processor count.
- Physical memory capacity and a conservative memory tier.
- Python runtime information.
- Local working-directory read/write capability.
- Windows administrator status when the operating system exposes the check.
- Existing system-information data for storage and graphics visibility.
- Conservative capability flags and compatibility recommendations.

### Architectural reason

This module separates **device discovery** from **component selection**. Discovery observes the environment. It does not install packages, modify configuration, request elevation, activate components, or force incompatible software to run.

The existing `chocobot/engine/system/sysinfo.py` remains the source of low-level system observations. `device_discovery.py` consumes those observations and converts them into a compatibility-oriented profile for future engine work.

### Safety constraints

The current implementation is intentionally read-only. A compatibility profile is an observation, not permission to modify the operating system.

Future component-selection or installer logic must consume the profile through an explicit detect -> analyze -> validate -> decide -> modify flow. It must not silently treat recommendations as installation instructions.

### Verification status

The implementation was inspected against the current repository architecture and the mandatory development rules. A network-isolated execution environment prevented cloning the GitHub repository for a local runtime test during this session, so a full runtime test of the new module is **not yet verified** here.

Do not mark adaptive device discovery as fully complete in the project roadmap until runtime testing is performed on the supported development environments.

### Related files

- `chocobot/engine/system/sysinfo.py` - existing low-level system information engine.
- `chocobot/engine/system/device_discovery.py` - compatibility-oriented discovery layer.
- `README.md` - project architecture and roadmap.
- `PERATURAN MUTLAK` - mandatory development rules.
