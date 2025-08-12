"""
Configuration management for AI Agent
Handles API keys and model settings for Claude and GPT
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for AI Agent settings"""
    
    def __init__(self):
        # API Keys
        self.anthropic_api_key: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
        
        # Model Settings
        self.claude_model: str = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
        self.gpt_model: str = os.getenv('GPT_MODEL', 'gpt-3.5-turbo')
        
        # Default model selection
        self.default_model: str = os.getenv('DEFAULT_MODEL', 'claude')
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not self.anthropic_api_key:
            missing_keys.append('ANTHROPIC_API_KEY')
        
        if not self.openai_api_key:
            missing_keys.append('OPENAI_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
    
    def get_model_config(self, model_type: str) -> dict:
        """Get configuration for specific model type"""
        if model_type.lower() == 'claude':
            return {
                'api_key': self.anthropic_api_key,
                'model': self.claude_model
            }
        elif model_type.lower() == 'gpt':
            return {
                'api_key': self.openai_api_key,
                'model': self.gpt_model
            }
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
