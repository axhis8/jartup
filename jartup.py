import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("group", type=str, help="group name (example: 'com.name')")
    parser.add_argument("name", type=str, help="projekt name")
    parser.add_argument(
        "-g", "--git", default=False, action="store_true", help="initialize git"
    )
    parser.add_argument(
        "-d", "--docker", default=False, action="store_true", help="initialize docker"
    )

    args = parser.parse_args()
    group_items: list[str] = args.group.split(".")

    # DIRS
    root = Path(args.name)
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


if __name__ == "__main__":
    main()
