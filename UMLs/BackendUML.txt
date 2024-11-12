@startuml
class GameController {
    - courtRoom: CourtRoom
    - courtRoomConversations: CourtRoomConversations
    - userManagement: UserManagement
    ---
    ...
}

class CourtRoom {
    + caseId: str
    + description: str
    + username: str
    + caseHistory: JSON
    ---
    + generatePlayerAppearance(): JSON
    + generateJudgesPersonality(): JSON
    + getRecentCases(username: str): JSON
}

class CourtRoomConversations {
    + verdictMeter: float
    + conversationResult: JSON
    ---
    + submitInitialDefense(defenseText: str): float
    + generateJudgeQuestion(personality: JSON): str
    + processAnswer(answer: str): float
    + simulateJudgeConversation(): str
    + generateFinalVerdict(): str
}

class UserManagement {
    ---
    + signup(username: str, password: str): bool
    + signin(username: str, password: str): bool
}

class DatabaseManager {
    + login(username: str, password:str) bool
    + storeCourtCase(courtCase: CourtRoom): void
    + storeUser(username: str, password:str): void
    + getRecentCases(username: str): JSON
}

GameController *-- CourtRoom
GameController *-- CourtRoomConversations
GameController *-- UserManagement
CourtRoom ..> DatabaseManager : "interacts with"
UserManagement ..> DatabaseManager : "interacts with"
@enduml
