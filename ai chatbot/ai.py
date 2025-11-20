
import os
from google import genai
MODEL = 'gemini-2.5-flash'
try:
    client = genai.Client()
except Exception as e:
    print("Error initializing client. Make sure your GEMINI_API_KEY is set.")
    exit()


def chat_with_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()
if __name__ == "__main__":
   while True:
      user_input = input("You: ")
      if user_input.lower() in ["exit", "quit","bye"]:

         print("chatbot: Goodbye!")
         break
      
      response = chat_with_gemini(user_input)
      print("chatbot:", response)
             