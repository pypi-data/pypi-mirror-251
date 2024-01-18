from typing import Dict
from trimesh import load_mesh, Trimesh
from pathlib import Path


def load(object_name: str) -> Trimesh:
    p = Path(__file__).parent / "stl_files" / (object_name + ".stl")
    mesh = load_mesh(p)
    assert isinstance(mesh, Trimesh)
    return mesh


def cache_path() -> Path:
    p = Path("~/.cache/ycb_utils").expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_with_scale(object_name: str, scale: float) -> Trimesh:
    scale = round(scale, 2)
    key = f"{object_name}_{scale}"
    p = cache_path() / (key + ".stl")
    if not p.exists():
        mesh = load(object_name)
        mesh.apply_scale(scale)
        mesh.export(str(p))
        # primary reason for caching is not to avoid the time to apply scale
        # but to name the file with distinct name as some software (e.g. trimesh)
        # has file name as a metadata
    mesh = load_mesh(p)
    assert isinstance(mesh, Trimesh)
    return mesh


def load_all() -> Dict[str, Trimesh]:
    p = Path(__file__).parent / "stl_files"
    table = {}
    for fp in p.iterdir():
        mesh = load_mesh(fp)
        assert isinstance(mesh, Trimesh)
        table[fp.stem] = mesh
    return table
