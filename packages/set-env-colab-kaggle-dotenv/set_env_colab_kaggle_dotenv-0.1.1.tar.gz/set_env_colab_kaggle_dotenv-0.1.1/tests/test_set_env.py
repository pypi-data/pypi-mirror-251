"""Test set_env."""
import os
from set_env import set_env


def test_hf_token():
    """Test dotenv HF_TOKEN."""
    set_env("HF_TOKEN", verbose=True)
    assert os.getenv("HF_TOKEN").startswith("hf")


def test_hf_token_w():
    """Test dotenv HF_TOKEN_W."""
    set_env("HF_TOKEN", "HF_TOKEN_W", override=True, verbose=True)
    _ = os.getenv("HF_TOKEN")
    assert _ == "hf...w"
