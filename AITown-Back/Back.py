from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import Error
from typing import Optional, Dict
from GPT import prompt
import mysql.connector
import json

app = FastAPI()

# Pydantic models for request bodies
class SignupRequest(BaseModel):
    username: str
    password: str

class SigninRequest(BaseModel):
    username: str
    password: str

class DefenceSubmission(BaseModel):
    case_story: str
    defence_text: str

class JudgeQuestionRequest(BaseModel):
    judge_personality: str
    defence_text: str
    case_story: str

class AnswerSubmission(BaseModel):
    judge_personality: str
    verdict_meter: float
    question: str
    answer: str
    
class CaseCreationRequest(BaseModel):
    case_ID: str
    username: str
    description: str
    case_history: str

class FinalVerdict(BaseModel):
    verdict_meter: float
    case_story: str

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

    def submit_initial_defence(self, case_story, defence_text: str) -> float:
        try:
            prompt_text = f"""Read the case story and the defense provided. Based on the information given, return a float number between 0 and 1 that indicates how guilty the user is. 
- 0 means guilty.
- 1 means innocent.

Case Story: {case_story}
Defense: {defence_text}
JUST RETURN A FLOAT NUMBER BETWEEN 0 AND 1.
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
            response = prompt(prompt_text)
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"

    def generate_judge_question(self, judge_personality: str, defence_text: str, case_story: str) -> str:
        try:
            prompt_text = f"""Based on the case story and the judge's personality below, generate a question that the judge must ask the suspect.

Case Story: {case_story}  
Judge Personality: {judge_personality}
"""
            response = prompt(prompt_text)
            return response

        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"
        
    def process_answer(self, judge_personality: str, verdict_meter: float, question: str, answer: str) -> float:
        try:
            prompt_text = f"""Given the question: "{question}" and the answer: "{answer}" and the judge's personality: "{judge_personality}"
Return a float value between 0 and 1 to indicate the credibility of the answer. 
0 means the answer is completely unreliable, and 1 means the answer is fully credible.
the verdict meter is now {verdict_meter}. return me the new verdict meter value in a float number between 0 an 1. JUST A FLOAT NUMBER.
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
    
    def generate_final_verdict(self, verdict_meter, case_story) -> str:
        try:
            state = "Innocent"
            if verdict_meter > 0.5:
                state = "guilty"
            prompt_text = f"""Generate the final verdict for the case, based on the state and case story. state is {state}. case story: {case_story}"""
            response = prompt(prompt_text)
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            return "Couldn’t connect to GPT"


class CourtRoom:
    def __init__(self, case_ID, username, description, case_history):
        self.caseID = case_ID
        self.username = username
        self.description = description
        self.case_history = case_history
        self.judges_personality = []

    def save_case(self) -> bool:
        try:
            case_data = json.dumps({
                "caseID": self.caseID,
                "username": self.username,
                "description": self.description,
                "case_history": self.case_history
            }, ensure_ascii=False)

            dbm = DataBaseManager()
            return dbm.store_court_case(self.username, case_data)

        except Exception as e:
            print(f"Error saving case: {e}")
            return False

    @staticmethod
    def show_recent_cases(username: str) -> dict:
        dbm = DataBaseManager()
        case_record = dbm.get_recent_cases(username)

        if not case_record:
            return {"error": "No cases found"}

        try:
            case_data = case_record.get("conversations")
            return json.loads(case_data) if case_data else {"error": "Invalid case data"}

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
        self.host = 'aitown-proxysql-svc.hrzentz.svc'
        self.user = 'hamadmin'
        self.password = 'yffpykifTgsFASt43y4y'
        self.port = "3306"
        self.database = 'hamdb'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port="3306",
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
    verdict_meter = courtroom.submit_initial_defence(request.case_story, request.defence_text)
    return {"verdict_meter": verdict_meter}

@app.get("/generate_case_story")
def generate_case_story():
    courtroom = CourtRoomConversations()
    case_story = courtroom.generate_case_story()
    return {"case_story": case_story}

@app.post("/generate_judge_question")
def generate_judge_question(request: JudgeQuestionRequest):
    courtroom = CourtRoomConversations()
    question = courtroom.generate_judge_question(request.judge_personality, request.defence_text, request.case_story)
    return {"question": question}

@app.post("/process_answer")
def process_answer(request: AnswerSubmission):
    courtroom = CourtRoomConversations()
    credibility = courtroom.process_answer(request.judge_personality, request.verdict_meter, request.question, request.answer, {})
    return {"credibility": credibility}

@app.post("/create_case")
def create_case(request: CaseCreationRequest):
    courtroom = CourtRoom(request.case_ID, request.username, request.description, request.case_history)
    success = courtroom.save_case()
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
    credibility = courtroom.generate_final_verdict(request.verdict_meter, request.case_story)
    return {"credibility": credibility}

@app.get("/generate_judge_personality")
def generate_judge_personality():
    courtroom = CourtRoom("caseID", "username", "description", "case_history")
    personalities = courtroom.generate_judge_personality()
    return {"judge_personalities": personalities}
