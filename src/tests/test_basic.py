import requests

def test_get_basic_html_page():
    name = "test"
    response = requests.get("http://localhost:8000/" + name)
    assert response.status_code == 200
    text = response.text
    assert f"<h1>Hello <span>{name}</span></h1>" in text
    pass

