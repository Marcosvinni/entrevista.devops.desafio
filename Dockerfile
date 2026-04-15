FROM python:3.11-slim AS builder

WORKDIR /app

COPY apps/api/requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY apps/api/ .

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]