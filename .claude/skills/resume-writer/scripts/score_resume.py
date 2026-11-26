#!/usr/bin/env python3
"""
Build a resume and score it against the guide's page-length-vs-experience
table, plus measure how full the last page actually is.

Usage:
    python3 scripts/score_resume.py <resume-name-or-path> [--skip-build]

Examples:
    python3 scripts/score_resume.py full_stack
    python3 scripts/score_resume.py resumes/computer_vision.json --skip-build

Requires: Node (to build via index.mjs), poppler's pdfinfo/pdftoppm, and Pillow
(python3 -c "import PIL").
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("This script needs Pillow: pip install pillow (or: python3 -c 'import PIL' to check)")

REPO_ROOT = Path(__file__).resolve().parents[4]
RESUMES_DIR = REPO_ROOT / "resumes"
OUTPUT_DIR = REPO_ROOT / "output"

# From the guide's "Resume length and information density" table.
# (min_years_inclusive, max_years_exclusive, min_pages, max_pages)
LENGTH_TABLE = [
    (None, 3, 1, 1),
    (3, 7, 1, 2),
    (7, 12, 2, 2),
    (12, None, 2, 3),
]

WHITE_THRESHOLD = 250  # grayscale 0-255; rows with nothing darker than this count as empty
SHRINKABLE_OCCUPANCY = 0.4  # below this, the last page looks under-filled enough to merge away


def resolve_resume(name_or_path: str) -> Path:
    p = Path(name_or_path)
    if p.suffix == ".json" and p.exists():
        return p
    candidate = RESUMES_DIR / (name_or_path if name_or_path.endswith(".json") else f"{name_or_path}.json")
    if candidate.exists():
        return candidate
    sys.exit(f"Resume not found: {name_or_path}")


def parse_partial_iso_date(value: str) -> datetime.date:
    """JSON Resume dates may be YYYY, YYYY-MM, or YYYY-MM-DD. Pad missing parts
    with the first month/day so partial dates don't crash the parser."""
    parts = value.split("-")
    parts += ["01"] * (3 - len(parts))
    return datetime.date.fromisoformat("-".join(parts))


def years_of_experience(resume: dict) -> float:
    """Span from the earliest work startDate to the latest endDate (today if a job
    is ongoing, i.e. endDate is empty). This is total career length, not a sum of
    per-job durations, matching how the guide's table means 'years of experience'."""
    work = resume.get("work", [])
    today = datetime.date.today()
    starts, ends = [], []
    for job in work:
        start = job.get("startDate") or None
        end = job.get("endDate") or None
        if start:
            starts.append(parse_partial_iso_date(start))
        ends.append(parse_partial_iso_date(end) if end else today)
    if not starts:
        return 0.0
    span_days = (max(ends) - min(starts)).days
    return max(span_days, 0) / 365.25


def recommended_pages(years: float):
    for lo, hi, min_p, max_p in LENGTH_TABLE:
        if (lo is None or years >= lo) and (hi is None or years < hi):
            return min_p, max_p
    return 2, 3


def build_pdf(resume_name: str) -> Path:
    subprocess.run(["node", "index.mjs", resume_name], cwd=REPO_ROOT, check=True)
    pdf_path = OUTPUT_DIR / f"{resume_name}.pdf"
    if not pdf_path.exists():
        sys.exit(f"Build did not produce {pdf_path}")
    return pdf_path


def page_count(pdf_path: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1].strip())
    sys.exit("Could not determine page count from pdfinfo output")


def last_page_occupancy(pdf_path: Path, pages: int) -> float:
    """Render just the last page and find the lowest row that has any non-white
    pixel. Rasterizing (rather than just reading text) catches rule lines, icons,
    and the theme's own spacing choices too, not only text glyphs."""
    with tempfile.TemporaryDirectory() as tmp:
        prefix = os.path.join(tmp, "page")
        subprocess.run(
            ["pdftoppm", "-f", str(pages), "-l", str(pages), "-gray", "-r", "100", str(pdf_path), prefix],
            check=True,
            stderr=subprocess.DEVNULL,  # xpdf's base-14 font substitution warnings are harmless noise
        )
        rendered = list(Path(tmp).glob("page*"))
        if not rendered:
            sys.exit("pdftoppm did not produce an image for the last page")
        img = Image.open(rendered[0]).convert("L")
        width, height = img.size
        pixels = img.load()
        for y in range(height - 1, -1, -1):
            if any(pixels[x, y] < WHITE_THRESHOLD for x in range(width)):
                return (y + 1) / height
    return 0.0


def score(years: float, pages: int, occupancy: float):
    min_p, max_p = recommended_pages(years)

    if pages <= max_p:
        length_score = 100.0
    else:
        length_score = max(0.0, 100.0 - 30.0 * (pages - max_p))

    could_shrink = pages > 1 and pages > min_p and occupancy < SHRINKABLE_OCCUPANCY
    overall = length_score
    if could_shrink:
        overall = max(0.0, overall - (SHRINKABLE_OCCUPANCY - occupancy) * 50)

    return {
        "years_experience": round(years, 1),
        "pages": pages,
        "recommended_pages": f"{min_p}-{max_p}" if min_p != max_p else str(min_p),
        "last_page_occupancy_pct": round(occupancy * 100, 1),
        "length_score": round(length_score, 1),
        "overall_score": round(overall, 1),
        "could_likely_shrink_a_page": could_shrink,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("resume", help="Resume name (e.g. full_stack) or path to its .json file")
    parser.add_argument("--skip-build", action="store_true", help="Reuse the existing output/<name>.pdf instead of rebuilding")
    args = parser.parse_args()

    resume_path = resolve_resume(args.resume)
    resume_name = resume_path.stem
    resume = json.loads(resume_path.read_text())

    pdf_path = OUTPUT_DIR / f"{resume_name}.pdf"
    if not args.skip_build or not pdf_path.exists():
        pdf_path = build_pdf(resume_name)

    years = years_of_experience(resume)
    pages = page_count(pdf_path)
    occupancy = last_page_occupancy(pdf_path, pages)
    result = score(years, pages, occupancy)
    result["resume"] = resume_name

    print(json.dumps(result, indent=2))

    if result["could_likely_shrink_a_page"]:
        print(
            f"\nLast page is only ~{result['last_page_occupancy_pct']}% full for a "
            f"{pages}-page resume — tightening earlier sections could likely remove a page.",
            file=sys.stderr,
        )
    elif pages > int(result["recommended_pages"].split("-")[-1]):
        print(
            f"\n{pages} pages is longer than the {result['recommended_pages']}-page range "
            f"recommended for ~{result['years_experience']} years of experience.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
