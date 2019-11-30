from pathlib import Path

from visions.core.implementations.types import (
    visions_integer,
    visions_existing_path,
    visions_string,
)
from visions.application.summaries.summary import CompleteSummary


summaries_dir = Path("summaries/")
summaries_dir.mkdir(exist_ok=True)

summary = CompleteSummary()

# For a typeset
summary.plot(summaries_dir / "summary_complete.svg")

# For specific types
summary.plot(summaries_dir / "summary_integer.svg", visions_integer)
summary.plot(summaries_dir / "summary_string.svg", visions_string)
summary.plot(summaries_dir / "summary_existing_path.svg", visions_existing_path)
