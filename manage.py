#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from decouple import config


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        config("DJANGO_SETTINGS_MODULE", default="config.settings.develop"),
    )
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
