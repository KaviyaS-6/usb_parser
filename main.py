"""
main.py

Entry point for USB PD Specification parser.
- Extracts Table of Contents (TOC) from the USB PD spec PDF
- Extracts detailed sections and their content
- Validates consistency between TOC and parsed sections
- Saves outputs to Excel/JSONL format
"""

from parser import PDFParser
from validator import SpecValidator


def main():
    """Run the USB PD parsing and validation pipeline."""
    pdf_path = "usb_pd_spec.pdf"
    output_dir = "sample_out"

    parser = PDFParser(pdf_path, output_dir)

    # Extract
    toc = parser.extract_toc()
    sections = parser.extract_sections()

    print(f"TOC sections extracted: {len(toc)}")
    print(f"Parsed sections with content: {len(sections)}")

    # Save outputs
    parser.save_excel(toc, "usb_pd_toc.xlsx")
    parser.save_excel(sections, "usb_pd_sections_with_content.xlsx")
    parser.save_jsonl(toc, "usb_pd_toc.jsonl")
    parser.save_jsonl(sections, "usb_pd_spec.jsonl")

    # Run validation
    validator = SpecValidator(output_dir)
    validator.validate_outputs()

    print("✅ All outputs saved in", output_dir)


if __name__ == "__main__":
    main()
