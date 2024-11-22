# PoliMi Run Race Results Processor

## Overview
A Python application to extract, sort, and format race results from PDF files, specifically designed for the PoliMi Run event. Supports both command-line and graphical user interfaces.

## Features
- Convert race result PDFs to sorted CSV files
- Generate formatted PDF reports
- Process single or multiple PDF files
- Graphical User Interface (GUI)
- Command-line interface

## Prerequisites
- Python 3.7+
- Required libraries: 
  * `tkinter`
  * `pdfplumber`
  * `fpdf`
  * `pandas`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/marcoilla/Polimi-RUN-processor.git
cd Polimi-RUN-processor
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install pdfplumber fpdf pandas
```
```bash
pip install -r requirements.txt
```

## Usage

### Graphical User Interface (Recommended)
Launch the GUI application:
```bash
python gui.py
```

#### GUI Features:
- Select input PDF file or folder
- Choose output directory
- Option to generate CSV only
- Progress tracking
- Error handling

### Command-Line Interface
Process race results directly from the terminal:

#### Process a Single PDF
```bash
python main.py -i race_results.pdf -o output_folder
```

#### Process All PDFs in a Directory
```bash
python main.py -i input_folder -o output_folder
```

## Command Line Arguments

| Argument | Short | Long | Description | Required | Default |
|----------|-------|------|-------------|----------|---------|
| Input | `-i` | `--input` | Input PDF file or directory | Yes | - |
| Output | `-o` | `--output` | Output directory | No | `output` |
| CSV Only | - | `--csv-only` | Generate only sorted CSV files | No | False |
| Verbose | `-v` | `--verbose` | Print detailed processing information | No | False |

## Important Note

To use this application, you need to download the race results PDF from the official race results platform, [Endu](https://www.endu.net).

## Contributing
Pull requests are welcome! Please open an issue first to discuss proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to:
- Use the software commercially
- Modify the software
- Distribute the software
- Use the software privately
- Use the software for warranty purposes

The only requirements are to:
- Include the original license and copyright notice in any substantial portion of the software
- Provide attribution to the original author

## Created with ❤️ by a PoliMi Student