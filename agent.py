"""
AI Agent implementation supporting Claude and GPT models
Excludes Gemini as per requirements
"""
from typing import List, Dict, Any, Optional
import anthropic
import openai
from config import Config

class AIAgent:
    """AI Agent class that integrates Claude and GPT models"""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the AI Agent with configuration"""
        self.config = config or Config()
        self.current_model = self.config.default_model
        
        # Initialize clients
        self._init_clients()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
    
    def _init_clients(self):
        """Initialize API clients for Claude and GPT"""
        # Initialize Anthropic client for Claude
        self.anthropic_client = anthropic.Anthropic(
            api_key=self.config.anthropic_api_key
        )
        
        # Initialize OpenAI client for GPT
        self.openai_client = openai.OpenAI(
            api_key=self.config.openai_api_key
        )
    
    def set_model(self, model_type: str):
        """Switch between Claude and GPT models"""
        if model_type.lower() not in ['claude', 'gpt']:
            raise ValueError(f"Unsupported model type: {model_type}. Use 'claude' or 'gpt'")
        
        self.current_model = model_type.lower()
        print(f"Switched to {self.current_model.upper()} model")
    
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.current_model
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _generate_claude_response(self, message: str) -> str:
        """Generate response using Claude model"""
        try:
            # Prepare messages for Claude
            messages = []
            for msg in self.conversation_history:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            # Add current message
            messages.append({
                'role': 'user',
                'content': message
            })
            
            # Generate response
            response = self.anthropic_client.messages.create(
                model=self.config.claude_model,
                max_tokens=1000,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error generating Claude response: {str(e)}"
    
    def _generate_gpt_response(self, message: str) -> str:
        """Generate response using GPT model"""
        try:
            # Prepare messages for GPT
            messages = []
            for msg in self.conversation_history:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            # Add current message
            messages.append({
                'role': 'user',
                'content': message
            })
            
            # Generate response
            response = self.openai_client.chat.completions.create(
                model=self.config.gpt_model,
                messages=messages,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating GPT response: {str(e)}"
    
    def generate_response(self, message: str, model_override: Optional[str] = None) -> str:
        """Generate response using the current or specified model"""
        # Determine which model to use
        model_to_use = model_override.lower() if model_override else self.current_model
        
        # Add user message to history
        self.add_to_history('user', message)
        
        # Generate response based on model
        if model_to_use == 'claude':
            response = self._generate_claude_response(message)
        elif model_to_use == 'gpt':
            response = self._generate_gpt_response(message)
        else:
            response = f"Error: Unsupported model '{model_to_use}'. Use 'claude' or 'gpt'"
        
        # Add assistant response to history
        if not response.startswith("Error"):
            self.add_to_history('assistant', response)
        
        return response
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return ['claude', 'gpt']
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model configuration"""
        return {
            'current_model': self.current_model,
            'claude_model': self.config.claude_model,
            'gpt_model': self.config.gpt_model,
            'available_models': self.get_available_models(),
            'conversation_length': len(self.conversation_history)
        }
