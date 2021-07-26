"""Main entrypoint for the service"""

import argparse
from .topics import subscribe

def run():
    """Run a notification microservice."""
    parser = argparse.ArgumentParser(
        description = 'Subscribe to specific topics to receive relevant messages.')
    parser.add_argument('topic_str', type=str)
    args = parser.parse_args()
    subscribe(args.topic_str)

if __name__ == "__main__":
    run()
