"""Validation logic for USB PD parser outputs."""

import os
import json
import pandas as pd


class SpecValidator:  # pylint: disable=too-few-public-methods
    """Validate extracted USB PD specification outputs."""

    def __init__(self, output_dir="sample_out"):
        """
        Initialize the SpecValidator.

        Args:
            output_dir (str): Directory containing parser output files.
        """
        self.output_dir = output_dir

    def _load_jsonl(self, filename):
        """
        Load a JSONL file from the output directory.

        Args:
            filename (str): File name to load.

        Returns:
            list[dict]: Parsed JSON objects from the file.
        """
        path = os.path.join(self.output_dir, filename)
        data = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return data

    def validate_outputs(self):
        """
        Validate consistency between TOC and parsed sections.

        Generates a validation report with metrics and saves to Excel.
        """
        toc = self._load_jsonl("usb_pd_toc.jsonl")
        sections = self._load_jsonl("usb_pd_spec.jsonl")

        # Collect section ids
        toc_ids = {t["section_id"] for t in toc if "section_id" in t}
        parsed_ids = {s["section_id"] for s in sections if "section_id" in s}

        # Compare
        missing_in_parsed = toc_ids - parsed_ids
        missing_in_toc = parsed_ids - toc_ids

        report = {
            "toc_count": len(toc),
            "parsed_count": len(sections),
            "missing_in_parsed": len(missing_in_parsed),
            "missing_in_toc": len(missing_in_toc),
        }

        print("📊 Validation Report:", report)

        # Save report as Excel
        report_df = pd.DataFrame(
            [{"metric": k, "value": v} for k, v in report.items()]
        )
        path = os.path.join(self.output_dir, "validation_report.xlsx")
        report_df.to_excel(path, index=False)

        print(f"✅ Validation report saved: {path}")
