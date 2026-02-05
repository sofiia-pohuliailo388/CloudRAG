from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    COHERE_API_KEY: str
    GOOGLE_API_KEY: str  
    
    EMBEDDING_DIMENSION: int 
    EMBEDDING_MODEL: str 
    
    QDRANT_URL: str
    QDRANT_API_KEY: str
    
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()