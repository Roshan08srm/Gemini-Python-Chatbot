import os
from google import genai

MODEL = 'gemini-2.5-flash' 

def main():
    """
    Main function to run the chatbot with conversational memory.
    """
    try:
        client = genai.Client()
        
        chat = client.chats.create(model=MODEL)

        print("Chatbot is ready! Type 'exit', 'quit', or 'bye' to end the conversation.")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye!")
                break
            
            if not user_input.strip():
                continue

            try:
                response = chat.send_message(user_input)
                
                print("Chatbot:", response.text.strip())
            
            except Exception as e:
                print(f"Error sending message: {e}")
                
    except Exception as e:
        print(f"Error initializing model: {e}")
        print("Make sure your GEMINI_API_KEY is set correctly.")
        exit()

if __name__ == "__main__":
    main()