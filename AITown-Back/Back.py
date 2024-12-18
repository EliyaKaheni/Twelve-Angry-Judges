from mysql.connector import Error
from typing import Optional, Dict
from GPT import pro
import mysql.connector

class UserManagement:
    def signup(username:str, password:str) -> bool:
        pass

    def signin(username:str, password:str) -> bool:
        pass


class CourtRoomConversations:
    def __init__(self):
        self.verdict_meter = 0.5
        self.conversationResult = {}

    def submit_initial_defence(defence_text:str) -> float:
        pass

    def generate_judge_question(personality: dict, defence_text:str, case_story:str) -> str:
        pass

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

    def generate_judge_personality() -> dict:
        pass

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
