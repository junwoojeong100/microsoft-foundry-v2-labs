from pathlib import Path

from foundry_workshop.agents import serve
from foundry_workshop.profiles import packaged_profile
from foundry_workshop.settings import Settings

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    serve(Settings.from_env(), root, packaged_profile(root))
