from pathlib import Path

from visions.types import Integer, ExistingPath, String, DateTime
from visions.application.summaries.complete_summary import CompleteSummary

summaries_dir = Path("summaries/")
summaries_dir.mkdir(exist_ok=True)

summary = CompleteSummary()

# For a typeset
summary.plot(summaries_dir / "summary_complete.svg")

# For specific types
summary.plot(summaries_dir / "summary_integer.svg", Integer)
summary.plot(summaries_dir / "summary_string.svg", String)
summary.plot(summaries_dir / "summary_datetime.svg", DateTime)
summary.plot(summaries_dir / "summary_existing_path.svg", ExistingPath)
