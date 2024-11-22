import pandas as pd
from fpdf import FPDF

import pandas as pd
from fpdf import FPDF

def csv_to_pdf(csv_file, pdf_file, description="This table represents the data from the CSV file."):
    # Read the CSV file
    try:
        data_frame = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Create a PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title to the PDF
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Data Table", ln=True, align='C')  # Title centered at the top
    pdf.ln(5)  # Add extra space after the title

    # Add a description below the title with reduced line spacing
    pdf.set_font("Arial", size=10)
    line_height = pdf.font_size * 1.2  # Adjust line spacing
    pdf.multi_cell(0, line_height, description, align='C')
    pdf.ln(5)  # Add space after the description

    # Set font for the table
    pdf.set_font("Arial", size=9)  # Slightly increased font size for the table
    row_height = pdf.font_size * 1.5  # Row height

    # Calculate column widths to fill the page width
    table_width = pdf.w - 20  # Total table width (page width minus margins)
    column_ratios = []
    for column_name in data_frame.columns:
        max_width = pdf.get_string_width(str(column_name).capitalize())  # Start with header width
        for item in data_frame[column_name]:
            text = str(item) if not pd.isna(item) else ""
            max_width = max(max_width, pdf.get_string_width(text))
        column_ratios.append(max_width)  # Save maximum width for the column

    # Normalize column widths to fit the page
    total_width = sum(column_ratios)
    column_widths = [table_width * (ratio / total_width) for ratio in column_ratios]

    # Write the headers (capitalize the first letter)
    for i, column_name in enumerate(data_frame.columns):
        pdf.cell(column_widths[i], row_height, str(column_name).capitalize(), border=1, align='C')
    pdf.ln(row_height)

    # Write the rows of data
    for _, row in data_frame.iterrows():
        for i, item in enumerate(row):
            if pd.isna(item):  # Check if the value is missing (NaN)
                text = ""
            else:
                # Write integers without decimal points and other values as strings
                if isinstance(item, (int, float)) and item == int(item):
                    text = f"{int(item)}"
                else:
                    text = str(item)
            pdf.cell(column_widths[i], row_height, text, border=1, align='C')
        pdf.ln(row_height)

    # Save the PDF to a file
    try:
        pdf.output(pdf_file)
        print(f"PDF file successfully saved: {pdf_file}")
    except Exception as e:
        print(f"Error saving the PDF file: {e}")