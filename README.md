# personal website

just a small personal flask site, made for fun!

## setup

you'll need to install `docker` to launch the server.

### for production

ensure that `docker-compose` is also installed. set up a cloudflare tunnel
with the desired configuration, and create a file called `.env` containing:

```bash
TUNNEL_TOKEN=<token here>
```

then deploy the server alongside nginx and gunicorn:

```bash
$ docker-compose up -d
```

### for development

to launch the flask server in debug mode:

```bash
$ docker build -t "kingsley-website" .
$ docker run -it "kingsley-website" flask run --debug
```

the flask server should then display the bound address, something like:

```
 * Running on http://172.17.0.2:5000
```
