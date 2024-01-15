#!/usr/bin/env python3

import my_functions_beatzaplenty.general_purpose as general_purpose

def main(services):
    """
    Update Docker Containers.

    :param services: An array of service names to be updated
    """
    try:
        for service in services:
            path = f"/docker/{service}/docker-compose.yml"
            pull_command = ["docker-compose", "--file", path, "pull"]
            up_command = ["docker-compose", "--file", path, "up", "-d"]
            if not general_purpose.run_command(pull_command):
                continue
            
            if not general_purpose.run_command(up_command):
                continue
        prune_command = ["docker","system","prune","-f"]
        general_purpose.run_command(prune_command)

    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    import argparse

    parser=argparse.ArgumentParser()

    parser.add_argument("--containers", nargs='+', help="Containers to update",required=True)

    args=parser.parse_args()
    main(args.containers)  # Replace with your list of services