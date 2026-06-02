from pydantic_settings import BaseSettings
import anthropic

class Settings(BaseSettings):
    anthropic_api_key: str
    debug: bool = False
    use_mock_llm: bool = False

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)