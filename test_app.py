from app import app


def test_api():
    client = app.test_client()
    response = client.get('/api')

    if response.status_code != 200:
        raise AssertionError("API did not return 200")

    if not response.is_json:
        raise AssertionError("API response is not JSON")