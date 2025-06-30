"""
Trust Bodhi Backend API
FastAPI server for processing client data with multiple tools.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import traceback
from tools.nectar_dashboard import normalize_nectar
from utils import file_cache

# Import tool modules
from tools.bbb_normalizer import normalize_bbb

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

@app.get("/")
async def root():
    """Root endpoint for basic API health check."""
    return {
        "message": "Trust Bodhi Backend API is running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for frontend."""
    return {
        "status": "healthy", 
        "message": "Trust Bodhi Backend API is running",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze")
async def analyze_bbb_files(
    bev_file: UploadFile = File(..., description="60 Bev CSV or XLSX file")
):
    """
    Analyze BBB files and return processed data.
    
    Accepts one file:
    - bev_file: 60 Bev CSV or XLSX
    
    Uses the master supplier list from test_files/60_Vines_Item_Supplier_List_Master.xlsx for supplier mapping.
    Returns JSON response with filename.
    """
    try:
        # Validate file type (allow CSV and XLSX)
        if not (bev_file.filename.lower().endswith('.csv') or bev_file.filename.lower().endswith('.xlsx')):
            raise HTTPException(status_code=400, detail="bev_file must be a CSV or XLSX file")
        
        # Save input file
        ext = bev_file.filename.split('.')[-1].lower()
        input_id = str(uuid.uuid4())[:8]
        input_path = os.path.join("files", f"input_bev_{input_id}.{ext}")
        with open(input_path, "wb") as f:
            f.write(await bev_file.read())
        
        # Use master supplier list
        master_supplier_path = os.path.join(os.path.dirname(__file__), "..", "test_files", "60_Vines_Item_Supplier_List_Master.xlsx")
        if not os.path.exists(master_supplier_path):
            raise HTTPException(status_code=500, detail=f"Master supplier list not found at: {master_supplier_path}")
        
        logger.info(f"Processing BBB file: {bev_file.filename} with master supplier list at: {master_supplier_path}")
        
        # Use BBB normalizer
        output_filename = normalize_bbb(input_path, master_supplier_path)
        logger.info(f"BBB file processed successfully: {output_filename}")
        return {"filename": output_filename}
    except HTTPException as e:
        logger.error(f"Error during BBB data processing: {e.detail}")
        raise
    except Exception as e:
        error_msg = f"Error during BBB data processing: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

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
async def get_file(filename: str):
    """
    Get processed file by filename for frontend download.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        FileResponse with the requested file
    """
    try:
        # Basic filename sanitization
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        if not safe_filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
            
        file_path = os.path.join("files", safe_filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=safe_filename
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 