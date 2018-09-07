#!/usr/bin/env python
import os
import sys
import raven

RAVEN_CONFIG = {
    'dsn': 'https://9189cccf8cbd4829bf893cc021a5157a:457bc29f5129417287dcb2840ee3d4d3@sentry.io/1276449',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from otree.management.cli import execute_from_command_line
    execute_from_command_line(sys.argv, script_file=__file__)
