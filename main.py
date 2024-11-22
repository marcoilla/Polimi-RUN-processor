import os
import argparse
from pdf_to_csv import pdf_to_csv
from csv_to_pdf import csv_to_pdf

def process_race_results(input_pdf, output_directory="output", generate_final_pdf=True):
    """
    Process race results from PDF: convert to sorted CSV and optionally generate a formatted PDF.
    
    Args:
        input_pdf (str): Path to the input PDF file containing race results
        output_directory (str): Directory where output files will be saved
        generate_final_pdf (bool): Whether to generate a formatted PDF from the sorted CSV
    
    Returns:
        tuple: Paths to the generated files (csv_path, pdf_path if generated, else None)
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        
        # Generate output file paths
        input_filename = os.path.splitext(os.path.basename(input_pdf))[0]
        csv_path = os.path.join(output_directory, f"{input_filename}_sorted.csv")
        pdf_path = os.path.join(output_directory, f"{input_filename}_sorted_formatted.pdf")
        
        # Step 1: Convert PDF to sorted CSV
        print("Converting race results PDF to sorted CSV...")
        pdf_to_csv(input_pdf, csv_path)
        print(f"Sorted CSV created: {csv_path}")
        
        # Step 2: Generate formatted PDF if requested
        if generate_final_pdf:
            print("Generating formatted PDF from sorted data...")
            description = (
                "Race Results\n"
                "This document contains the sorted race results with participant details.\n"
                "Athletes are ranked by their finish time."
            )
            csv_to_pdf(csv_path, pdf_path, description)
            print(f"Formatted PDF created: {pdf_path}")
            return csv_path, pdf_path
        
        return csv_path, None
        
    except Exception as e:
        print(f"Error processing race results: {str(e)}")
        raise

def setup_argument_parser():
    """
    Set up command line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Process race results from PDF files: convert to sorted CSV and formatted PDF.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input',
        help='Input PDF file or directory containing PDF files',
        required=True
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for generated files (default: output)',
        default='output'
    )
    
    parser.add_argument(
        '--csv-only',
        action='store_true',
        help='Generate only sorted CSV files (skip PDF generation)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed processing information'
    )
    
    return parser

def main():
    """
    Main function to handle race results processing with command line arguments.
    
    Example usage:
        # Process a single PDF file:
        python main.py -i race_results.pdf -o output_folder
        
        # Process all PDFs in a directory:
        python main.py -i input_folder -o output_folder
        
        # Generate only CSV files:
        python main.py -i race_results.pdf --csv-only
        
        # Show detailed processing information:
        python main.py -i race_results.pdf -v
    """
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    try:
        # Create output directory
        os.makedirs(args.output, exist_ok=True)
        
        # Determine input files
        if os.path.isfile(args.input):
            # Single file processing
            if args.input.endswith('.pdf'):
                pdf_files = [args.input]
            else:
                raise ValueError("Input file must be a PDF")
        elif os.path.isdir(args.input):
            # Directory processing
            pdf_files = [
                os.path.join(args.input, f) 
                for f in os.listdir(args.input) 
                if f.endswith('.pdf')
            ]
            if not pdf_files:
                raise ValueError(f"No PDF files found in directory: {args.input}")
        else:
            raise ValueError("Input path does not exist")
        
        # Process each PDF file
        for pdf_file in pdf_files:
            if args.verbose:
                print(f"\nProcessing: {pdf_file}")
                print("-" * 50)
            
            csv_path, pdf_path = process_race_results(
                pdf_file,
                output_directory=args.output,
                generate_final_pdf=not args.csv_only
            )
            
            if args.verbose:
                print("\nProcessing completed!")
                print(f"- Input PDF: {pdf_file}")
                print(f"- Generated CSV: {csv_path}")
                if pdf_path:
                    print(f"- Generated PDF: {pdf_path}")
                print("-" * 50)
            else:
                print(f"Processed: {os.path.basename(pdf_file)}")
        
        print("\nAll files processed successfully!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()