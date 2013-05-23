#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    sys.argv.insert(1, 'test')

    if len(sys.argv) == 2:
        sys.argv.append('testapp_tests')

    execute_from_command_line(sys.argv)
