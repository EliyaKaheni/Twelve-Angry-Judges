from GPT import prompt

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
    def login(username:str, password:str) -> bool:
        pass

    def store_court_case(court_case:CourtRoom) -> bool:
        pass

    def store_user(username:str, password:str) -> bool:
        pass

    def get_recent_cases(username:str) -> dict:
        pass