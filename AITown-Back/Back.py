from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import Error
from typing import Optional, Dict
from GPT import prompt
import mysql.connector
import json

app = FastAPI()

class QuestionData:
    question: str
    answer: str

class CaseData:
    def __init__(self, case_name: str, convict_name: str, story: str, questions: list[QuestionData], verdict: str, trust: float):
        self.case_name = case_name
        self.convict_name = convict_name
        self.story = story
        self.questions = questions
        self.verdict = verdict
        self.trust = trust

    def __str__(self):
        case_str = f"Case Name: {self.case_name}\n\n"
        case_str += f"Convict Name: {self.convict_name}\n\n"
        case_str += f"Story: {self.story}\n\n"
        case_str += "Questions:\n"
        for i, question_data in enumerate(self.questions, start=1):
            case_str += f"Question {i}:\n{question_data.question}\n"
            case_str += f"Answer {i}:\n{question_data.answer}\n\n"
        case_str += f"Verdict: {self.verdict}\n\n"
        case_str += f"Trust: {self.trust}\n"
        return case_str

# Pydantic models for request bodies
class SignupRequest(BaseModel):
    username: str
    password: str

class SigninRequest(BaseModel):
    username: str
    password: str

class DefenceSubmission(BaseModel):
    case_data: CaseData
    judge_traits: str

class JudgeQuestionRequest(BaseModel):
    case_data: CaseData
    judge_traits: str

class AnswerSubmission(BaseModel):
    case_data: CaseData
    question_data: QuestionData
    judge_traits: str
    
class CaseCreationRequest(BaseModel):
    case_data: CaseData
    username: str

class FinalVerdict(BaseModel):
    case_data: CaseData

class UserManagement:
    @staticmethod
    def signup(username: str, password: str) -> bool:
        dbm = DataBaseManager()
        return dbm.store_user(username=username, password=password)

    @staticmethod
    def signin(username: str, password: str) -> bool:
        dbm = DataBaseManager()
        return dbm.login(username=username, password=password)


class CourtRoomConversations:
    def __init__(self):
        self.verdict_meter = 0.5
        self.case_story = ''
        self.conversationResult = {}

    def submit_initial_defence(self, case_data: CaseData, judge_traits: str) -> float:
        try:
            prompt_text = f"""Current case data:
{case_data}

Request:
The initial defense of the convict is provided as the first question and answer above, judge the answer from the point of view of a judge with traits '{judge_traits}' and provide only a float number between 0 and 1 for the initial trust meter value.
"""
            self.verdict_meter = float(prompt(prompt_text))
            return self.verdict_meter
        
        except Exception as e:
            print(f"Error: {e}")
            return 0.5  

    @staticmethod
    def generate_case_story() -> str:
        try:
            prompt_text = """Generate a concise and engaging 3-line case story for a fictional legal game. Each case story should include:  
1. **The Conflict**: The central legal issue or dispute (e.g., criminal, civil, corporate, or family law).  
2. **The Twist**: A surprising or challenging element that complicates the case and requires deeper investigation or decision-making.  
3. **The Stakes**: The consequences or broader implications of resolving the case correctly or incorrectly.  

Write one case story in a way that intrigues the player and provides clear gameplay objectives. Avoid specific references to judges or other characters."""
            response = prompt(prompt_text, ' ')
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"

    def generate_judge_question(self, case_data: CaseData, judge_traits: str) -> str:
        try:
            prompt_text = f"""Current case data:
{case_data}

Request:
The current case data is provided above. I need you to generate a new relevant question from the point of view of a judge with traits '{judge_traits}'. Provide only a question and nothing more.
"""
            response = prompt(prompt_text)
            return response

        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"
        
    def process_answer(self, case_data: CaseData, question_data: QuestionData, judge_traits: str) -> float:
        try:
            question = question_data.question
            answer = question_data.answer
            prompt_text = f"""Current case data:
{case_data}

Request:
The current case data is provided above. The current question and answer is listed below. I want you to judge the convict's answer from the point of view of a judge with traits '{judge_traits}', and provide only a new trust meter value from 0 to 1, according to the current trust value (provided above) and the validity of the answer and traits of the judge.
Question: {question}
Answer: {answer}

"""
            response = float(prompt(prompt_text))
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return 0.5  

    def simulate_judges_conversation(self) -> str:
        try:
            prompt_text = """Generate a simulated conversation between judges, where they discuss the case and provide a collective view on the verdict. 
Include personality clashes or differences of opinion between them."""
            response = prompt(prompt_text)
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"
    
    def generate_final_verdict(self, case_data) -> str:
        try:
            prompt_text = f"""Current case data:
{case_data}

Request:
The current case data is provided above, including all the questions and answers and the trust meter value. I want you to generate a verdict declaring whether the convict is guilty or not, and if they are, include the punishment as well. Provide only the final verdict and nothing more.
"""
            response = prompt(prompt_text)
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"


