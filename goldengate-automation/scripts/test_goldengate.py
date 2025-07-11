#!/usr/bin/env python3
"""Spin up a Goldengate container and perform a basic deployment test."""

import subprocess
import os
import time
import sys

IMAGE = os.environ.get("GG_DOCKER_IMAGE", "oracle/goldengate:latest")
CONTAINER = "gg-test"


def run(cmd, **kwargs):
    print(" ".join(cmd))
    return subprocess.run(cmd, check=True, **kwargs)


def main():
    try:
        run(["docker", "pull", IMAGE])
        run(["docker", "run", "-d", "--name", CONTAINER, IMAGE])
        # Simplified validation step
        time.sleep(30)
        run(["docker", "exec", CONTAINER, "info"])
    finally:
        subprocess.run(["docker", "rm", "-f", CONTAINER], check=False)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
