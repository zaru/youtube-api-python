import settings
import os


def _make_dir():
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)


def main():
    _make_dir()


if __name__ == "__main__":
    main()
