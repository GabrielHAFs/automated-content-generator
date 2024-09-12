# Automated Content Generation Tool - main script
import os
import pandas as pd
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from src.core.prompts import prompts
from src.core.chat_completions import article_generation, image_captioning
from groq import Groq
import base64
from dotenv import load_dotenv
import argparse

_ = load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client_openai = OpenAI(
    api_key=OPENAI_API_KEY,
)
client_groq = Groq(
    api_key=GROQ_API_KEY,
)

def validate_file_type(file_path, expected_extensions):
    return file_path.lower().endswith(expected_extensions)

def validate_image_size(image_path, max_size_mb=20):
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    return file_size_mb <= max_size_mb

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description="Automated Content Generation Tool")
    
    parser.add_argument('-m', '--mode', choices=['article_gen', 'image_caption'], required=True,
                        help="Mode of operation: 'article_gen' to generate articles, 'image_caption' to generate captions for images.")
    
    parser.add_argument('-k', '--keywords-file', type=str, help="Path to the keywords CSV file (required for article generation mode).")
    parser.add_argument('-i', '--image', type=str, help="Path to the image file (required for image captioning mode).")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output JSON file.")

    args = parser.parse_args()

    if args.mode == 'article_gen':
        if not args.keywords_file or not validate_file_type(args.keywords_file, '.csv'):
            print("Error: You must provide a valid CSV file for article generation.")
            sys.exit(1)
        if not validate_file_type(args.output, '.json'):
            print("Error: Output file must be a JSON file.")
            sys.exit(1)

        # Load the CSV file
        df = pd.read_csv(args.keywords_file)
        
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
        print(f"\n{article_cot}\n")
        
        # Save the generated article to a JSON file
        if article_cot:
            with open(args.output, 'w') as file:
                json.dump(article_cot, file, indent=2)
            print(f"\nArticle saved to {args.output}")
        else:
            print("\nFailed to generate article.")

    elif args.mode == 'image_caption':
        if not args.image or not validate_file_type(args.image, ('.jpeg', '.jpg', '.png')):
            print("Error: You must provide a valid image file (jpeg, jpg, png) for image captioning.")
            sys.exit(1)
        if not validate_image_size(args.image):
            print("Error: Image file size must be under 20MB.")
            sys.exit(1)
        if not validate_file_type(args.output, '.json'):
            print("Error: Output file must be a JSON file.")
            sys.exit(1)

        # Generate image caption
        encoded_image = encode_image(args.image)

        caption = image_captioning(client_groq, encoded_image)
        print(caption)
        
        # Save the caption to a JSON file
        if caption:
            with open(args.output, 'w') as file:
                json.dump(caption, file, indent=2)
            print(f"Caption saved to {args.output}")
        else:
            print("Failed to generate image caption.")

if __name__ == "__main__":
    main()
