"""
Main application for AI Agent
Demonstrates functionality with Claude and GPT models
"""
from agent import AIAgent
from config import Config
import sys

def print_separator():
    """Print a visual separator"""
    print("-" * 60)

def display_model_info(agent: AIAgent):
    """Display current model information"""
    info = agent.get_model_info()
    print(f"Current Model: {info['current_model'].upper()}")
    print(f"Claude Model: {info['claude_model']}")
    print(f"GPT Model: {info['gpt_model']}")
    print(f"Conversation Length: {info['conversation_length']} messages")

def interactive_mode(agent: AIAgent):
    """Run interactive conversation mode"""
    print("🤖 AI Agent Interactive Mode")
    print("Commands:")
    print("  /switch claude - Switch to Claude model")
    print("  /switch gpt - Switch to GPT model")
    print("  /info - Show model information")
    print("  /clear - Clear conversation history")
    print("  /quit - Exit the program")
    print_separator()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input[1:].lower()
                
                if command == 'quit':
                    print("Goodbye! 👋")
                    break
                elif command.startswith('switch '):
                    model = command.split(' ', 1)[1]
                    try:
                        agent.set_model(model)
                    except ValueError as e:
                        print(f"Error: {e}")
                elif command == 'info':
                    display_model_info(agent)
                elif command == 'clear':
                    agent.clear_history()
                    print("Conversation history cleared.")
                else:
                    print("Unknown command. Type /quit to exit.")
                continue
            
            # Generate response
            print(f"\n{agent.get_current_model().upper()}: ", end="")
            response = agent.generate_response(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

def demo_mode(agent: AIAgent):
    """Run demonstration mode with example conversations"""
    print("🚀 AI Agent Demo Mode")
    print_separator()
    
    # Demo questions
    demo_questions = [
        "Hello! Can you introduce yourself?",
        "What's the weather like today?",
        "Can you help me write a Python function to calculate fibonacci numbers?"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\nDemo Question {i}: {question}")
        print_separator()
        
        # Test with Claude
        print("🔵 Claude Response:")
        claude_response = agent.generate_response(question, model_override='claude')
        print(claude_response)
        
        print("\n🟢 GPT Response:")
        gpt_response = agent.generate_response(question, model_override='gpt')
        print(gpt_response)
        
        print_separator()
        
        # Clear history between questions for fair comparison
        agent.clear_history()

def main():
    """Main application entry point"""
    print("🤖 AI Agent - Claude & GPT Integration")
    print("Gemini is excluded as per requirements")
    print_separator()
    
    try:
        # Initialize configuration and agent
        config = Config()
        agent = AIAgent(config)
        
        print("✅ AI Agent initialized successfully!")
        display_model_info(agent)
        print_separator()
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == '--demo':
            demo_mode(agent)
        else:
            interactive_mode(agent)
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure you have set up your environment variables:")
        print("- ANTHROPIC_API_KEY")
        print("- OPENAI_API_KEY")
        print("\nSee .env.example for reference.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
