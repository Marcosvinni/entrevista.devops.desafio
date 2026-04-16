#!/usr/bin/env python3
import logging
import os
import sys
from datetime import datetime

import requests


API_URL = os.getenv("API_URL", "http://localhost:8001/health")
TIMEOUT = int(os.getenv("TIMEOUT", "5"))
ALERT_LOG = os.getenv("ALERT_LOG", "./scripts/alerts.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(ALERT_LOG, encoding="utf-8"),
    ],
)


def main() -> int:
    logging.info("Iniciando health check da API em %s", API_URL)

    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        response.raise_for_status()
        logging.info("API saudável | status=%s | body=%s", response.status_code, response.text)
        return 0
    except requests.RequestException as exc:
        logging.error("Falha no health check: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())