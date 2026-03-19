"""Test script for processing PDF files from ex1/input and outputting to ex1/output."""

import sys
import json
from pathlib import Path

# Add parent directory to path for app imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.orchestrator.manager import ConversionManager
from app.internal.config import Settings


def main():
    """Process PDF files and save results to ex1/output.

    Usage:
        python3 test_pdf_processing.py                    # Process all PDFs in ex1/input/
        python3 test_pdf_processing.py path/to/file.pdf   # Process specific PDF file(s)
    """

    # Setup paths
    test_dir = Path(__file__).parent
    output_dir = test_dir / "ex1" / "output"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize settings and conversion manager
    settings = Settings()
    manager = ConversionManager(settings)

    # Check if manager is ready
    if not manager.is_ready():
        print("❌ ConversionManager is not ready")
        return

    print(f"✅ ConversionManager ready")
    print(f"📁 Output directory: {output_dir}")
    print()

    # Determine which files to process
    if len(sys.argv) > 1:
        # Process files provided as arguments
        pdf_files = [Path(arg) for arg in sys.argv[1:]]
        print(f"📄 Processing {len(pdf_files)} file(s) from command line\n")
    else:
        # Process all PDFs from ex1/input/
        input_dir = test_dir / "ex1" / "input"
        pdf_files = list(input_dir.glob("*.pdf"))
        print(f"📁 Input directory: {input_dir}")

    if not pdf_files:
        print("⚠️  No PDF files found")
        return

    # Validate that files exist
    missing_files = [f for f in pdf_files if not f.exists()]
    if missing_files:
        print("❌ The following files were not found:")
        for f in missing_files:
            print(f"   - {f}")
        return

    print(f"📄 Found {len(pdf_files)} PDF file(s) to process\n")

    # Process each PDF file
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        try:
            # Read PDF file
            with open(pdf_file, "rb") as f:
                file_bytes = f.read()

            # Convert using OCR
            result = manager.convert(
                file_bytes=file_bytes,
                file_format="pdf",
                use_ocr=True,
            )

            # Save results
            base_name = pdf_file.stem

            # Save as text
            txt_output = output_dir / f"{base_name}.txt"
            with open(txt_output, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"  ✅ Text saved to: {txt_output.name}")

            # Save as JSON (with metadata)
            json_output = output_dir / f"{base_name}.json"
            json_data = {
                "filename": pdf_file.name,
                "line_count": result["line_count"],
                "lines": result["lines"],
            }
            with open(json_output, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"  ✅ JSON saved to: {json_output.name}")

        except Exception as e:
            print(f"  ❌ Error processing {pdf_file.name}: {e}")

        print()

    print("✅ All files processed successfully!")


if __name__ == "__main__":
    main()
