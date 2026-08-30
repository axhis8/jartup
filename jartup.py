import subprocess
import argparse
import logging
import sys
from os.path import exists
from pathlib import Path


def setup_logger():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    logger = setup_logger()

    parser.add_argument("group", type=str, help="group name (example: 'com.name')")
    parser.add_argument("name", type=str, help="projekt name")
    parser.add_argument(
        "-g", "--git", default=False, action="store_true", help="initialize git"
    )
    parser.add_argument(
        "-d", "--docker", default=False, action="store_true", help="initialize docker"
    )
    parser.add_argument(
        "--force",
        default=False,
        action="store_true",
        help="forces project creation by overwriting file which has the same project name",
    )

    args = parser.parse_args()
    group_items: list[str] = args.group.split(".")
    if len(group_items) != 2:
        logger.error("Invalid group arguments!")
        sys.exit(1)

    # DIRS
    root = Path(args.name)
    if root.exists() and not args.force:
        logger.error(f"Project '{args.name}' already exists!")
        sys.exit(1)

    main_dir = (
        root / "src" / "main" / "java" / group_items[0] / group_items[1] / args.name
    )
    test_dir = (
        root / "src" / "test" / "java" / group_items[0] / group_items[1] / args.name
    )
    resources_dir = root / "src" / "main" / "resources"

    # FILES
    main_java_file = main_dir / "Main.java"
    gitignore_file = root / ".gitignore"
    dockerignore_file = root / ".dockerignore"
    dockerfile_file = root / "Dockerfile"
    docker_compose_file = root / "docker-compose.yml"
    pom_file = root / "pom.xml"
    readme_file = root / "README.md"

    # CREATE
    logger.info("Creating Directories and Files...")

    main_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    main_java_file.touch(exist_ok=True)
    pom_file.touch(exist_ok=True)

    if args.git:
        logger.info("Initializing Git...")
        subprocess.run(["git", "init"], cwd=root)
        gitignore_file.touch(exist_ok=True)
        readme_file.touch(exist_ok=True)

    if args.docker:
        logger.info("Setting up Docker...")
        dockerignore_file.touch(exist_ok=True)
        dockerfile_file.touch(exist_ok=True)
        docker_compose_file.touch(exist_ok=True)

    # WRITING IN FILES
    logger.info("Writing in Files...")


if __name__ == "__main__":
    main()
