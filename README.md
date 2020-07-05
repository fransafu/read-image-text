# read-image-text

# Getting started

Install the dependencies:
* `pip install -r requirements.txt`

Run the project with the follow command line (I recommend use to `virtualenv` for run in local).

* `python app.py`

# Test the project
Test the local project with the follow request:

```
curl --location --request POST 'http://0.0.0.0:8080/graphql' \
--header 'Content-Type: application/json' \
--data-raw '{"query":"{ image(url: \"https://www.google.cl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png\") { text }}"}'
```

**The model is base on the following project:** [click here](https://github.com/kurapan/CRNN)
