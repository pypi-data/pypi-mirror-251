"""WIP stuff using only the primites from fabric instead of our Remote/SlurmRemote
classes
"""
import fabric
from milatools.cli.utils import T
import functools


def make_get_output_fn(login_node_remote_runner: fabric.runners.Remote, hostname: str):
    return functools.partial(_get_output, login_node_remote_runner, hostname)


def _get_output(
    login_node_remote_runner: fabric.runners.Remote, hostname: str, cmd: str, **kwargs
):
    """TODO: WIP: Trying to get rid of the need for the `SlurmRemote` class."""
    result = login_node_remote_runner.run(
        cmd,
        # These two (echo and echo_format) do the same thing as the 'self.display'
        # method of our `Remote` class.
        echo=True,
        echo_format=T.bold_cyan(f"({hostname})" + " $ {command}"),
        in_stream=False,  # disable in_stream so tests work correctly.
        hide="stdout",  # hide stdout because we'll be printing it in colour below.
        **kwargs,
    )
    # TODO: Take a look at "stream watchers" in the fabric docs.
    assert result
    output = result.stdout.strip()
    print(T.cyan(output))
    return output
