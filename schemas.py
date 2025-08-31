"""JSON Schemas for USB PD specification outputs."""

TOC_SCHEMA = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "page": {"type": "integer"},
        "level": {"type": "integer"},
        "parent_id": {"type": ["string", "null"]},
        "full_path": {"type": "string"},
    },
    "required": [
        "section_id",
        "title",
        "page",
        "level",
        "full_path",
    ],
}
