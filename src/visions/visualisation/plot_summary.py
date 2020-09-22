from pathlib import Path

from visions.application.summaries.complete_summary import CompleteSummary
from visions.types import DateTime, File, Integer, String


def generate_summary_plots() -> None:
    summaries_dir = Path("summaries/")
    summaries_dir.mkdir(exist_ok=True)

    summary = CompleteSummary()

    # For a typeset
    summary.plot(summaries_dir / "summary_complete.svg")

    # For specific types
    summary.plot(summaries_dir / "summary_integer.svg", Integer)
    summary.plot(summaries_dir / "summary_string.svg", String)
    summary.plot(summaries_dir / "summary_datetime.svg", DateTime)
    summary.plot(summaries_dir / "summary_file.svg", File)


if __name__ == "__main__":
    generate_summary_plots()
