# ruff: noqa
"""
Seeds - Index.

This module initializes the database seeding process by importing seed functions
from various modules.
"""

import argparse
import os
import sys
from pathlib import Path


# Set the working directory to the 'src' folder
src_path = Path(__file__).resolve().parent.parent.parent.parent.parent
os.chdir(src_path)
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    from src.libs.log import get_context as _  # noqa: E402
    from src.libs.log import get_logger  # noqa: E402
    from src.libs.utilities.path.to_seed_files import load_all_seeds

    log = get_logger()

    order_to_seed = load_all_seeds()

    # Parse command line arguments to determine which seeds to run
    parser = argparse.ArgumentParser(description="Seed the database.")
    parser.add_argument(
        "--seeds",
        type=str,
        default="all",
        help="Which seeds to run (e.g. 'all', 'users', ...)",
    )

    seeds_arg = getattr(parser.parse_args(), "seeds", None)

    if not seeds_arg:
        log.warning(
            f"{_()}: No seeds specified. Use --seeds to specify which seeds to run.",
        )
        sys.exit(1)

    if seeds_arg == "all":
        log.info(f"{_()}: Found {len(order_to_seed)} seed functions to run.")

        for func in order_to_seed:
            log.debug(f"{_()}: Running seed '{func.__name__}'")
            func()

        log.info(f"{_()}: All seeds have been run successfully.")
        sys.exit(0)

    target_seed = f"seed_{seeds_arg}"

    matched_funcs = [func for func in order_to_seed if func.__name__ == target_seed]

    if matched_funcs:
        for func in matched_funcs:
            log.debug(f"{_()}: Running seed '{func.__name__}'")
            func()

    else:
        log.warning(f"{_()}: No seed found for '{seeds_arg}'")
