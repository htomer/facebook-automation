
class Credentials():
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return "%s(email=%r, pass=%r)" % (self.__class__.__name__, self.email, self.password)
