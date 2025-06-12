# File Analysis Tool

A FastAPI-based web application that analyzes Excel and CSV files, performs transformations, and displays the results in a modern web interface.

## Features

- Upload Excel (.xlsx, .xls) or CSV files
- Automatic file analysis and transformation
- Modern UI with Tailwind CSS
- Real-time progress indication
- Interactive results table
- Download transformed data

## Requirements

- Python 3.10
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Click the "Choose File" button or drag and drop your Excel/CSV file
2. Click "Analyze File" to process the data
3. View the results in the interactive table
4. Use the "Download Results" button to save the transformed data

## Development

The application consists of:
- `main.py`: FastAPI backend with file processing logic
- `templates/index.html`: Frontend template with Vue.js and Tailwind CSS
- `requirements.txt`: Python dependencies

## License

MIT License 