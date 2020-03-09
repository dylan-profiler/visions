from pathlib import Path

from visions.types import (
    visions_integer,
    visions_existing_path,
    visions_string,
    visions_datetime,
)
from visions.application.summaries.complete_summary import CompleteSummary

summaries_dir = Path("summaries/")
summaries_dir.mkdir(exist_ok=True)

summary = CompleteSummary()

# For a typeset
summary.plot(summaries_dir / "summary_complete.svg")

# For specific types
summary.plot(summaries_dir / "summary_integer.svg", visions_integer)
summary.plot(summaries_dir / "summary_string.svg", visions_string)
summary.plot(summaries_dir / "summary_datetime.svg", visions_datetime)
summary.plot(summaries_dir / "summary_existing_path.svg", visions_existing_path)
