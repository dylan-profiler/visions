from pathlib import Path

from visions.core.implementations.types import visions_integer, visions_existing_path
from visions.core.summaries.summary import CompleteSummary


summaries_dir = Path("summaries/")
summaries_dir.mkdir(exist_ok=True)

summary = CompleteSummary()

# For all types
summary.plot(summaries_dir / "summary_complete.svg")

# For a specific type
summary.plot(summaries_dir / "summary_integer.svg", visions_integer)
summary.plot(summaries_dir / "summary_existing_path.svg", visions_existing_path)
