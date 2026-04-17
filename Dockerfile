FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PORT=8000

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup  appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE ${PORT}

CMD ["sh","-c","exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]