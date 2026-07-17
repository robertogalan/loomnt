"""Allow `python -m loomnt` and serve as the PyInstaller entry point."""

from loomnt.cli import main

if __name__ == "__main__":
    main()
