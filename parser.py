"""USB PD Specification Parser."""

import os
import json
import PyPDF2


class PDFParser:
    """Parse USB PD specification PDF into structured JSONL outputs."""

    def __init__(self, pdf_path, output_dir="sample_out"):
        """
        Initialize the PDFParser.

        Args:
            pdf_path (str): Path to the USB PD specification PDF file.
            output_dir (str): Directory where parsed outputs will be saved.
        """
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_toc(self):
        """
        Extract table of contents from the PDF.

        Returns:
            list[dict]: TOC entries with section_id, title, page,
                level, parent_id, and full_path.
        """
        # TODO: Implement real ToC parsing from PDF bookmarks/outlines
        return [
            {
                "section_id": "1",
                "title": "Introduction",
                "page": 1,
                "level": 1,
                "parent_id": None,
                "full_path": "1 Introduction",
            }
        ]

    def extract_sections(self):
        """
        Extract sections and text content from the PDF.

        Returns:
            list[dict]: Section entries with section_id, title, page,
                level, parent_id, full_path, and text.
        """
        sections = []
        with open(self.pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                sections.append(
                    {
                        "section_id": f"{i}",
                        "title": f"Page {i}",
                        "page": i,
                        "level": 1,
                        "parent_id": None,
                        "full_path": f"Page {i}",
                        "text": text.strip(),
                    }
                )
        return sections

    def save_jsonl(self, data, filename):
        """
        Save parsed data into JSONL format.

        Args:
            data (list[dict]): Parsed entries.
            filename (str): Name of the JSONL output file.
        """
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            for entry in data:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def validate_sections(self, toc, sections):
        """
        Validate that ToC entries exist in parsed sections.

        Args:
            toc (list[dict]): Table of contents entries.
            sections (list[dict]): Parsed section entries.

        Returns:
            dict: {"missing": [...], "coverage": float}
        """
        section_ids = {s["section_id"] for s in sections}
        missing = [t for t in toc if t["section_id"] not in section_ids]
        coverage = (
            (len(toc) - len(missing)) / len(toc) * 100 if toc else 100.0
        )
        return {"missing": missing, "coverage": coverage}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="USB PD Specification PDF Parser"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    args = parser.parse_args()

    parser_obj = PDFParser(args.pdf)

    toc = parser_obj.extract_toc()
    sections = parser_obj.extract_sections()

    parser_obj.save_jsonl(toc, "toc.jsonl")
    parser_obj.save_jsonl(sections, "sections.jsonl")

    report = parser_obj.validate_sections(toc, sections)
    parser_obj.save_jsonl([report], "validation.jsonl")

    print(f"✅ Parsing complete. Coverage: {report['coverage']:.2f}%")
