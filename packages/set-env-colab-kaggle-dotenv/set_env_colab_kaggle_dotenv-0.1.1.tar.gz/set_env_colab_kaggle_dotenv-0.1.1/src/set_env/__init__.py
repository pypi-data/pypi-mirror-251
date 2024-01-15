"""Init."""
from .set_env import set_env


def hello():
    print("Hello from set-env!!")
    return "Hello from set-env!"


__version__ = "0.1.1"
__all__ = ("set_env",)
