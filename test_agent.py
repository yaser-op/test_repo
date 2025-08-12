#!/usr/bin/env python3
"""
Test script to validate agent.py implementation
"""
import os
import sys

# Set dummy API keys for testing
os.environ['ANTHROPIC_API_KEY'] = 'test-anthropic-key'
os.environ['OPENAI_API_KEY'] = 'test-openai-key'

# Test import
try:
    from agent import AIAgent
    from config import Config
    print("✅ AIAgent class imported successfully")
except ImportError as e:
    print(f"❌ Failed to import AIAgent: {e}")
    sys.exit(1)

# Test agent initialization
print("\n🧪 Testing agent initialization...")
try:
    config = Config()
    agent = AIAgent(config)
    print("✅ Agent initialized successfully")
    print(f"✅ Default model: {agent.get_current_model()}")
except Exception as e:
    print(f"❌ Error during agent initialization: {e}")

# Test model selection
print("\n🧪 Testing model selection...")
try:
    # Test switching to Claude
    agent.set_model('claude')
    assert agent.get_current_model() == 'claude'
    print("✅ Successfully switched to Claude")
    
    # Test switching to GPT
    agent.set_model('gpt')
    assert agent.get_current_model() == 'gpt'
    print("✅ Successfully switched to GPT")
    
    # Test invalid model
    try:
        agent.set_model('gemini')
        print("❌ Should have failed for unsupported model")
    except ValueError as e:
        print(f"✅ Unsupported model validation working: {e}")
        
except Exception as e:
    print(f"❌ Error during model selection test: {e}")

# Test conversation history management
print("\n🧪 Testing conversation history...")
try:
    agent.clear_history()
    assert len(agent.conversation_history) == 0
    print("✅ History cleared successfully")
    
    agent.add_to_history('user', 'Hello')
    agent.add_to_history('assistant', 'Hi there!')
    assert len(agent.conversation_history) == 2
    print("✅ Messages added to history successfully")
    
    agent.clear_history()
    assert len(agent.conversation_history) == 0
    print("✅ History management working correctly")
    
except Exception as e:
    print(f"❌ Error during history test: {e}")

# Test model info
print("\n🧪 Testing model info...")
try:
    info = agent.get_model_info()
    required_keys = ['current_model', 'claude_model', 'gpt_model', 'available_models', 'conversation_length']
    
    for key in required_keys:
        assert key in info
        print(f"✅ Model info contains {key}: {info[key]}")
    
    available_models = agent.get_available_models()
    assert 'claude' in available_models
    assert 'gpt' in available_models
    assert 'gemini' not in available_models
    print("✅ Available models correct (excludes Gemini)")
    
except Exception as e:
    print(f"❌ Error during model info test: {e}")

# Test response generation structure (without actual API calls)
print("\n🧪 Testing response generation structure...")
try:
    # This will fail due to invalid API keys, but we can test the structure
    agent.clear_history()
    
    # Test that the method exists and handles errors gracefully
    response = agent.generate_response("Hello", model_override='claude')
    assert isinstance(response, str)
    print("✅ Claude response generation method works (returns error message as expected)")
    
    response = agent.generate_response("Hello", model_override='gpt')
    assert isinstance(response, str)
    print("✅ GPT response generation method works (returns error message as expected)")
    
    # Test invalid model override
    response = agent.generate_response("Hello", model_override='gemini')
    assert "Unsupported model" in response
    print("✅ Invalid model override handled correctly")
    
except Exception as e:
    print(f"❌ Error during response generation test: {e}")

print("\n🎉 AI Agent implementation tests completed!")
print("Note: API response tests show error messages due to test API keys, which is expected behavior.")
