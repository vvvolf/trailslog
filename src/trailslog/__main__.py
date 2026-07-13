from trailslog.app import ensure_runtime_dirs
from trailslog.config import load_config


def main() -> None:
    config = load_config()

    ensure_runtime_dirs(config)

    print("TrailsLog")
    print(f"Project root : {config.project_root}")
    print(f"Data directory: {config.data_dir}")
    print("Ready.")
    