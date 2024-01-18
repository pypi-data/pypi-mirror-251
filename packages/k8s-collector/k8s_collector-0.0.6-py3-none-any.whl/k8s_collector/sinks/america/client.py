class AmericaClient:
    def __init__(self, america_url: str, username: str, password: str):
        self._america_url = america_url
        self._username = username
        self._password = password

    def add(self, obj: dict) -> None:
        print(f'America client: {obj}')

    def update(self, obj: dict) -> None:
        print(f'America client: {obj}')

    def delete(self, obj: dict) -> None:
        print(f'America client: {obj}')
