import yaml
import os

class ConfigManager:
    """
    A singleton class to manage a YAML configuration file.
    """
    _instance = None

    def __new__(cls, config_file_path="config.yaml"):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config_file_path = config_file_path
            cls._instance._config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """
        Loads the YAML configuration from the file.
        Creates an empty file if it doesn't exist.
        """
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as f:
                yaml.dump({}, f)  # Create an empty YAML file
            return {}
        try:
            with open(self.config_file_path, 'r') as f:
                return yaml.safe_load(f) or {}  # Handle empty files
        except yaml.YAMLError as e:
            print(f"Error loading YAML file '{self.config_file_path}': {e}")
            return {}

    def get(self, key, default=None):
        """
        Gets a value from the configuration.
        Returns the default value if the key is not found.
        """
        return self._config.get(key, default)

    def reload_config(self):
        """
        Reloads the configuration from the file.
        """
        self._config = self._load_config()
