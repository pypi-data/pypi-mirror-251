import os
import subprocess
import urllib
import urllib.parse
from typing import cast, Any, Sequence, Optional
import logging
import colorlog # type: ignore

_logger : Optional[logging.Logger] = None
def getLogger() -> logging.Logger:
    global _logger
    if _logger is None:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s:%(name)s:%(message)s'))
        _logger = cast(logging.Logger, colorlog.getLogger('travo'))
        _logger.addHandler(handler)
    return _logger

def urlencode(s: str) -> str:
    """
    Encode a string `s` for inclusion in a URL

    Parameters
    ----------
    s : str
        Input string to encode.

    Returns
    -------
    str
        Encoded string.

    Examples
    --------
        >>> urlencode("foo/bar!")
        'foo%2Fbar%21'
    """
    return urllib.parse.urlencode({'':s})[1:]

def run(args: Sequence[str],
        check: bool = True, **kwargs: Any) -> subprocess.CompletedProcess:
    """
    A wrapper around subprocess.run

    - logs command with pretty printing
    - set check=True by default
    """
    # Backport capture_output from Python 3.6
    if kwargs.get('capture_output'):
        del kwargs['capture_output']
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT
    getLogger().info("Running: " + ' '.join(args))
    return subprocess.run(args, check=check, **kwargs)

def git_get_origin(cwd: str = ".") -> str:
    """
    Return the origin of the current repository

    Parameters
    ----------
    cwd : str, optional
        Path to current working repository. The default is ".".

    Raises
    ------
    RuntimeError
        Raises if `git remote get-url origin` yields return code other than zero.

    Returns
    -------
    str
        URL of the repository at origin.
    
    Examples
    --------
        >>> tmp_path = getfixture('tmp_path')
        >>> result = subprocess.run(["git", "init"], cwd=tmp_path)
        >>> result = subprocess.run(["git", "remote", "add", "origin", "https://xxx.yy/truc.git"], cwd=tmp_path)
        >>> git_get_origin(tmp_path)
        'https://xxx.yy/truc.git'
        >>> os.chdir(tmp_path)
        >>> git_get_origin()
        'https://xxx.yy/truc.git'
    """
    result = run(["git", "remote", "get-url", "origin"], check=False, capture_output=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(result.stdout.decode().strip())
    lines = result.stdout.decode().splitlines()
    assert lines
    return cast(str, lines[0])
