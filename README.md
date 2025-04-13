# personal website

just a small personal flask site, made for fun!

### setup

deployment with docker is planned but not yet implemented. in the meantime,
launching the development server is as easy as:

```bash
# with python and sass already installed:
$ sass app/static/style/style.scss app/static/style/style.css
$ pip -r requirements.txt
$ python -m flask run --debug
```
