from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    server_name: str = "mcp-gitlab-server"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    gitlab_token: str
    gitlab_url: str = "https://gitlab.com/api/v4"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
