@startuml
actor Player
actor AI
actor System

Player --> (Sign Up / Log In)
Player --> (Create Court Case)
Player --> (Submit Initial Defense)
Player --> (Answer Judges' Questions)
Player --> (View Confidence Meter)
Player --> (Observe Deliberation)
Player --> (Receive Final Verdict)
Player --> (View Previous Cases)
Player --> (Update Account Details)
Player --> (Save Game Progress)

(Create Court Case) ..> (Generate Player Appearance) : <<include>>
(Create Court Case) ..> (Generate Judge Personalities) : <<include>>
(Submit Initial Defense) ..> (Calculate Initial Confidence) : <<include>>
(Answer Judges' Questions) ..> (Update Confidence Meter) : <<include>>
(Observe Deliberation) ..> (Simulate Judge Conversations) : <<include>>
(Receive Final Verdict) ..> (Generate Verdict) : <<include>>

AI --> (Generate Player Appearance)
AI --> (Generate Judge Personalities)
AI --> (Simulate Judge Conversations)
AI --> (Generate Verdict)

System --> (Save Case Progress)
System --> (Load Previous Cases)
System --> (Validate User Credentials)
System --> (Update Account Details) : "Sync Player Data"
System --> (Save Game Progress) : "Store Progress in DB"
System --> (Sign Up / Log In) : "Validate Credentials"
@enduml
