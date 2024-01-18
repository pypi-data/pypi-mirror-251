import os


class Config:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            api_key=os.environ["SCHEMALESS_API_KEY"],
            base_url=os.environ["SCHEMALESS_BASE_URL"],
        )

    def get_api_key(self) -> str:
        return self.api_key

    def get_base_url(self) -> str:
        return self.base_url
