import os
import unittest

from usb_parser.parser import PDFParser
from usb_parser.validator import SpecValidator


class TestParserValidator(unittest.TestCase):
    """Unit tests for PDFParser and SpecValidator."""

    def setUp(self):
        self.output_dir = "sample_out"
        self.parser = PDFParser("sample.pdf", output_dir=self.output_dir)
        self.validator = SpecValidator(output_dir=self.output_dir)

    def test_save_and_validate(self):
        """Test save_jsonl and validation workflow."""
        toc = self.parser.extract_toc()
        sections = [
            {
                "section_id": "1",
                "title": "Test",
                "page": 1,
                "level": 1,
                "parent_id": None,
                "full_path": "1 Test",
            }
        ]

        self.parser.save_jsonl(toc, "usb_pd_toc.jsonl")
        self.parser.save_jsonl(sections, "usb_pd_spec.jsonl")

        self.validator.validate_outputs()
        path = os.path.join(self.output_dir, "validation_report.xlsx")
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
