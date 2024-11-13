@startuml

class User{
    + Username : string
    + Password : string
    + CourtCases : List<CourtCase>
}

class UserManager {
    + User : User
    + LoadUserData(username : string, password : string) : bool // sign in or sign up
    + SaveUser() : bool
    + LogOut() : bool
}

class Judges {
    - judges : List<Judge> //or GameObject
    + Confidence : float
    + ShowResponse(response : string) : void
    + EvaluateConvictResponse(response : string) : void
    + AskQuestion(judge : Judge)
}

class ConfidenceMeter {
    + UpdateConfidence() : void
}

interface IScreen {
    + Show() : void
    + Hide() : void
}

class UserSignInScreen {
    + Show() : void
    + Hide() : void
    + EvaluateInput() : void
}

class PreviousCasesScreen {
    + Show() : void
    + Hide() : void
    + LoadPreviousCase(case : CourtCase) : void
}

class StartingScreen {
    + Show() : void
    + Hide() : void
}

class Character {
    + SetupCharacter() : void
}

class ResponseScreen{
    + Show() : void
    + Hide() : void
    + SendResponse() : void
}

class GameFlowManager {
    + SetupScene() : void
    + StartGame() : void
    + EndGame() : void
    + SaveGame() : void
}

class PreviousCases {
    - previousCases : List<CourtCase>
    + LoadCases() : void
    + ReplayCase(case : CourtCase) : void
}

class CourtCase{
    + timestamp : DateTime
    + flow : List<string> // for now, may change later.
}

class CourtCasePlayer{
    + PlayCourtCase(case : CourtCase)
}

class APIHandler {
    // placeholder
    + SendRequest(endpoint : string, data : string) : void
    + GetResponse() : String
}

UserManager --> User : manages
UserManager --> CourtCase : loads & saves
Judges --> ConfidenceMeter : updates
Judges --> CourtCase : refers to
ConfidenceMeter --> Judges : modifies confidence
IScreen <|-- UserSignInScreen
IScreen <|-- PreviousCasesScreen
IScreen <|-- StartingScreen
IScreen <|-- ResponseScreen
UserSignInScreen --> UserManager : calls methods
PreviousCasesScreen --> PreviousCases : loads data
PreviousCases --> CourtCase : manages list of cases
GameFlowManager --> Judges : manages
GameFlowManager --> Character : sets up
GameFlowManager --> StartingScreen : opens
GameFlowManager --> PreviousCases : interacts
GameFlowManager --> ResponseScreen : opens
PreviousCases --> CourtCasePlayer : interacts with
CourtCasePlayer --> CourtCase : replays
APIHandler --> GameFlowManager : communicates
APIHandler --> UserManager : sends data

@enduml
