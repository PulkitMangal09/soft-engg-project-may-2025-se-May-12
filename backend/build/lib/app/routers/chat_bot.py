from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def chat_bot(chat_history):
    # Format chat history for the prompt
    formatted_history = "\n".join(
        f"{msg.get('sender_type', 'user')}: {msg.get('message_content', '')}" for msg in chat_history
    )
    
    prompt = f"""
    You are MyWellBeingBot, a friendly AI assistant that helps users with two kinds of sessions: 
  • Diet guidance ("diet" sessions)  
  • Emotion check‑ins ("emotion" sessions)  

Here is the conversation so far:
{formatted_history}

When you respond, always:
  • Reference the user's last message.  
  • Keep responses concise (2–4 sentences) unless the user asks for more detail.  
  • Use a conversational, warm tone.  
  • Never reveal the internal metadata (session_id, user_id, etc.) back to the user. 
  • Provide a helpful reply and optionally suggest an action.
  """
    
    # Define the response schema according to the official documentation
    response_schema = {
        "type": "object",
        "properties": {
            "reply": {
                "type": "string",
                "description": "The AI assistant's response to the user"
            },
            "suggested_action": {
                "type": "string",
                "description": "Optional suggested action",
                "enum": ["ask_more", "offer_tip", "recommend_break", "none"]
            }
        },
        "required": ["reply"],
        "propertyOrdering": ["reply", "suggested_action"]
    }
    
    try:
        # Generate content with structured output using the correct config format
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )
        print(prompt)
        # Parse and return the JSON response
        parsed_response = json.loads(response.text)
        
        # Ensure required fields are present
        if "reply" not in parsed_response:
            raise ValueError("Missing required field: reply")
            
        # Set default for optional field if not present
        if "suggested_action" not in parsed_response:
            parsed_response["suggested_action"] = "none"
            
        return parsed_response
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Raw response: {response.text if 'response' in locals() else 'No response'}")
        return {
            "reply": "I'm sorry, I encountered an error processing your request. Please try again.",
            "suggested_action": "none"
        }
    except ValueError as e:
        print(f"Validation error: {e}")
        return {
            "reply": "I'm sorry, I encountered an error processing your request. Please try again.",
            "suggested_action": "none"
        }
    except Exception as e:
        print(f"Unexpected error in chat_bot: {e}")
        return {
            "reply": "I'm sorry, I encountered an error processing your request. Please try again.",
            "suggested_action": "none"
        }