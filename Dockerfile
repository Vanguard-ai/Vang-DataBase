FROM python:3.12-slim

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv && \
    pipenv install --system --deploy && \
    pip uninstall pipenv -y

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
