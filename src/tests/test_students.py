import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture
def student_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "grades": [
            {"course": "math", "score": 90},
            {"course": "science", "score": 85},
            {"course": "history", "score": 95}
        ]
    }

def create_admin():
    body = {
        "username": "admin_for_test",
        "password": "password_admin_for_test"
    }
    try:
        response = requests.post(f"{BASE_URL}/user/", json=body)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            response = requests.post(f"{BASE_URL}/user/login", json=body)
            response.raise_for_status()
        else:
            raise e
    return response.json()

def create_student(student_data):
    bearer = student_data['bearer']

    print(bearer)
    headers = {
        "Authorization": f"Bearer {bearer}"
    }
    response = requests.post(f"{BASE_URL}/student/", json=student_data, headers=headers)
    response.raise_for_status()
    return response.json()

def get_student(identifier):
    response = requests.get(f"{BASE_URL}/student/{identifier}")
    response.raise_for_status()
    return response.json()

def delete_student(identifier):
    response = requests.delete(f"{BASE_URL}/student/{identifier}")
    return response.status_code

def get_one_grade_from_one_student(student_identifier, grade_identifier):
    response = requests.get(f"{BASE_URL}/student/{student_identifier}/grades/{grade_identifier}")
    response.raise_for_status()
    return response.json()

def delete_one_grade_from_one_student(student_identifier, grade_identifier):
    response = requests.delete(f"{BASE_URL}/student/{student_identifier}/grades/{grade_identifier}")
    response.raise_for_status()
    return response.status_code

class TestStudentManagement:

    def test_create_get_delete_student_with_multiple_grades(self, student_data):

        admin = create_admin()

        access_token = admin["access_token"]
        token_type = admin["token_type"]

        student_data['bearer'] = f'{token_type} {access_token}'
        
        # Créer un étudiant
        identifier = create_student(student_data)
        
        # Récupérer les données de l'étudiant
        student = get_student(identifier)

        # Vérifier que les données de l'étudiant sont correctes
        assert student["first_name"] == student_data["first_name"]
        assert student["last_name"] == student_data["last_name"]
        assert student["email"] == student_data["email"]
        assert len(student["grades"]) == len(student_data["grades"])

        for i, grade in enumerate(student_data["grades"]):
            assert student["grades"][i]["course"] == grade["course"]
            assert student["grades"][i]["score"] == grade["score"]

        # Regarder une note de l'étudiant
        grade_id = student["grades"][0]["id"]
        grade = get_one_grade_from_one_student(identifier, grade_id)
        assert grade["course"] == student["grades"][0]["course"]
        
        # Supprimer une note de l'étudiant
        assert delete_one_grade_from_one_student(identifier, grade_id) == 200
        
        # On supprime l'étudiant que l'on vient de créer
        assert delete_student(identifier) == 200
        # Comme on a supprimé l'étudiant, on ne doit pas pouvoir le récupérer
        assert delete_student(identifier) == 404
        pass

if __name__ == "__main__":
    pytest.main()
