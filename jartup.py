import argparse


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

    print(args)


if __name__ == "__main__":
    main()
