from openai import OpenAI
from openai import OpenAIError


system_prompt=f""""There is a game about a convict and some judges. The user enters the name of the case, convict's name, and the story of the case (what the case is about). Then the user, role-playing as the convict, is asked to submit a defense (first question every time) and then the defense is judged to grant the user an initial trust meter value (a float value from 0 to 1, 0 means not trusting the convict at all, and 1 means totally trusting the convict). Trust meter indicates how much the judges trust the convict's sayings. The more they trust the convict there is less chance of declaring the convict guilty, and giving them a punishment. After the first defense, each judge will ask a relevant question and judge the user's answer. There are different judges with different traits, and each trait may sway their opinions (judging the user's answer or asking a question). After the judging of the answer, the trust meter goes up or down slightly according to the validity of the answer provided and the judge's traits. After the quesioning has been done, the judges declare a verdict to pronounce the convict guilty or not. If they are pronounced guilty, the judges will provide a punishment as well that fits the crime.

The case info is provided below in the following format and some description of what each field means. I want you to satisfy my request below EXACTLY as I say.

Case Data: represents the current state of the case.
Case Name: the name of the case.
Convict Name: the name of the convict.
Story: what the case is about.
Questions: questions are listed as pairs: questions (from the judges) and corresponding answers (from the user).
Verdict: the final verdict of the judges, including whether the convict is guilty or not, and the suitable punishment.
Trust: the current trust meter value of the judges.
"""


def prompt(user_prompt, system_prompt=system_prompt):
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
    