import subprocess  # noqa: S404


def run(command, args=None, *, force=False):
    if args is None:
        args = []
    if force:
        args.insert(0, "--force")
    subprocess.run([command, *args], check=True)  # noqa: S603
