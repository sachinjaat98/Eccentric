"""Local development entry point for the Eccentric API."""
import argparse
import logging

from eccentric import __version__
from eccentric.web import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Eccentric OCR API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    create_app().run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
