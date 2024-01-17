import argparse

import structlog
from dotenv import load_dotenv

load_dotenv(".env", override=True)

from .core import run_session

logger = structlog.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run codecraft session")
    parser.add_argument("-c", "--coverage", action="store_true", help="Run worker to increase coverage", default=False)
    parser.add_argument("-q", "--query", type=str, help="Get query param from CLI", default=None)
    args = parser.parse_args()

    if args.coverage:
        run_session(coverage=True)
    elif args.query:
        run_session(query=args.query)
    else:
        run_session()


if __name__ == "__main__":  # pragma: no cover
    main()
