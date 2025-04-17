FROM python:3.13-alpine

RUN apk add --no-cache npm
RUN npm install -g sass

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/static/style app/static/style
RUN sass --style=compressed app/static/style/style.scss app/static/style/style.css

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
