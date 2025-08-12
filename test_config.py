#!/usr/bin/env python3
"""
Test script to validate config.py implementation
"""
import os
import sys

# Test import
try:
    from config import Config
    print("✅ Config class imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Config: {e}")
    sys.exit(1)

# Test configuration without API keys (should raise ValueError)
print("\n🧪 Testing configuration validation...")
try:
    # Clear any existing API keys for this test
    original_anthropic = os.environ.get('ANTHROPIC_API_KEY')
    original_openai = os.environ.get('OPENAI_API_KEY')
    
    # Remove API keys temporarily
    if 'ANTHROPIC_API_KEY' in os.environ:
        del os.environ['ANTHROPIC_API_KEY']
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        config = Config()
        print("❌ Configuration should have failed without API keys")
    except ValueError as e:
        print(f"✅ Configuration validation working: {e}")
    
    # Restore original values
    if original_anthropic:
        os.environ['ANTHROPIC_API_KEY'] = original_anthropic
    if original_openai:
        os.environ['OPENAI_API_KEY'] = original_openai
        
except Exception as e:
    print(f"❌ Error during validation test: {e}")

# Test model configuration methods
print("\n🧪 Testing model configuration methods...")
try:
    # Set dummy API keys for testing
    os.environ['ANTHROPIC_API_KEY'] = 'test-anthropic-key'
    os.environ['OPENAI_API_KEY'] = 'test-openai-key'
    
    config = Config()
    
    # Test Claude configuration
    claude_config = config.get_model_config('claude')
    print(f"✅ Claude config: {claude_config}")
    
    # Test GPT configuration
    gpt_config = config.get_model_config('gpt')
    print(f"✅ GPT config: {gpt_config}")
    
    # Test invalid model type
    try:
        invalid_config = config.get_model_config('gemini')
        print("❌ Should have failed for unsupported model")
    except ValueError as e:
        print(f"✅ Unsupported model validation working: {e}")
        
except Exception as e:
    print(f"❌ Error during model config test: {e}")

print("\n🎉 Configuration management tests completed!")
