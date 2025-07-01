"""
Trust Bodhi Backend API
FastAPI server for processing client data with multiple tools.
"""

import os
import sys
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from io import BytesIO
import traceback
import pandas as pd

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.bbb_normalizer import BBBNormalizer
from utils.file_utils import generate_output_filename
from tools.nectar_dashboard import normalize_nectar
from utils import file_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trust Bodhi Backend API",
    description="API for processing client data with multiple normalization tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("files", exist_ok=True)

def clean_for_json(obj):
    """Clean object to ensure JSON safety by handling NaN and inf values"""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    elif pd.isna(obj):
        return None
    elif isinstance(obj, (int, float)):
        if pd.isna(obj) or pd.isinf(obj):
            return 0.0
        return obj
    else:
        return obj

@app.get("/")
async def root():
    """Root endpoint for basic API health check."""
    return {
        "message": "Trust Bodhi Backend API is running",
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for frontend."""
    return {
        "status": "healthy", 
        "message": "Trust Bodhi Backend API is running",
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.post("/analyze")
async def analyze_file(bev_file: UploadFile = File(...)):
    """
    Analyze BBB files and return processed data.
    
    Accepts one file:
    - bev_file: 60 Bev CSV or XLSX
    
    Uses the master supplier list from test_files/60_Vines_Item_Supplier_List_Master.xlsx for supplier mapping.
    Returns JSON response with filename.
    """
    try:
        logger.info(f"Processing BBB file: {bev_file.filename}")
        
        # Read the uploaded file
        file_content = await bev_file.read()
        
        # Process the file using BBB normalizer with master supplier list
        # Try multiple possible paths for the supplier reference file
        possible_paths = [
            "60_Vines_Item_Supplier_List_Master.xlsx",  # Root directory
            os.path.join("test_files", "60_Vines_Item_Supplier_List_Master.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files", "60_Vines_Item_Supplier_List_Master.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "60_Vines_Item_Supplier_List_Master.xlsx"),
            "/app/60_Vines_Item_Supplier_List_Master.xlsx",  # Railway container path
            "/app/test_files/60_Vines_Item_Supplier_List_Master.xlsx"  # Railway container path
        ]
        
        supplier_reference_file = None
        for path in possible_paths:
            if os.path.exists(path):
                supplier_reference_file = path
                logger.info(f"Found supplier reference file at: {path}")
                break
        
        if not supplier_reference_file:
            logger.error("Supplier reference file not found in any expected location")
            logger.error(f"Current working directory: {os.getcwd()}")
            logger.error(f"Available files: {os.listdir('.')}")
            if os.path.exists('test_files'):
                logger.error(f"test_files contents: {os.listdir('test_files')}")
            raise HTTPException(status_code=500, detail="Supplier reference file not found")
        
        bbb_normalizer = BBBNormalizer(supplier_reference_file)
        result = bbb_normalizer.normalize(file_content)
        
        logger.info(f"BBB file processed successfully: {result['filename']}")
        
        # Clean the result to ensure JSON safety
        cleaned_result = clean_for_json(result)
        
        return {
            "success": True,
            "filename": cleaned_result["filename"],
            "summary": cleaned_result["summary"]
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_bbb_file")
async def process_bbb_file(bev_file: UploadFile = File(...)):
    """
    Process BBB files - alias for /analyze endpoint for frontend compatibility.
    
    Accepts one file:
    - bev_file: 60 Bev CSV or XLSX
    
    Uses the master supplier list from test_files/60_Vines_Item_Supplier_List_Master.xlsx for supplier mapping.
    Returns JSON response with filename.
    """
    try:
        logger.info(f"Processing BBB file: {bev_file.filename}")
        
        # Read the uploaded file
        file_content = await bev_file.read()
        
        # Process the file using BBB normalizer with master supplier list
        # Try multiple possible paths for the supplier reference file
        possible_paths = [
            "60_Vines_Item_Supplier_List_Master.xlsx",  # Root directory
            os.path.join("test_files", "60_Vines_Item_Supplier_List_Master.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files", "60_Vines_Item_Supplier_List_Master.xlsx"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "60_Vines_Item_Supplier_List_Master.xlsx"),
            "/app/60_Vines_Item_Supplier_List_Master.xlsx",  # Railway container path
            "/app/test_files/60_Vines_Item_Supplier_List_Master.xlsx"  # Railway container path
        ]
        
        supplier_reference_file = None
        for path in possible_paths:
            if os.path.exists(path):
                supplier_reference_file = path
                logger.info(f"Found supplier reference file at: {path}")
                break
        
        if not supplier_reference_file:
            logger.error("Supplier reference file not found in any expected location")
            logger.error(f"Current working directory: {os.getcwd()}")
            logger.error(f"Available files: {os.listdir('.')}")
            if os.path.exists('test_files'):
                logger.error(f"test_files contents: {os.listdir('test_files')}")
            raise HTTPException(status_code=500, detail="Supplier reference file not found")
        
        bbb_normalizer = BBBNormalizer(supplier_reference_file)
        result = bbb_normalizer.normalize(file_content)
        
        logger.info(f"BBB file processed successfully: {result['filename']}")
        
        # Clean the result to ensure JSON safety
        cleaned_result = clean_for_json(result)
        
        return {
            "success": True,
            "filename": cleaned_result["filename"],
            "summary": cleaned_result["summary"]
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-nectar")
async def analyze_nectar(
    byzzer_report: UploadFile = File(..., description="Nielsen/Byzzer report (Excel)"),
    vip_report: UploadFile = File(..., description="VIP Distributor report (Excel)"),
    pricing_sheet: UploadFile = File(None),
    mandate_list: UploadFile = File(None, description="Optional: Custom mandate list (uses master file if not provided)"),
    byzzer_market_map: UploadFile = File(None),
):
    try:
        # Read required files
        byzzer_bytes = await byzzer_report.read()
        vip_bytes = await vip_report.read()

        # Read optional files if provided
        pricing_bytes = await pricing_sheet.read() if pricing_sheet else None
        mandate_bytes = await mandate_list.read() if mandate_list else None
        market_map_bytes = await byzzer_market_map.read() if byzzer_market_map else None

        references = {
            "pricing_sheet": pricing_bytes,
            "mandate_list": mandate_bytes,
            "byzzer_market_map": market_map_bytes,
        }

        result = normalize_nectar(byzzer_bytes, vip_bytes, references)
        # If result is a dict with 'filename', return just the filename string
        if isinstance(result, dict) and 'filename' in result:
            filename = result['filename']
        else:
            filename = str(result)
        return {"filename": filename}

    except Exception as e:
        logger.error(f"Error in /analyze-nectar: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to process files: {str(e)}")

@app.get("/files/{filename}")
async def download_file(filename: str):
    """
    Get processed file by filename for frontend download.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        FileResponse with the requested file
    """
    try:
        file_path = os.path.join("files", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(file_path, filename=filename)
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        # Get port from environment variable (for Railway)
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Starting server on port {port}")
        logger.info(f"Environment: PORT={os.environ.get('PORT', '8000')}")
        
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"ERROR: Failed to start server: {e}")
        sys.exit(1) 