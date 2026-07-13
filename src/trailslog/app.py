from trailslog.config import Config


def ensure_runtime_dirs(config: Config) -> None:
    config.data_dir.mkdir(parents=True, exist_ok=True)
    