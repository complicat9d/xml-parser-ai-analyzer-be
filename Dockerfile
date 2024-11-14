FROM python:3.12

WORKDIR /app
ENV DOCKER=1
ENV PYTHONPATH="/app"
RUN pip install --upgrade pip pipenv
COPY ./Pipfile* ./
RUN pipenv install --deploy --system --clear

COPY . .