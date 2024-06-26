import requests

def get_json():
    url = "http://localhost:8000/export/json"
    response = requests.get(url)
    return response

def get_csv():
    url = "http://localhost:8000/export/csv"
    response = requests.get(url)
    return response

class TestExport():
    def test_json(self):
        response = get_json()
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

    def test_csv(self):
        response = get_csv()
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'

