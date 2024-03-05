FROM --platform=linux/amd64 python:latest

WORKDIR /usr/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
