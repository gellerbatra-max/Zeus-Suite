from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    platform_api_url: str = "http://localhost:8000"
    database_url: str = "postgresql+psycopg://zeus:zeus@localhost:5432/zeus_suite"
    # Sec 2.1: Gerber's own documented ~2,000-style chunking guidance, "a floor, not a ceiling"
    # (Sec 7 Step 5). `/run` processes at most this many still-pending items per call, so a
    # multi-thousand-item batch bounds each request instead of blocking on the whole batch --
    # overridable in tests to exercise the chunking logic without needing thousands of fixtures.
    migration_chunk_size: int = 2000
    # Azurite by default -- same local-dev connection string every other app in the suite uses.
    storage_connection_string: str = (
        "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )


settings = Settings()
