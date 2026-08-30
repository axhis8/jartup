#!/usr/bin/env python3

import subprocess
import argparse
import logging
import shutil
import sys
from pathlib import Path
from string import Template

CACHED_DIR_SUFFIX = "_cached"

logging.basicConfig(level=logging.INFO, format="[Jartup] %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def cache_old_dir(root: Path):
    logger.info("Backing up existing project...")
    cached_path = get_cached_path(root)

    if cached_path.exists():
        rollback(
            f"Path {cached_path} already exists! Rename the existing file to fix this issue.",
            root,
            False,
            False,
        )

    shutil.move(root, get_cached_path(root))


def get_cached_path(root: Path) -> Path:
    return Path(str(root) + CACHED_DIR_SUFFIX)


def validate_template(template_path: Path, filename: str) -> Path:
    file = template_path / filename
    if not file.exists():
        raise FileNotFoundError(
            f"Required template file {filename} is missing in {template_path}!"
        )

    return file


def render_template(template_path: Path, filename: str, context: dict[str, str]) -> str:
    file = validate_template(template_path, filename)
    template = Template(file.read_text(encoding="utf-8"))
    return template.substitute(context)


def rollback(
    error_msg: str, root: Path, old_dir_exists: bool, root_is_created: bool = True
):
    logger.error(error_msg)

    if root.exists() and root_is_created:
        logger.info(f"Cleaning up created Directory '{root}'...")
        shutil.rmtree(root)

    if old_dir_exists:
        logger.info("Restoring overwritten Directory...")
        shutil.move(get_cached_path(root), root)

    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()

    # ARGS
    parser.add_argument("group", type=str, help="group name (example: 'com.name')")
    parser.add_argument("name", type=str, help="project name")
    parser.add_argument(
        "-m", "--maven", default=False, action="store_true", help="set up maven build"
    )
    parser.add_argument(
        "-g", "--git", default=False, action="store_true", help="initialize git"
    )
    parser.add_argument(
        "-d",
        "--docker",
        default=False,
        action="store_true",
        help="initialize docker (also sets up maven build)",
    )
    parser.add_argument(
        "-v",
        "--java-version",
        type=int,
        default=17,
        help="sets java version (default: 17)",
    )
    parser.add_argument(
        "--force",
        default=False,
        action="store_true",
        help="forces project creation by overwriting file which has the same project name",
    )

    args = parser.parse_args()
    group_items: list[str] = args.group.split(".")

    if len(group_items) < 2:
        logger.error("Invalid group arguments!")
        sys.exit(1)

    if args.docker:
        args.maven = True

    # DIRS
    root = Path(args.name)

    old_dir_cached = False
    if root.exists() and not args.force:
        rollback(f"Project '{args.name}' already exists!", root, old_dir_cached, False)

    elif root.exists() and args.force:
        logging.info(f"Directory '{args.name}' already exists")
        cache_old_dir(root)
        old_dir_cached = True

    package_path = Path(*group_items)
    template_path = Path(__file__).resolve().parent / "templates"

    mvn_path = root / ".mvn"
    main_path = root / "src" / "main" / "java" / package_path
    test_path = root / "src" / "test" / "java" / package_path
    resources_path = root / "src" / "main" / "resources"

    # FILES
    gitignore_file = root / ".gitignore"
    dockerignore_file = root / ".dockerignore"
    dockerfile_file = root / "Dockerfile"
    docker_compose_file = root / "docker-compose.yml"
    pom_file = root / "pom.xml"
    readme_file = root / "README.md"
    mvnw_file = root / "mvnw"
    mvnw_cmd_file = root / "mvnw.cmd"
    main_java_file = main_path / "Main.java"

    # CREATE & WRITE
    logger.info("Creating & Writing on Directories and Files...")
    context: dict[str, str] = {
        "name": args.name,
        "group": args.group,
        "java_version": str(args.java_version),
    }

    try:
        main_path.mkdir(parents=True, exist_ok=True)
        test_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)

        main_java_file.write_text(
            render_template(template_path, "Main.java.tmpl", context), encoding="utf-8"
        )

        if args.maven:
            logger.info("Setting up Maven Build...")

            mvnw_template = validate_template(template_path, "mvnw")
            mvnw_cmd_template = validate_template(template_path, "mvnw.cmd")
            mvn_dir_template = validate_template(template_path, ".mvn")

            shutil.copytree(mvn_dir_template, mvn_path, dirs_exist_ok=True)
            shutil.copy2(mvnw_cmd_template, mvnw_cmd_file)
            shutil.copy2(mvnw_template, mvnw_file)
            mvnw_file.chmod(0o755)

            pom_file.write_text(
                render_template(template_path, "pom.xml.tmpl", context),
                encoding="utf-8",
            )

        if args.git:
            logger.info("Initializing Git...")

            gitignore_template = validate_template(template_path, ".gitignore")

            subprocess.run(["git", "init"], cwd=root)
            shutil.copy2(gitignore_template, gitignore_file)

            readme_file.write_text(
                render_template(template_path, "README.md.tmpl", context),
                encoding="utf-8",
            )

        if args.docker:
            logger.info("Setting up Docker...")

            dockerignore_template = validate_template(template_path, ".dockerignore")
            dockerfile_template = validate_template(template_path, "Dockerfile")

            shutil.copy2(dockerignore_template, dockerignore_file)
            shutil.copy2(dockerfile_template, dockerfile_file)

            docker_compose_file.write_text(
                render_template(template_path, "docker-compose.yml.tmpl", context),
                encoding="utf-8",
            )

    except FileNotFoundError as e:
        rollback(f"Error during project creation/writing: {e}", root, old_dir_cached)

    # CLEAN UP
    if old_dir_cached:
        cached_path = get_cached_path(root)
        if cached_path.exists():
            logging.info("Removing cached Directory...")
            shutil.rmtree(cached_path)

    logging.info(f"Successfully created projekt {args.name}!")


if __name__ == "__main__":
    main()
