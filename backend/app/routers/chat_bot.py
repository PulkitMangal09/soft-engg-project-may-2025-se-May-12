from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def chat_bot(chat_history, session_type: str | None = None, image_bytes: bytes | None = None, image_mime: str | None = None):
    """Generate a bot reply from chat history, tailored by session type ('diet' or 'emotion').
    Optionally include an image (jpg/png) to provide visual context to the model.
    """
    # Format chat history for the prompt
    formatted_history = "\n".join(
        f"{msg.get('sender_type', 'user')}: {msg.get('message_content', '')}" for msg in chat_history
    )

    session_directives = ""
    if session_type == "diet":
        session_directives = (
            "Focus on nutrition tips, balanced meals, allergies, sodium/sugar guidance, and hydration. "
            "When appropriate, suggest healthier alternatives and portion control."
        )
    elif session_type == "emotion":
        session_directives = (
            "Focus on empathetic, supportive tone. Offer coping strategies, breathing exercises, and resources. "
            "Avoid diagnosing. Encourage seeking help if severe distress is indicated."
        )
    else:
        session_directives = (
            "Provide friendly, helpful guidance based on the user's message."
        )

    prompt_text = f"""
    You are MyWellBeingBot, a friendly AI assistant.
    Session type: {session_type or 'general'}
    Guidance: {session_directives}

    Conversation so far:
    {formatted_history}

    Respond rules:
      • Reference the user's last message.
      • Keep responses concise (2–4 sentences) unless the user asks for more detail.
      • Use a conversational, warm tone.
      • Never reveal internal metadata (session_id, user_id, etc.).
      • Never reply to or discuss any NSFW or inappropriate content as this conversation is with a child—if such content arises, respond with a gentle reminder about safe and appropriate topics. 
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
        # Build contents: text plus optional inline image
        contents = []
        # main user/system prompt text
        contents.append({"role": "user", "parts": [{"text": prompt_text}]})
        # attach image if present
        if image_bytes and image_mime in ("image/jpeg", "image/jpg", "image/png"):
            # Gemini accepts inline bytes via 'inline_data'
            contents[-1]["parts"].append({
                "inline_data": {
                    "mime_type": image_mime,
                    "data": image_bytes
                }
            })

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema
            }
        )
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
        print(
            f"Raw response: {response.text if 'response' in locals() else 'No response'}")
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
