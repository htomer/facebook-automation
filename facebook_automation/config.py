from facebook_automation.facebook import Credentials
import yaml


class Config():

    def __init__(self, keyword: str, count: str, credentials):
        self.keyword = keyword
        self.count = count
        self.credentials = Credentials(**credentials)

    def __repr__(self) -> str:
        return "%s(keyword=%r, count=%r, %r)" % (self.__class__.__name__, self.keyword, self.count, self.credentials)

    @staticmethod
    def dump_default_config_to_file(file_name: str):
        default_config = {"keyword": "israel", "count": 30}
        default_creds = {"credentials": {
            "email": "EMAIL", "password": "PASSWORD"}}
        with open(file_name, "w") as file:
            yaml.dump(default_config, file)
            yaml.dump(default_creds, file)

    @classmethod
    def load_config_from_file(cls, file_name: str = 'config.yml'):
        try:
            # Load configs file.
            with open('config.yml', 'r') as yaml_file:
                config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

            # Load data from file into config intance.
            return cls(**config_data)
        except OSError as e:

            # Dump default configs.
            cls.dump_default_config_to_file(file_name)

            return None
