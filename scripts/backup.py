#!/usr/bin/env python3
import logging
import os
import tarfile
from datetime import datetime
from pathlib import Path


BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "./backups"))
INCLUDE_PATHS = [
    "docker-compose.yml",
    "Dockerfile",
    "apps",
    "terraform",
    ".github",
    "scripts",
    "docs",
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main() -> int:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"config_backup_{timestamp}.tar.gz"

    logging.info("Gerando backup em %s", backup_file)

    with tarfile.open(backup_file, "w:gz") as tar:
        for item in INCLUDE_PATHS:
            path = Path(item)
            if path.exists():
                tar.add(path, arcname=path.name)
                logging.info("Adicionado ao backup: %s", path)
            else:
                logging.warning("Caminho não encontrado, ignorando: %s", path)

    logging.info("Backup finalizado com sucesso")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())