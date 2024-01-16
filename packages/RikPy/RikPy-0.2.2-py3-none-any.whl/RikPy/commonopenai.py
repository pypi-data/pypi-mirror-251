from openai import OpenAI
from dotenv import load_dotenv
import os


          
def generate_response(prompt, openai_key):
    
    # Executes the prompt and returns the response without parsing
    print ("Warming Up the Wisdom Workshop!")
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=openai_key  # Replace with your actual API key
    )

    print ("Assembling Words of Wisdom!")
    details_response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,  # Your prompt goes here
            }
        ],
        model="gpt-3.5-turbo"
    )
    
    return details_response

def generate_image(image_prompt, number_images, openai_key):
    
    # Executes the prompt and returns the response without parsing
    
    print ("Sparking the Synapses of Silicon!")
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=openai_key  # Replace with your actual API key
    )
    print("Summoning Pixels from the Digital Depths!")
    
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        n=number_images,
        size="1024x1024"
    )
    
    return image_response