FROM python:3.12-slim

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
