__all__ = ["generate_path"]

import os
from pathlib import Path
from enum import Enum, auto

class ObjectType(Enum):
    File = auto()
    Dir = auto()

def generate_path(name: Path, x: int=0, object_type: ObjectType = ObjectType.File) -> Path:
    new_path = Path(name.parent / ((name.stem + ("_" + str(x) if x != 0 else "")).strip() + name.suffix))
    if not new_path.exists():
        if object_type == ObjectType.Dir:         
            os.mkdir(new_path)
        else:        
            with open(new_path, "w"):
                pass
        return new_path
    else:
        return generate_path(name, x + 1, object_type)
