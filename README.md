# read-image-text

The project is an example of implementation of a simple GraphQL API with an artificial intelligence model; The model is owned by the GitHub user kurapan and you can check the repository [click here](https://github.com/kurapan/CRNN).

The main idea is to make a simple request with the URL of an image, the backend downloads the image and tries to read, and the result is solved by the tartiflette library.

# Getting started

Install the dependencies:
* `pip install -r requirements.txt`

Run the project with the follow command line (I recommend use to `virtualenv` for run in local).

* `python app.py`

# Test the project
Test the local project with the follow request:

```
curl --location --request POST 'http://localhost:8080/graphql' \
--header 'Content-Type: application/json' \
--data-raw '{"query":"{ image(url: \"https://www.google.cl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png\") { text }}"}'
```
