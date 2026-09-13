from pathlib import Path

from foundry_workshop.agents import serve
from foundry_workshop.settings import Settings

if __name__ == "__main__":
    serve(Settings.from_env(), Path(__file__).resolve().parent)
