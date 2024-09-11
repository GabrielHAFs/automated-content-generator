# Automated Content Generation Tool - main script
import os
import pandas as pd
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from src.dataset.core.prompts import prompts

_ = load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client_openai = OpenAI(
    api_key=OPENAI_API_KEY,
)

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

def main(csv_path):
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Prepare the user prompt
    user_prompt = prompts["user_prompt"].format(
        main_keyword=df['Main Keyword'].iloc[0],
        sec_keywords=df['Secondary Keywords'].iloc[0]
    )
    
    # Generate the article using Chain of Thought (CoT) prompt
    article_cot = article_generation(
        client_openai, 
        system_prompt=prompts["cot_system_prompt"], 
        user_prompt=user_prompt, 
        model="gpt-4o-2024-08-06"
    )
    
    # Save the generated article to a JSON file
    if article_cot:
        output_file = 'output.json'
        with open(output_file, 'w') as file:
            json.dump(article_cot, file, indent=2)
        print(f"Article saved to {output_file}")
    else:
        print("Failed to generate article.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv>")
    else:
        csv_path = sys.argv[1]
        main(csv_path)
