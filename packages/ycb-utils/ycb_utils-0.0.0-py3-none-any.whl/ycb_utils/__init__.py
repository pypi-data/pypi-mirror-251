from typing import Dict
from trimesh import load_mesh, Trimesh
from pathlib import Path


def load(object_name: str) -> Trimesh:
    p = Path(__file__).parent / "stl_files" / file_name + ".stl"
    return load_mesh(p)


def load_all() -> Dict[str, Trimesh]:
    p = Path(__file__).parent / "stl_files"
    return {f.stem: load_mesh(f) for f in p.iterdir() if f.suffix == ".stl"}
