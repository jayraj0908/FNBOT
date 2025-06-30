# Trust Bodhi Backend

A clean, modular FastAPI backend for processing client data with multiple normalization tools.

## 📁 Project Structure

```
backend/
├── main.py                     # FastAPI router: handles POST requests only
├── tools/
│   ├── __init__.py            # Package initialization
│   ├── bbb_normalizer.py      # BBB Purchase Log normalization
│   └── nectar_dashboard.py    # Nectar CPG dashboard processing
├── utils/
│   ├── __init__.py            # Package initialization
│   └── file_utils.py          # Shared file operations and utilities
├── files/                     # Output and temporary upload directory
└── requirements.txt           # Python dependencies
```

## 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```
   
   The server will start on `http://localhost:8000`

## 🔌 API Endpoints

### Health Check
- **GET** `/health` - Check if the API is running

### BBB Normalization
- **POST** `/analyze` - Process BBB purchase log data
  - `bev_file` (CSV): 60 Bev CSV file
  - `supplier_file` (Excel): Supplier reference file
  - Returns: JSON with output filename

### Nectar Dashboard
- **POST** `/analyze-nectar` - Process Nectar CPG dashboard data
  - `byzzer_report` (Excel): Byzzer Excel report
  - `vip_report` (Excel): VIP Excel report
  - Optional reference files: `pricing_sheet`, `mandate_list`, `byzzer_market_map`
  - Returns: JSON with output filename

### File Download
- **GET** `/files/{filename}` - Download processed files

## 🛠️ Tools

### BBB Normalizer (`tools/bbb_normalizer.py`)
- Processes purchase log data with supplier matching
- Uses fuzzy matching for item identification
- Creates 4 output sheets:
  - Purchase Log
  - Item Totals
  - Supplier Totals
  - Confidence Dashboard

### Nectar Dashboard (`tools/nectar_dashboard.py`)
- Processes CPG dashboard data from Byzzer and VIP reports
- Supports optional reference files for enhanced analysis
- Calculates metrics like rate of sale, fulfillment percentages, and revenue

## 🔧 Utilities (`utils/file_utils.py`)

Shared utility functions for:
- File reading (Excel, CSV)
- Date parsing and normalization
- Column name normalization
- File saving and cleanup
- Output filename generation

## 📝 Example Usage

### BBB Processing
```python
import requests

files = {
    'bev_file': open('60_bev.csv', 'rb'),
    'supplier_file': open('supplier_list.xlsx', 'rb')
}

response = requests.post('http://localhost:8000/analyze', files=files)
result = response.json()
filename = result['filename']

# Download the processed file
download_response = requests.get(f'http://localhost:8000/files/{filename}')
with open('output.xlsx', 'wb') as f:
    f.write(download_response.content)
```

### Nectar Processing
```python
import requests

files = {
    'byzzer_report': open('byzzer_report.xlsx', 'rb'),
    'vip_report': open('vip_report.xlsx', 'rb')
}

response = requests.post('http://localhost:8000/analyze-nectar', files=files)
result = response.json()
filename = result['filename']
```

## 🔒 CORS Configuration

The API is configured to allow all origins for development. For production, update the CORS middleware in `main.py` to restrict origins.

## 📊 Logging

The application uses Python's logging module with INFO level. All operations are logged for debugging and monitoring purposes. 