import pandas as pd
import fitz  # PyMuPDF
import re
import os

PDF_FILE = "USB_PD_Spec.pdf"
OUTPUT_XLSX = "usb_pd_sections_with_content.xlsx"

def extract_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc_raw = doc.get_toc()
    toc_list = []
    for entry in toc_raw:
        level, title, page = entry
        # Remove weird whitespace/newlines
        title = re.sub(r'\s+', ' ', title).strip()
        toc_list.append({"level": level, "title": title, "page": page})
    return toc_list

def extract_sections(pdf_path, toc):
    doc = fitz.open(pdf_path)
    sections = []
    for i, toc_entry in enumerate(toc):
        start_page = toc_entry["page"] - 1
        end_page = toc[i + 1]["page"] - 2 if i + 1 < len(toc) else doc.page_count - 1
        text = ""
        for p in range(start_page, end_page + 1):
            text += doc[p].get_text("text") + "\n"
        sections.append({
            "section": toc_entry["title"],
            "page_start": toc_entry["page"],
            "content": text.strip()
        })
    return sections

def print_toc(toc):
    # Find max length of "Title" part for alignment
    max_len = max(len(f"{entry['title']}") for entry in toc) + 5
    for entry in toc:
        dots = '.' * (max_len - len(entry['title']))
        print(f"{entry['title']} {dots} {entry['page']}")

def save_to_excel(sections, filename):
    df = pd.DataFrame(sections)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    print(f"Using PDF file: {PDF_FILE}")

    toc_entries = extract_toc(PDF_FILE)
    sections_data = extract_sections(PDF_FILE, toc_entries)

    # Filter only sections with content
    sections_with_content = [s for s in sections_data if s["content"].strip()]

    # Print TOC like screenshot
    print_toc(toc_entries)

    # Print summary
    print(f"TOC entries extracted: {len(toc_entries)}")
    print(f"Document sections extracted: {len(sections_data)}")
    print(f"Sections with content extracted: {len(sections_with_content)}")

    # Save Excel
    save_to_excel(sections_with_content, OUTPUT_XLSX)
    print(f"Excel file saved: {OUTPUT_XLSX}")
