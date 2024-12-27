from mysql.connector import Error
from typing import Optional, Dict
from GPT import prompt
import mysql.connector

class UserManagement:
    def signup(username:str, password:str) -> bool:
        dbm = DataBaseManager()
        return dbm.store_user(username=username, password=password)

    def signin(username:str, password:str) -> bool:
        dbm = DataBaseManager()
        return dbm.login(username=username, password=password)


class CourtRoomConversations:
    def __init__(self):
        self.verdict_meter = 0.5
        self.case_story = ''
        self.conversationResult = {}

    def submit_initial_defence(self, defence_text:str) -> float:
        try:
            prompt_text = f"""Read the case story and the defense provided. Based on the information given, return a float number between 0 and 1 that indicates how guilty the user is. 
- 0 means guilty.
- 1 means innocent.

Case Story: {self.case_story}
Defense: {defence_text}
"""
            self.verdict_meter = prompt(prompt_text)
            return self.verdict_meter
        
        except:
            return 'Couldn`t connect to GPT'

    def generate_case_story() -> str:
        try:
            prompt_text = """Generate a concise and engaging 3-line case story for a fictional legal game. Each case story should include:  
1. **The Conflict**: The central legal issue or dispute (e.g., criminal, civil, corporate, or family law).  
2. **The Twist**: A surprising or challenging element that complicates the case and requires deeper investigation or decision-making.  
3. **The Stakes**: The consequences or broader implications of resolving the case correctly or incorrectly.  

Write One case story in Persian and a way that intrigues the player and provides clear gameplay objectives. Avoid specific references to judges or other characters.   """
            response = prompt(prompt_text)
            return response
        
        except:
            return 'Couldn`t connect to GPT'

    def generate_judge_question(self, judges_personalities: dict, judge_name: str, defence_text:str, case_story:str) -> str:
        try:
            judge_personality = judges_personalities[judge_name]
            prompt_text = f"""Based on the case story and the judge's personality below, generate a question that the judge must ask the suspect.

Case Story: {self.case_story}  
Judge Personality: {judge_personality}
"""
            response = prompt(prompt_text)
            return response

        except:
            return 'Couldn`t connect to GPT'
        
    def process_answer(question:str, answer:str) -> float:
        pass

    def simulate_judge_conversation() -> str:
        pass
    
    def generate_final_verdict() -> str:
        pass

    
class CourtRoom:
    def __init__(self, case_ID, username, description, case_history):
        self.caseID = case_ID
        self.username = username
        self.description = description
        self.case_history = case_history
        self.judges_personality = []
    
    def generate_player_appearance() -> dict:
        pass

    def generate_judge_personality(self) -> dict:
        try:
            prompt_text = """Generate 12 unique judge characters for a fictional game in JSON format. Each character should have the following attributes:
    1. **Name**: A distinct and realistic name.
    2. **Summary**: A short description of their personality, key traits, and judging style.

    Output the result as a properly formatted JSON array.
    Generate the summary in Persian"""
            
            self.judges_personality = prompt(prompt_text)
            return self.judges_personality
        
        except:
            return 'Couldn`t connect to GPT'


    def show_recent_cases(username:str) -> dict:
        pass

class DataBaseManager:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'Ekaheni82'
        self.database = 'aiTown'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
        
        except Error as e:
            print(f'Error occured in connecting to database: {e}')


    def close_connection(self):
        if self.connection:
            self.connection.close()


    def login(self, username:str, password:str) -> bool:
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            return user is not None
        
        except Error as e:
            print(f'Error occured during login: {e}')
            return False
        
        finally:
            self.close_connection()


    def store_court_case(self, court_case:CourtRoom) -> bool:
        query = '''INSERT INTO courtCaseRecord (sername, conversations)
        VALUES (%s, %s)'''
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, court_case.username, court_case.case_history)
            self.connection.commit()
            return True
        
        except Error as e:
            print(f'Error occured during storing court case: {e}')
            return False
        
        finally:
            self.close_connection()


    def store_user(self, username:str, password:str) -> bool:
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, (username, password))
            self.connection.commit()
            return True
        
        except Error as e:
            print(f'Error occured during storing court case: {e}')
            return False
        
        finally:
            self.close_connection()


    def get_recent_cases(self, username: str) -> Optional[Dict]:
        query = """SELECT * FROM courtCaseRecord 
        WHERE username = %s 
        ORDER BY created_at DESC
        LIMIT 10
        """
        try:
            self.connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (username,))
            cases = cursor.fetchall()
            return cases if cases else {}
        
        except Error as e:
            print(f"Error retrieving recent cases: {e}")
            return {}
        
        finally:
            self.close_connection()
