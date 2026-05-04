"""
Extract PDF files to markdown using pymupdf4llm
"""
import pymupdf
import pymupdf4llm
from pathlib import Path
import re
import os

# Directories
pdf_dir = Path("PDF Downloads")
output_dir = Path("./_extracts")

os.makedirs(output_dir, exist_ok=True)

def clean_filename(filename):
    """Convert PDF filename to clean markdown filename"""
    # Remove .pdf extension
    name = filename.replace('.pdf', '')
    # Clean up common patterns
    name = re.sub(r'[_-]+', ' ', name)
    # Capitalize words
    name = ' '.join(word.capitalize() for word in name.split())
    return f"{name}.md"

def extract_pdf_to_markdown(pdf_path, output_path):
    """Extract PDF content to markdown"""
    try:
        print(f"Processing: {pdf_path.name}")
        
        # Extract markdown from PDF
        md_text = pymupdf4llm.to_markdown(pdf_path)
        # temp just extract text to check if it's working
        # pages: pymupdf.Page = pymupdf.Document(pdf_path).pages()
 
        # Add header with metadata
        header = f"# {output_path.stem}\n\n"
        header += f"**Source:** {pdf_path.name}\n\n"
        header += "---\n\n"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header + md_text)
        
        print(f"  ✓ Saved to: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    # Get all PDFs
    pdf_files = list(pdf_dir.glob("*.pdf"))
    # pdf_files = [f for f in pdf_files if f.name == "1-s2.0-S004727270800131X-main.pdf"]
    if not pdf_files:
        print("No PDF files found in 'PDF Downloads' folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files\n")
    
    success_count = 0
    
    for pdf_path in pdf_files:
        # Generate output filename
        output_filename = clean_filename(pdf_path.name)
        output_path = output_dir / output_filename
        
        # Skip if markdown file already exists (unless you want to overwrite)
        if output_path.exists():
            print(f"Skipping: {pdf_path.name} (markdown already exists)")
            continue
        
        # Extract
        if extract_pdf_to_markdown(pdf_path, output_path):
            success_count += 1
        
        print()  # Blank line between files
    
    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{len(pdf_files)} PDFs extracted")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
