from pydantic import BaseSettings


class Config(BaseSettings):
    DB_PROTOCOL: str
    DB_SERVER: str

    class Config:
        case_sensitive = True


config = Config()
