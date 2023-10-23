
from dataclasses import dataclass


@dataclass
class Credentials():
    email: str = "EMAIL"
    password: str = "PASSWORD"

    def to_dict(self) -> dict:
        return {'email': self.email, 'password': self.password}
