# test_app.py
from fastapi.testclient import TestClient
from app import main_app

client = TestClient(main_app)

text_input = """
    The ideal company should be a leader in the technology sector, specifically in artificial intelligence and machine learning. 
    It should have a strong commitment to sustainability and ethical practices. 
    The company should be medium-sized, with a global reach and a diverse team.
"""

def test_process_text():
    response = client.post("/clients", json={"text": text_input})
    assert response.status_code == 200
    # Aquí asumimos que tu respuesta incluirá "companies_db", "selected_companies", "employees_db", "selected_employees"
    assert "companies_db" in response.json()
    assert "selected_companies" in response.json()
    assert "employees_db" in response.json()
    assert "selected_employees" in response.json()

if __name__ == "__main__":
    test_process_text()