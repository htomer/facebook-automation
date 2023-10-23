from dataclasses import dataclass, field, fields
import yaml

from facebook_automation.facebook import Credentials

DEFAULT_CONFIG_FILE = "config.yml"


@dataclass()
class Config():
    keyword: str = "israel"
    count: int = 30
    credentials: Credentials = field(default_factory=dict)

    def __post_init__(self):
        # Create credentials instance.
        self.credentials = Credentials(**self.credentials)

    @classmethod
    def from_dict(cls, d: dict) -> "Config":
        field_names = (field.name for field in fields(cls))
        return cls(**{k: v for k, v in d.items() if k in field_names})

    def to_dict(self) -> dict:
        return {'keyword': self.keyword, 'count': self.count, 'credentials': self.credentials.to_dict()}

    def dump_to_file_yaml(self, file_name: str = DEFAULT_CONFIG_FILE):
        with open(file_name, "w") as f:
            yaml.dump(self.to_dict(), f, sort_keys=False)

    @classmethod
    def load_from_file_yaml(cls, file_name: str = DEFAULT_CONFIG_FILE) -> "Config":
        try:
            # Load configs file.
            with open(file_name, 'r') as yaml_file:
                config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

                # Load data from file into config intance.
                return cls.from_dict(config_data)

        except OSError as e:

            # No config file available.
            return None
