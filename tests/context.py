from pathlib import Path
import sys

# Enables workingdays module imports when running tests
context = Path(__file__).resolve().parents[1] / "workingdays"
sys.path.insert(0, str(context))