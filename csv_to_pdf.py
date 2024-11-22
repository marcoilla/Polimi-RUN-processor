import pandas as pd
from fpdf import FPDF

def csv_to_pdf(csv_file, pdf_file, description="This table represents the data from the CSV file."):
    """
    Converts a CSV file to a PDF file with a tabular representation of the data.

    Args:
        csv_file (str): The path to the CSV file to read.
        pdf_file (str): The path where the generated PDF file will be saved.
        description (str, optional): A short description to include at the top of the PDF. Defaults to a generic message.
    """
    # Read the CSV file
    try:
        data_frame = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Create a PDF object and configure it
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title to the PDF
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Data Table", ln=True, align='C')
    pdf.ln(5)

    # Add a description below the title
    pdf.set_font("Arial", size=10)
    line_height = pdf.font_size * 1.2
    pdf.multi_cell(0, line_height, description, align='C')
    pdf.ln(5)

    # Configure table fonts and row heights
    pdf.set_font("Arial", size=9)
    row_height = pdf.font_size * 1.5

    # Calculate column widths to fit the page
    table_width = pdf.w - 20
    column_ratios = []
    for column_name in data_frame.columns:
        max_width = pdf.get_string_width(str(column_name).capitalize())
        for item in data_frame[column_name]:
            text = str(item) if not pd.isna(item) else ""
            max_width = max(max_width, pdf.get_string_width(text))
        column_ratios.append(max_width)

    # Normalize column widths to fit the table within the page width
    total_width = sum(column_ratios)
    column_widths = [table_width * (ratio / total_width) for ratio in column_ratios]

    # Write the table headers
    for i, column_name in enumerate(data_frame.columns):
        pdf.cell(column_widths[i], row_height, str(column_name).capitalize(), border=1, align='C')
    pdf.ln(row_height)

    # Write the rows of data
    for _, row in data_frame.iterrows():
        for i, item in enumerate(row):
            if pd.isna(item):
                text = ""
            else:
                # Format integers without decimals and other values as strings
                if isinstance(item, (int, float)) and item == int(item):
                    text = f"{int(item)}"
                else:
                    text = str(item)
            pdf.cell(column_widths[i], row_height, text, border=1, align='C')
        pdf.ln(row_height)

    # Save the PDF to a file
    try:
        pdf.output(pdf_file)  # Save the PDF to the specified path
        print(f"PDF file successfully saved: {pdf_file}")
    except Exception as e:
        print(f"Error saving the PDF file: {e}")