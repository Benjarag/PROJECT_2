FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/MerchantService

COPY . .

EXPOSE 8001

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8001"]
