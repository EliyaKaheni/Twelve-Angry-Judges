from openai import OpenAI
from openai import OpenAIError

def prompt(user_prompt, system_prompt=' '):
    try:
        client = OpenAI(
            api_key='KasiBeMaShakDare?',
            base_url = "http://localhost:1337/v1"
        )

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': "Set language is English. Don`t use any headings or additional signs.\n" + system_prompt},
                {'role':'user', 'content':user_prompt
                }
            ]
        )

        return response.choices[0].message.content
    
    except OpenAIError as e:
        return f'Error occured: {e}'
    