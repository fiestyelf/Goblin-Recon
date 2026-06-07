"""pytest configuration for Goblin Recon.

Auto-discovers scripts so tests don't need sys.path hacks.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
