from pydantic import BaseSettings
class Settings(BaseSettings):
    database_hostname : str = ''
    database_port : int = 5432
    database_password : str  = ''
    database_name : str  = ''
    database_username : str  = ''
    secret_key : str  = ''
    algorithm : str  = ''
    access_token_expire_minutes : int = 30
    
    class Config:
        env_file =".env"

setting = Settings()
