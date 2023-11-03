
from dataclasses import dataclass


@dataclass
class Credentials():
    email: str = ""
    password: str = ""

    def to_dict(self) -> dict:
        return {'email': self.email, 'password': self.password}
