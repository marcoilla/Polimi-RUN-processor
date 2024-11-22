import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pdf_to_csv import pdf_to_csv
from csv_to_pdf import csv_to_pdf


class RaceResultsProcessorGUI:
    def __init__(self, root):
        """
        Initialize the GUI for race results processing.
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Race Results Processor")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set up variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.csv_only = tk.BooleanVar(value=False)
        self.processing = False
        
        # Default output path
        default_output = os.path.join(os.getcwd(), "output")
        self.output_path.set(default_output)
        
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI layout and components"""
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main window grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure main frame grid
        main_frame.columnconfigure(0, weight=1)
        for i in range(5):  # Configure rows 0-4
            main_frame.rowconfigure(i, weight=1 if i == 3 else 0)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=5, pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="PDF File/Folder:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(input_frame, textvariable=self.input_path).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=5, pady=5)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Entry(output_frame, textvariable=self.output_path).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=2, padx=5)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), padx=5, pady=5)
        options_frame.columnconfigure(0, weight=1)
        
        ttk.Checkbutton(options_frame, text="Generate CSV only (skip PDF generation)", 
                       variable=self.csv_only).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # Progress section
        self.progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        self.progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.progress_frame.columnconfigure(0, weight=1)
        self.progress_frame.rowconfigure(1, weight=1)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Log text area with frame
        log_frame = ttk.Frame(self.progress_frame)
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.E), padx=5, pady=5)
        
        self.process_button = ttk.Button(button_frame, text="Process Files", command=self.start_processing)
        self.process_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).grid(row=0, column=1, padx=5)
        
    def browse_input(self):
        """Open file dialog for input selection"""
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if path:
            self.input_path.set(path)
            self.log(f"Selected input: {path}")
    
    def browse_output(self):
        """Open directory dialog for output folder selection"""
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)
            self.log(f"Selected output folder: {path}")
    
    def log(self, message):
        """Add message to log window"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log window"""
        self.log_text.delete(1.0, tk.END)
    
    def process_files(self):
        """Process the selected files"""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            
            if not input_path:
                raise ValueError("Please select an input PDF file")
            
            if not output_path:
                raise ValueError("Please select an output folder")
            
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            
            # Process the file
            self.log(f"Processing: {input_path}")
            
            # Get the base filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            csv_path = os.path.join(output_path, f"{base_name}_sorted.csv")
            
            # Convert PDF to CSV
            self.log("Converting to CSV...")
            pdf_to_csv(input_path, csv_path)
            self.log(f"CSV file created: {csv_path}")
            
            # Generate formatted PDF if requested
            if not self.csv_only.get():
                pdf_path = os.path.join(output_path, f"{base_name}_sorted_formatted.pdf")
                self.log("Generating formatted PDF...")
                description = (
                    "Race Results\n"
                    "This document contains the sorted race results with participant details.\n"
                    "Athletes are ranked by their finish time."
                )
                csv_to_pdf(csv_path, pdf_path, description)
                self.log(f"PDF file created: {pdf_path}")
            
            # Use Tkinter's `after` method to update the UI after processing
            self.root.after(0, self.show_success_message)

        except Exception as e:
            # If an exception occurs, show an error message in the main thread
            self.root.after(0, self.show_error_message, str(e))
    

    def show_success_message(self):
        """Show a success message in a dialog box"""
        messagebox.showinfo("Success", "Processing completed successfully!")
    
    def show_error_message(self, error_message):
        """Show an error message in a dialog box"""
        messagebox.showerror("Error", error_message)
    
    def start_processing(self):
        """Start processing in a separate thread"""
        if not self.processing:
            self.processing = True
            self.process_button["state"] = "disabled"
            self.progress_bar.start()
            
            # Start processing in a separate thread
            self.thread = threading.Thread(target=self.process_files)
            self.thread.daemon = True
            self.thread.start()

            # Periodically check if the thread is still running
            # The check_thread function will be called every 100 ms
            self.root.after(100, self.check_thread)
    
    def check_thread(self):
        """Checks if the thread has finished its task"""
        if self.thread.is_alive():
            # If the thread is still running, keep checking
            # The function will be called again in 100 ms
            self.root.after(100, self.check_thread)
        else:
            # Ensure proper thread termination and UI update
            self.processing = False
            self.progress_bar.stop()
            self.process_button["state"] = "normal"

def gui():
    root = tk.Tk()
    app = RaceResultsProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    gui()