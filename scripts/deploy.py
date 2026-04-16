#!/usr/bin/env python3
import logging
import subprocess
import sys
import time

import requests


COMPOSE_FILE = "docker-compose.yml"
HEALTH_URL = "http://localhost:8001/health"
HEALTH_TIMEOUT = 5
WAIT_SECONDS = 10

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_command(command: list[str]) -> None:
    logging.info("Executando comando: %s", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    if result.stdout:
        logging.info(result.stdout.strip())
    if result.stderr:
        logging.warning(result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(f"Falha ao executar comando: {' '.join(command)}")


def validate_health() -> None:
    logging.info("Validando health check em %s", HEALTH_URL)
    response = requests.get(HEALTH_URL, timeout=HEALTH_TIMEOUT)
    response.raise_for_status()
    logging.info("Aplicação validada com sucesso")


def main() -> int:
    try:
        run_command(["docker-compose", "-f", COMPOSE_FILE, "up", "--build", "-d"])
        logging.info("Aguardando containers estabilizarem...")
        time.sleep(WAIT_SECONDS)
        validate_health()
        logging.info("Deploy concluído com sucesso")
        return 0
    except Exception as exc:
        logging.error("Falha no deploy: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())