from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # pydantic-settings will read these from a .env file if present,
    # or fall back to the defaults below (which match docker-compose.yml).
    postgres_url: str = (
        "postgresql+asyncpg://shopforge:shopforge_pass@localhost:5433/shopforge"
    )
    mongo_url: str = (
        "mongodb://shopforge:shopforge_pass@localhost:27018/shopforge?authSource=admin"
    )
    mongo_db_name: str = "shopforge"

    # Tell pydantic-settings to look for a .env file in the working directory.
    # extra="ignore" means unknown keys in .env won't cause an error.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# A single shared instance — import `settings` anywhere you need config.
settings = Settings()
