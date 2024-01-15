# set-env

Set an environ varibale from colab, kaggle or dotenv (search default .env/dotenv/env)

## Intro

colab and kaggle bother provide a way to manage secrets (typically API tokens).

`set_env` is mainly for running ipynb (jupyter notebook) files in colab/kaggle or cloud instance when we need to set an environ variable, for example, `HF_TOKEN` to download models or datasets from huggingdace hub, other scenarios include `WANDB_API_KEY` or `NGROK_AUTHCODE` or `OPENAI_API_KEY` etc.

When running an ipynb in a cloud instance, we may use `dotenv` (`pip install python-dotenv`) to set environ varibales based on `.env`.

## Install
```
pip install set-env
```

## Use it
```
from set_env import set_env

# e.g.
set_env("HF_TOKEN")
set_env("WANDB_API_KEY")
set_env("NGROK_AUTHCODE")
```
