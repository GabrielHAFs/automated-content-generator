import json
import sys
import time

def article_generation(
        client, 
        system_prompt: str, 
        user_prompt: str, 
        model: str = "gpt-4o"):
    """
    Generates an article using a language model with a structured JSON schema output.

    Args:
        client: The OpenAI API client instance.
        system_prompt (str): The initial prompt given to the system to set the tone or context.
        user_prompt (str): The content or prompt provided by the user, typically a string generated from a DataFrame or similar source.
        model (str): The model to use for generating the completion. Default is 'llama3-70b-8192'.

    Returns:
        str: The structured JSON content of the generated article.
    """
    print("Generating your article\n", end="")
    
    for _ in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.5)
    print(" Please wait...")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "article_response",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "article_title": {"type": "string"},
                            "sections": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "headline": {"type": "string"},
                                        "body": {"type": "string"}
                                    },
                                    "required": ["headline", "body"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["article_title", "sections"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return json.loads(response.choices[0].message.content)

def image_captioning(
        client, 
        base64_image, 
        model: str = "llava-v1.5-7b-4096-preview"):
    """
    Generates an image caption using a multimodal vision model.

    Args:
        client: The OpenAI API client instance.
        base64_image: image encoded as base64.
        model (str): The model to use for generating the completion.

    Returns:
        str: The image caption
    """
    print("Generating your image caption\n", end="")
    
    for _ in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.5)
    print(" Please wait...")

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """You are a helpful assistant. Your objective is to provide a 100 words caption to the image. Be clear and objective. Your tone and language-level must be adequate for high-school studentes who want to learn and understand about the image.
                        """},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=model,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return {
        "caption": response.choices[0].message.content
    }