class CourtRoom:
    def save_case(self, case_data, username) -> bool:
        try:
            dbm = DataBaseManager()
            return dbm.store_court_case(username, case_data)

        except Exception as e:
            print(f"Error saving case: {e}")
            return False

    @staticmethod
    def show_recent_cases(username: str) -> dict:
        try:
            dbm = DataBaseManager()
            case_record = dbm.get_recent_cases(username)

            if not case_record:
                return []

            else:
                return [case_record]

        except Exception as e:
            print(f"Error retrieving case data: {e}")
            return {"error": "Could not retrieve case data"}

    # @staticmethod
    # def generate_player_appearance() -> dict:
    #     return {}

    def generate_judge_personality(self) -> dict:
        try:
            prompt_text = """Generate 12 unique judge characters for a fictional game in JSON format. Each character should have the following attributes:
1. **Name**: A distinct and realistic name.
2. **Summary**: A short description of their personality, key traits, and judging style.

Output the result as a properly formatted JSON array.
"""
            
            response = prompt(prompt_text)
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

class DataBaseManager:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'HShea@yazd82'
        self.database = 'aiTown'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f'Error connecting to database: {e}')

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def store_court_case(self, username: str, case_data: str) -> bool:
        """Stores the case data as a JSON string in the database."""
        query = '''INSERT INTO courtCaseRecord (username, conversations) VALUES (%s, %s)'''
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, (username, case_data))
            self.connection.commit()
            return True

        except Error as e:
            print(f'Error storing court case: {e}')
            return False

        finally:
            self.close_connection()

    def get_recent_cases(self, username: str) -> Optional[Dict]:
        """Fetches the most recent case from the database as a JSON object."""
        query = """SELECT conversations FROM courtCaseRecord 
                   WHERE username = %s 
                   ORDER BY created_at DESC 
                   LIMIT 1"""
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (username,))
            case_record = cursor.fetchone()
            return case_record if case_record else {}

        except Error as e:
            print(f"Error retrieving recent cases: {e}")
            return {}

        finally:
            self.close_connection()
    
    def login(self, username: str, password: str) -> bool:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            return user is not None
        except Error as e:
            print(f"Error occurred during login: {e}")
            return False
        finally:
            self.close_connection()

    def store_user(self, username: str, password: str) -> bool:
        """Registers a new user."""
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, (username, password))
            self.connection.commit()
            return True
        except Error as e:
            print(f'Error registering user: {e}')
            return False
        finally:
            self.close_connection()


@app.post("/signup")
def signup(request: SignupRequest):
    success = UserManagement.signup(request.username, request.password)
    if not success:
        raise HTTPException(status_code=400, detail="Signup failed")
    return {"message": "Signup successful"}

@app.post("/signin")
def signin(request: SigninRequest):
    success = UserManagement.signin(request.username, request.password)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Signin successful"}

@app.post("/submit_defence")
def submit_defence(request: DefenceSubmission):
    courtroom = CourtRoomConversations()
    verdict_meter = courtroom.submit_initial_defence(request.case_data, request.judge_traits)
    return {"verdict_meter": verdict_meter}

@app.get("/generate_case_story")
def generate_case_story():
    courtroom = CourtRoomConversations()
    case_story = courtroom.generate_case_story()
    return {"case_story": case_story}

@app.post("/generate_judge_question")
def generate_judge_question(request: JudgeQuestionRequest):
    courtroom = CourtRoomConversations()
    question = courtroom.generate_judge_question(request.case_data, request.judge_traits)
    return {"question": question}

@app.post("/process_answer")
def process_answer(request: AnswerSubmission):
    courtroom = CourtRoomConversations()
    credibility = courtroom.process_answer(request.case_data, request.question_data, request.judge_traits)
    return {"credibility": credibility}

@app.post("/create_case")
def create_case(request: CaseCreationRequest):
    courtroom = CourtRoom()
    success = courtroom.save_case(request.case_data, request.username)
    if not success:
        raise HTTPException(status_code=400, detail="Case creation failed")
    return {"message": "Case created successfully"}

@app.get("/recent_cases/{username}")
def get_recent_cases(username: str):
    cases = CourtRoom.show_recent_cases(username)
    return {"cases": cases}

@app.post("/final_verdict")
def process_answer(request: FinalVerdict):
    courtroom = CourtRoomConversations()
    credibility = courtroom.generate_final_verdict(request.case_data)
    return {"credibility": credibility}

@app.get("/generate_judge_personality")
def generate_judge_personality():
    courtroom = CourtRoom("caseID", "username", "description", "case_history")
    personalities = courtroom.generate_judge_personality()
    return {"judge_personalities": personalities}
