"""Set an environ var in colab/kaggle/dotenv(search for .env dotenv env).

!pip install -q python-dotenv
"""
import os

from dotenv import dotenv_values, find_dotenv


def set_env(env_var="HF_TOKEN", source_var=None, envfile=None, override=False):
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

    Returns:
    -------
    value of the env var.
    """
    if override:
        if os.getenv(env_var) is not None:
            del os.environ[env_var]

    if source_var is None:
        source_var = env_var
    try:
        from google.colab import userdata

        try:
            os.environ[env_var] = userdata.get(source_var)
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
            if envfile:
                break

    if envfile:
        print(f"loading {envfile=} with dotenv_values(envfile)")
        if dotenv_values(envfile).get(source_var):
            os.environ[env_var] = dotenv_values(envfile).get(source_var)

    if os.getenv(env_var):
        return os.getenv(env_var)

    # try manual input?
    return None
