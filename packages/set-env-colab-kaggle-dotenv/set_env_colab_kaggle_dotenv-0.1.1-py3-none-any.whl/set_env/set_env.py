"""Set an environ var in colab/kaggle/dotenv(search for .env dotenv env).

!pip install -q python-dotenv
"""
import os
import sys

from dotenv import dotenv_values, find_dotenv
from loguru import logger


def set_env(
    env_var="HF_TOKEN", source_var=None, envfile=None, override=False, verbose=False
):
    """
    Set environ var via google userdat/kaggle_secrets/[.env/dotenv/env].

    Args:
    ----
    env_var:
        env var to set, default HF_TOKEN.
    source_var:
        var from google/kaggle secret/userdata
        or defined in .env/dotenv/env
    envfile: file to read from, default, search
        for ['.env', 'dotenv', 'env']
    override:
        reset if set to True
    verbose:
        for loguru.logging, print TRACE if set

    Returns:
    -------
    value of the env var.
    """
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="TRACE")  # default "DEBUG"

    if override:
        if os.getenv(env_var) is not None:
            save_env_var = os.environ[env_var]
            del os.environ[env_var]
        logger.trace(f"{override=}")

    if source_var is None:
        source_var = env_var
    try:
        from google.colab import userdata

        try:
            os.environ[env_var] = userdata.get(source_var)
            logger.trace(f"colab: set {env_var}={source_var}")
        except (userdata.SecretNotFoundError, userdata.NotebookAccessError):
            ...
    except ModuleNotFoundError:
        ...
    if os.getenv(env_var):
        return os.getenv(env_var)

    # not enabled or not exist: kaggle_web_client.BackendError
    try:
        import kaggle_web_client
        from kaggle_secrets import UserSecretsClient

        user_secrets = UserSecretsClient()
        try:
            os.environ[env_var] = user_secrets.get_secret(source_var)  # BackendError
            logger.trace(f"kaggle: set {env_var}={source_var}")
        except kaggle_web_client.BackendError:
            ...
    except ModuleNotFoundError:
        ...

    if os.getenv(env_var):
        return os.getenv(env_var)

    # .env dotenv env
    # envfile = None
    if envfile is None:
        for _ in [".env", "dotenv", "env"]:
            envfile = find_dotenv(_)
            logger.trace(f"Found {envfile=}")
            if envfile:
                break

    if envfile:
        print(f"loading {envfile=} with dotenv_values(envfile)")
        if dotenv_values(envfile).get(source_var):
            os.environ[env_var] = dotenv_values(envfile).get(source_var)
            logger.trace(f"{envfile=}: set {env_var}={source_var}")
    if os.getenv(env_var):
        return os.getenv(env_var)

    # try manual input?
    logger.warning(
        f"""
        Unable to set {env_var}={source_var},
        not in colab or Secret not set, not kaggle
        or Secrets not set, no .env/dotenv/env file
        in the current working dir or parent dirs."""
    )

    # restore
    if override:
        if os.getenv(env_var) is not None:
            os.environ[env_var] = save_env_var

    return None
