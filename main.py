from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import pandas as pd
import os
from datetime import datetime
from ml_logic import process_bev_to_vines, read_input_file, read_reference_file, is_bev_format
import logging
import io
import openpyxl
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    reference_file: Optional[UploadFile] = None
):
    """
    Analyze uploaded file and return processed data.
    Handles both Excel and CSV files with graceful error handling.
    Always returns a file, even if processing fails.
    """
    try:
        # Read file contents
        try:
            contents = await file.read()
            file_extension = file.filename.split('.')[-1].lower()
            logger.info(f"Processing file: {file.filename} with extension: {file_extension}")
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            output_stream = io.BytesIO()
            pd.DataFrame({'Error': [f"Failed to read file: {str(e)}"]}).to_excel(output_stream, index=False)
            output_stream.seek(0)
            return StreamingResponse(
                output_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
            )

        # Read and process input file
        try:
            df = read_input_file(contents, f".{file_extension}")
            
            # Normalize column headers
            df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
            logger.info(f"Normalized columns: {df.columns.tolist()}")
            
            # Verify basic structure
            if df.empty:
                output_stream = io.BytesIO()
                pd.DataFrame({'Error': ['File is empty']}).to_excel(output_stream, index=False)
                output_stream.seek(0)
                return StreamingResponse(
                    output_stream,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment; filename=empty_60vines.xlsx"}
                )
                
        except Exception as e:
            logger.error(f"Error processing input file: {str(e)}")
            output_stream = io.BytesIO()
            pd.DataFrame({'Error': [f"Failed to process file: {str(e)}"]}).to_excel(output_stream, index=False)
            output_stream.seek(0)
            return StreamingResponse(
                output_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
            )

        # Read reference file if provided
        reference_maps = {}
        if reference_file:
            try:
                ref_contents = await reference_file.read()
                ref_extension = reference_file.filename.split('.')[-1].lower()
                ref_df = read_reference_file(ref_contents, f".{ref_extension}")
                
                # Normalize reference file columns
                ref_df.columns = [str(col).strip().lower().replace(" ", "_") for col in ref_df.columns]
                
                # Create reference maps
                reference_maps = {
                    'item_standard': dict(zip(ref_df['item_norm'], ref_df['item'])),
                    'store': dict(zip(ref_df['store_norm'], ref_df['store'])),
                    'vendor': dict(zip(ref_df['vendor_norm'], ref_df['vendor'])),
                    'pack_size': dict(zip(ref_df['item_norm'], ref_df['pack_size'])),
                    'case_size': dict(zip(ref_df['item_norm'], ref_df['case_size'])),
                    'category': dict(zip(ref_df['item_norm'], ref_df['category']))
                }
                logger.info("Reference maps created successfully")
                
            except Exception as e:
                logger.warning(f"Error processing reference file: {str(e)}")
                # Continue without reference data
                reference_maps = {}

        # Process the data
        try:
            # Create output buffer
            output_stream = io.BytesIO()
            
            # Process data and write to Excel
            with pd.ExcelWriter(output_stream, engine='openpyxl') as writer:
                summary = process_bev_to_vines(df, writer)
            
            # Reset buffer position
            output_stream.seek(0)
            
            # Return the processed file
            return StreamingResponse(
                output_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=output_60vines.xlsx"}
            )
            
        except Exception as e:
            logger.error(f"Error during data processing: {str(e)}")
            output_stream = io.BytesIO()
            pd.DataFrame({'Error': [f"Error processing data: {str(e)}"]}).to_excel(output_stream, index=False)
            output_stream.seek(0)
            return StreamingResponse(
                output_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in /analyze: {str(e)}")
        output_stream = io.BytesIO()
        pd.DataFrame({'Error': [f"Unexpected error: {str(e)}"]}).to_excel(output_stream, index=False)
        output_stream.seek(0)
        return StreamingResponse(
            output_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
        )

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download file with lenient filename validation."""
    try:
        # Basic filename sanitization
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        if not safe_filename:
            safe_filename = "output_60vines.xlsx"
            
        file_path = os.path.join("uploads", safe_filename)
        if not os.path.exists(file_path):
            output_stream = io.BytesIO()
            pd.DataFrame({'Error': ['File not found']}).to_excel(output_stream, index=False)
            output_stream.seek(0)
            return StreamingResponse(
                output_stream,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
            )
            
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=safe_filename
        )
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        output_stream = io.BytesIO()
        pd.DataFrame({'Error': [f"Error downloading file: {str(e)}"]}).to_excel(output_stream, index=False)
        output_stream.seek(0)
        return StreamingResponse(
            output_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=error_60vines.xlsx"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 