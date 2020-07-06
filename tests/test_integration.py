import json
import multiprocessing
import pytest
import requests
import time

from app import run


@pytest.fixture(autouse=True, scope="session")
def start_app():
    p = multiprocessing.Process(target=run)
    p.start()
    # Wait for start app
    time.sleep(4)
    yield
    p.terminate()


@pytest.fixture
def base_url():
    return "http://localhost:8080/graphql"


def test_sucessful_read_text_from_google_image(base_url):
    body = {
        "query": "{ image(url: \"https://www.google.cl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png\") { text }}"
    }
    resp = requests.post(base_url, data=json.dumps(body), headers={
                         'Content-Type': 'application/json'})
    resp_content = json.loads(resp.text)
    assert resp_content is not None, "The content can't be empty"
    assert resp_content['data']['image']['text'] == "google"
