"""Make sure __version__ matches version in pyproject.toml."""
import re
from pathlib import Path
from set_env import __version__
from loguru import logger


def test_version():
    """Test version."""
    version = ""

    # fetch version in pyproject.toml")
    try:
        text = Path("pyproject.toml").read_text()
        _ = re.findall(r"version\s*=\s*['\"]([\d.]+)", text)
        if _:
            version = _[0]
    except Exception as exc:
        logger.error(exc)

    assert version == __version__
