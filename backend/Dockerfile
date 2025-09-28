# Django + Gunicorn + Uvicorn Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start Gunicorn with Uvicorn workers
CMD ["gunicorn", "uzuri_university.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000"]
