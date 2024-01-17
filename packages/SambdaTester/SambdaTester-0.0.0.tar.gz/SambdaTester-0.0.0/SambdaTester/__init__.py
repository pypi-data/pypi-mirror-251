from .app import DoItLive

def run(config_path: str = None, path: str = None):
    return DoItLive(config_path)