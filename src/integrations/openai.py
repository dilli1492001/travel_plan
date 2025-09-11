

from openai import OpenAI
from fastapi.responses import JSONResponse
import json

openapi_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 
 
client = OpenAI(api_key=openapi_key)
 
 

def generate_plan(data):
    prompt = '''
    Your are a AI travel planer with 19 years of experience. 
    You are supposed to understand my apps user travel plan data and 
    generate a clean and simple travel plan accordingly to my user needs
    Dont wish like 'sure, i will generate etc..'
    Directly come to the point. I need only the plan.
    Keep reply under 100 words.
    '''
    response = client.responses.create(
            model="gpt-4.1",
            max_output_tokens=1000,
            temperature=0.7,
            input=[
                    {
                "role": "system",
                "content": prompt
                },
                {
                    "role": "user",
                    "content": f'Please generate a travel plan for me. Details are here: {data}'
                }
            ],
        )

    # data = json.loads(response.output_text)

    # data = json.loads(data)

    return response.output_text
