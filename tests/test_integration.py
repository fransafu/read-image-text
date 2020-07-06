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


def test_try_read_text_from_google_chrome_logo(base_url):
    body = {
        "query": "{ image(url: \"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/64px-Google_Chrome_icon_%28September_2014%29.svg.png\") { text }}"
    }
    resp = requests.post(base_url, data=json.dumps(body), headers={
                         'Content-Type': 'application/json'})
    resp_content = json.loads(resp.text)
    assert resp_content is not None, "The content can't be empty"
    assert resp_content['data']['image']['text'] == "9"


def test_wrong_url_image(base_url):
    body = {
        "query": "{ image(url: \"https://www.example.cl/non-image\") { text }}"
    }
    resp = requests.post(base_url, data=json.dumps(body), headers={
                         'Content-Type': 'application/json'})
    resp_content = json.loads(resp.text)
    assert resp_content is not None, "The content can't be empty"
    assert resp_content['data']['image']['text'] == "Sorry. we can't download the image. Check the url and Try again"
