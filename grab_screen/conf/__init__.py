from .configs import Config

__all__ = ['config']

config = Config()
config.load()
config.load_logging()
