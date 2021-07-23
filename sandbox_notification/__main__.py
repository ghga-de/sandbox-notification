"""Main entrypoint for the service"""

from .channels import subscribe

def run():
    subscribe()

if __name__ == "__main__":
    run()