import toml
import os
from dataclasses import dataclass
from loguru import logger

@dataclass
class Config:
    config_path: str = os.path.join(os.path.dirname(__file__), '..', 'config_folder', 'config.toml')
    config: dict = None

    def load_config(self):
        """Loads the configuration file."""
        if not os.path.exists(self.config_path):
            logger.error("config dosyasi bulunamadi.")
            raise Exception("config dosyasi bulunamadi.")

        with open(self.config_path, 'r') as file:
            self.config = toml.load(file)
            
    
    def get_config(self, section: str):
        """Returns a specific section of the configuration as a dictionary."""
        if not self.config:
            self.load_config()
        return self.config.get(section, {})
