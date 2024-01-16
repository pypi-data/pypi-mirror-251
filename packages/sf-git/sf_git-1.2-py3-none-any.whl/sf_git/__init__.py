from pathlib import Path

from dotenv import load_dotenv
from pkg_resources import DistributionNotFound, get_distribution

__version__ = "1.2"

HERE = Path(__file__).parent
dotenv_path = HERE / "sf_git.conf"

if dotenv_path.is_file():
    load_dotenv(dotenv_path=dotenv_path)
