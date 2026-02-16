"""
Configuration settings for UnifySense
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # DynamoDB settings
    dynamodb_table_name: str = "unifysense-patients"
    
    # S3 settings
    s3_bucket_name: str = "unifysense-documents"
    
    # Nova model IDs
    nova_pro_model_id: str = "amazon.nova-pro-v1:0"
    nova_lite_model_id: str = "amazon.nova-lite-v1:0"
    nova_micro_model_id: str = "amazon.nova-micro-v1:0"
    
    # Application settings
    max_tokens: int = 2048
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()
