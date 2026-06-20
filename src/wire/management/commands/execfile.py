"""
Executes the given Python source file under the context of the current
Django settings
"""

import os
import sys
from django.core.management.base import BaseCommand


def execute(script):
    kws = {"__name__": "__main__", "__file__": script}
    exec(compile(open(script).read(), script, "exec"), kws)


class Command(BaseCommand):
    help = " ".join([line.strip() for line in __doc__.strip().splitlines()])

    def add_arguments(self, parser):
        parser.add_argument("args", nargs="+")

    def handle(self, *args, **options):
        is_verbose = options.get("verbosity", 1) > 1
        script = os.path.abspath(os.path.expandvars(os.path.normpath(args[0])))
        if is_verbose:
            self.stderr.write(self.style.WARNING("Executing script {}".format(script)))

        sys.argv = [script] + list(args[1:])
        sys.path.append(os.path.dirname(script))

        execute(script)
