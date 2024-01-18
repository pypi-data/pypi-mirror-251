from typing import Dict
from trimesh import load_mesh, Trimesh
from pathlib import Path


def load(object_name: str) -> Trimesh:
    p = Path(__file__).parent / "stl_files" / (object_name + ".stl")
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
