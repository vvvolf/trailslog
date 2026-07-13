from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    project_root: Path
    data_dir: Path
    db_path: Path


def load_config() -> Config:
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"

    return Config(
        project_root=project_root,
        data_dir=data_dir,
        db_path=data_dir / "trailslog.db",
    )
    