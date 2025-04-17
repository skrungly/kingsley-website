# personal website

just a small personal flask site, made for fun!

### setup

for production, first install `docker` and `docker-compose`. the following
command will start the server via gunicorn on a docker network called `proxy`:

```bash
$ docker-compose up -d
```

note that by default, the service doesn't publish the port because it is
intended to share the `proxy` network with a reverse proxy like nginx running
in a different container. to run a development server instead, simply do:

```bash
$ docker build -t "kingsley-website" .
$ docker run -it "kingsley-website" flask run --debug
```

the flask debug server should then display the address, something like:

```
 * Running on http://172.17.0.2:5000
```
