import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is in main.py

client = TestClient(app)

# Test user signup
def test_signup():
    response = client.post("/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signup successful"

# Test user signin
def test_signin():
    response = client.post("/signin", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signin successful"

# Test case creation
def test_create_case():
    response = client.post("/create_case", json={"case_data": "Sample Case Data", "username": "testuser"})
    assert response.status_code == 200
    assert response.json()["message"] == "Case created successfully"

# Test generating a case story
def test_generate_case_story():
    response = client.get("/generate_case_story")
    assert response.status_code == 200
    assert "case_story" in response.json()

# Test generating judge question
def test_generate_judge_question():
    response = client.post("/generate_judge_question", json={
        "case_data": {"case_name": "Test Case", "convict_name": "John Doe", "story": "Sample Story", "questions": [], "verdict": "", "trust": 0.5},
        "judge_traits": "Strict"
    })
    assert response.status_code == 200
    assert "question" in response.json()

# Test processing an answer
def test_process_answer():
    response = client.post("/process_answer", json={
        "case_data": {"case_name": "Test Case", "convict_name": "John Doe", "story": "Sample Story", "questions": [], "verdict": "", "trust": 0.5},
        "question_data": {"question": "Did you commit the crime?", "answer": "No"},
        "judge_traits": "Strict"
    })
    assert response.status_code == 200
    assert "credibility" in response.json()

# Test final verdict generation
def test_final_verdict():
    response = client.post("/final_verdict", json={
        "case_data": {"case_name": "Test Case", "convict_name": "John Doe", "story": "Sample Story", "questions": [], "verdict": "", "trust": 0.5}
    })
    assert response.status_code == 200
    assert "final_verdict" in response.json()

# Test retrieving recent cases
def test_get_recent_cases():
    response = client.get("/recent_cases/testuser")
    assert response.status_code == 200
    assert "cases" in response.json()

# Test resetting database
def test_reset_database():
    response = client.get("/reset_database")
    assert response.status_code == 200
    assert "message" in response.json()

# Test submitting defense
def test_submit_defence():
    response = client.post("/submit_defence", json={
        "case_data": {"case_name": "Test Case", "convict_name": "John Doe", "story": "Sample Story", "questions": [], "verdict": "", "trust": 0.5},
        "judge_traits": "Strict",
        "question_data": {"question": "Did you commit the crime?", "answer": "No"}
    })
    assert response.status_code == 200
    assert "credibility" in response.json()

# Test generating judge personality
def test_generate_judge_personality():
    response = client.get("/generate_judge_personality")
    assert response.status_code == 200
    assert "judge_personalities" in response.json()

if __name__ == "__main__":
    pytest.main()
