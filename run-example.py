"""
Script to run OpenUxAS examples.
"""

import argparse
import os
import pathlib
import re
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# These control the default directory that will be used for running OpenUxAS
# or OpenAMASE. They are configured to support the Vagrant machines specified
# in the OpenUxAS-bootstrap repository.
DEFAULT_AMASE_DIR = os.path.join(
    ROOT_DIR, "sbx", "x86_64-linux", "amase", "src")
DEFAULT_UXAS_DIR = os.path.join(
    ROOT_DIR, "sbx", "x86_64-linux", "uxas-release", "src")

# These control the name of the environment variable that will be checked for
# the OpenUxAS or OpenAMASE directories.
AMASE_ENV_KEY = "OPENAMASE_DIR"
UXAS_ENV_KEY = "OPENUXAS_DIR"

# Prefer the environment variable over the default directories.
AMASE_DIR = os.environ.get(AMASE_ENV_KEY, DEFAULT_AMASE_DIR)
UXAS_DIR = os.environ.get(UXAS_ENV_KEY, DEFAULT_UXAS_DIR)

DESCRIPTION = """
Run OpenUxAS, OpenAMASE or both, using the configuration in the specified
example.

This script is a frontend for both OpenUxAS and OpenAMASE that simplifies
running examples contained in the `examples` directory of the OpenUxAS
repository. You run an example by providing the path to its directory, under
`examples`. For example, run:

  python3 run-example.py 02_Example_WaterwaySearch

to run the Waterways example from a single terminal session. Or:

  python3 run-example.py --uxas 99_Tasks/AngledAreaSearchTask

to run just OpenUxAS for the angled-area example.
"""


def get_example_dir():
    """Get the path to the directory containing the example to run."""

    return os.path.join(args.uxas_dir, "examples", args.example)


def get_example_name():
    """Get the name of the example."""

    # The best way to get the name of the example seems to be to look at the
    # "Scenario_XXX.xml" file. That file's name consistently matches the name
    # of the cfg_ file for UxAS.
    files = os.listdir(get_example_dir())
    scenarios = [f for f in files if (f.startswith("Scenario_") and
                                      f.endswith(".xml"))]

    if not scenarios:
        raise Exception("No scenario file found in %s" % get_example_dir())

    filename = scenarios[0]

    if len(scenarios) > 1:
        print("Warning: multiple scenario files found in %s" %
              get_example_dir())
        print("  Using the first file: %s" % filename)

    return re.match(r'Scenario_(.*)\.xml', filename)[1]


def get_amase_wd():
    """Get the OpenAMASE working directory."""
    return os.path.join(args.amase_dir, "OpenAMASE")


def get_uxas_wd():
    """Make and return the OpenUxAS working directory."""

    wd = os.path.join(get_example_dir(), "RUNDIR_%s" % get_example_name())

    # Next, we need to create the working directory for the command. The XML
    # that configures UxAS for this example assumes a working directory next
    # to the XML file, so we create that. The name used for the working
    # directory is taken from the original launch script.
    pathlib.Path(wd).mkdir(parents=True, exist_ok=True)

    return wd


def get_amase_scenario():
    """Get the full path to the scenario XML for OpenAMASE."""
    return os.path.join(get_example_dir(),
                        "Scenario_%s.xml" % get_example_name())


def get_uxas_config():
    """Get the full path to the config XML for OpenUxAS."""

    filename = "cfg_%s.xml" % get_example_name()
    filepath = os.path.join(get_example_dir(), filename)

    if os.path.exists(filepath):
        return filepath
    else:
        # Try the alternate form:
        filename2 = "%s_cfg.xml" % get_example_name()
        filepath2 = os.path.join(get_example_dir(), filename)

        if os.path.exists(filepath2):
            return filepath2
        else:
            raise Exception("Neither %s nor %s are found in %s" %
                            (filename, filename2, get_example_dir()))


def get_amase_cmd():
    """Return the array representing a call to OpenAMASE."""

    return [
        "java", "-Xmx2048m",
        "-splash:%s" % os.path.join("data", "amase_splash.png"),
        "-classpath", "%s:%s" % (os.path.join("dist", "*"),
                                 os.path.join("lib", "*")),
        "avtas.app.Application",
        "--config", os.path.join("config", "amase"),
        "--scenario", get_amase_scenario()]


def run_amase():
    """Run the OpenAMASE part of the example."""

    # First, make sure we can find the Scenario:
    amase_cmd = get_amase_cmd()

    print("Running OpenAMASE for '%s'." % args.example)
    print(" ")

    subprocess.run(amase_cmd, cwd=get_amase_wd())


def get_uxas_cmd():
    """Return the array representing a call to OpenUxAS."""

    return [os.path.join(args.uxas_dir, "../", "install", "bin", "uxas"),
            "-cfgPath", get_uxas_config()]


def run_uxas():
    """Run the OpenUxAS part of the example."""

    # First, make sure we can find the cfg:
    uxas_cmd = get_uxas_cmd()

    print("Running OpenUxAS for '%s'." % args.example)
    print("Data and logfiles " +
          "are in:")
    print(get_uxas_wd())
    print(" ")

    subprocess.run(uxas_cmd, cwd=get_uxas_wd())


def run_both():
    """Run both OpenUxAS and OpenAMASE."""

    # First, let's make sure this will all work.
    uxas_cmd = get_uxas_cmd()
    amase_cmd = get_amase_cmd()

    # Next, start OpenUxAS
    print("Starting OpenUxAS in a separate process.")
    uxas_popen = subprocess.Popen(uxas_cmd, cwd=get_uxas_wd())

    # Now, start OpenAMASE
    print("Starting OpenAMASE in this process.")
    subprocess.run(amase_cmd, cwd=get_amase_wd())

    # Now, when we get here, that means that OpenAMASE was closed.
    print(" ")
    print("Shutting down OpenUxAS.")
    uxas_popen.terminate()


# Script processing.
if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION)

    ap.add_argument("example",
                    help="the example directory")

    ap.add_argument("--amase", dest="run_amase", default=False,
                    action="store_true",
                    help="run the OpenAMASE part of the example")

    ap.add_argument("--uxas", dest="run_uxas", default=False,
                    action="store_true",
                    help="run the OpenUxAS part of the example")

    ap.add_argument("--amase-dir", default=AMASE_DIR,
                    help="absolute path to the OpenAMASE repository " +
                         "containing build outputs")

    ap.add_argument("--uxas-dir", default=UXAS_DIR,
                    help="absolute path to the OpenUxAS repository " +
                         "containing build outputs")

    args = ap.parse_args()

    try:
        if args.run_amase:
            run_amase()

        elif args.run_uxas:
            run_uxas()

        else:
            run_both()

    except Exception as e:
        print(e, file=sys.stderr)
        print(" ", file=sys.stderr)
        ap.print_usage()
