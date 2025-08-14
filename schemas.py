{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "USB PD Table of Contents Entry",
  "type": "object",
  "properties": {
    "doc_title": { "type": "string" },
    "section_id": { "type": "string" },
    "title": { "type": "string" },
    "page": { "type": "integer", "minimum": 1 },
    "level": { "type": "integer", "minimum": 1 },
    "parent_id": { "type": ["string", "null"] },
    "full_path": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["doc_title", "section_id", "title", "page", "level", "full_path"]
}
