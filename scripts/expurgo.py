#!/usr/bin/env python3
import logging
import subprocess
import sys
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# política de retenção (em horas)
IMAGE_RETENTION_HOURS = 24
CONTAINER_RETENTION_HOURS = 24


def run_command(command: list[str]) -> None:
    logging.info("Executando: %s", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    if result.stdout:
        logging.info(result.stdout.strip())
    if result.stderr:
        logging.warning(result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao executar {' '.join(command)}")


def expurgo_containers():
    logging.info("Removendo containers parados...")
    run_command(["docker", "container", "prune", "-f"])


def expurgo_images():
    logging.info("Removendo imagens antigas/dangling...")
    run_command(["docker", "image", "prune", "-a", "-f"])


def expurgo_networks():
    logging.info("Removendo networks não utilizadas...")
    run_command(["docker", "network", "prune", "-f"])


def expurgo_volumes():
    logging.info("Removendo volumes não utilizados...")
    run_command(["docker", "volume", "prune", "-f"])


def main() -> int:
    try:
        logging.info("Iniciando processo de expurgo...")

        expurgo_containers()
        expurgo_images()
        expurgo_networks()
        expurgo_volumes()

        logging.info("Expurgo finalizado com sucesso")
        return 0

    except Exception as exc:
        logging.error("Falha no expurgo: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())