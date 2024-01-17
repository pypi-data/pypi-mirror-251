import sys
import os
from .yams.yams import Yams
from .config.config import Configurator, EnvironmentType

class DoItLive():

    def __init__(config_path: str | None):
            
        #total arguments
        config = Configurator(config_path, EnvironmentType.Dev)

        yaml_file = Yams(config.Config)
        yaml_file.parse_file()