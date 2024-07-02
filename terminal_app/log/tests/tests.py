from pathlib import Path
import sys

sys.path.append(Path(__file__).parent.parent.as_posix())


if __name__ == "__main__":
    print("Test 1...")
    import root
    
    assert (Path(__file__).parent / "root.root.log").exists()
    assert (Path(__file__).parent / "root/root.log").exists()
    assert (Path(__file__).parent / "root/child/child.log").exists()
    
    