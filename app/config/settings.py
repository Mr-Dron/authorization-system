from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #DataBase
    DATABASE_URL: str
    
    #Token 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN: int
    ALGORITHM: str
    SECRET_KEY: str

    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()