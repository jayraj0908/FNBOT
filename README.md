# Trust Bodhi - Multi-Client Data Processing Platform

A modern, modular platform for processing client data with multiple normalization tools.

## 📁 Project Structure

```
FNBOT/
├── backend/                    # FastAPI Backend (Refactored)
│   ├── main.py                # API router
│   ├── tools/                 # Client-specific tools
│   │   ├── bbb_normalizer.py  # BBB Purchase Log processing
│   │   └── nectar_dashboard.py # Nectar CPG dashboard processing
│   ├── utils/                 # Shared utilities
│   │   └── file_utils.py      # File operations & helpers
│   ├── files/                 # Output directory
│   └── requirements.txt       # Python dependencies
├── trust-bodhi-app/           # Next.js Frontend
│   ├── src/                   # Source code
│   ├── pages/                 # Next.js pages
│   └── package.json           # Frontend dependencies
├── test_files/                # Test data files
└── .venv/                     # Python virtual environment
```

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python start_server.py
```

### Frontend Setup
```bash
cd trust-bodhi-app
npm install
npm run dev
```

## 🔌 API Endpoints

- `GET /health` - Health check
- `POST /analyze` - BBB file processing
- `POST /analyze-nectar` - Nectar dashboard processing
- `GET /files/{filename}` - File download
- `GET /docs` - API documentation

## 🛠️ Tools

### BBB Normalizer
- Processes purchase log data with supplier matching
- Creates 4 output sheets: Purchase Log, Item Totals, Supplier Totals, Confidence Dashboard
- Uses fuzzy matching for item identification

### Nectar Dashboard
- Processes CPG dashboard data from Byzzer and VIP reports
- Supports optional reference files for enhanced analysis
- Calculates metrics like rate of sale, fulfillment percentages, and revenue

## 📊 Features

- ✅ **Modular Architecture** - Clean separation of concerns
- ✅ **Multiple Client Tools** - BBB and Nectar processing
- ✅ **Shared Utilities** - Common file operations
- ✅ **Production Ready** - Proper error handling and logging
- ✅ **API Documentation** - Interactive Swagger UI
- ✅ **CORS Enabled** - Frontend integration ready

## 🔧 Development

The project uses:
- **Backend**: FastAPI with Python 3.11+
- **Frontend**: Next.js with TypeScript
- **Data Processing**: Pandas, OpenPyXL
- **File Matching**: FuzzyWuzzy

## 📝 License

This project is proprietary and confidential. 