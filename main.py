
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date
from analysis_crew import run_financial_analysis
from typing import Dict, Any
import markdown, os


# Initialize the FastAPI app
app = FastAPI(
    title="Financial Analysis API",
    description="An API to perform financial analysis on a stock using a multi-agent system.",
    version="1.0.0"
)

# Pydantic model for request body validation
class StockAnalysisRequest(BaseModel):
    stock_selection: str
    date_analysis: date = date.today() # Optional: defaults to today's date

# Define the root endpoint for health checks
@app.get("/", tags=["Health Check"])
async def read_root():
    return {"status": "API is running"}

# Define the main analysis endpoint
@app.post("/analyze", tags=["Analysis"])
async def analyze_stock(request: StockAnalysisRequest):
    """
    Accepts a stock symbol and returns a financial analysis report.
    """
    try:
        print(f"🚀 Kicking off analysis for: {request.stock_selection}")
        # Call the refactored crew logic
        result = run_financial_analysis(
            stock_selection=request.stock_selection,
            date=request.date_analysis.strftime("%m/%d/%Y") # Format date as string for the crew
        )
        print("✅ Analysis completed successfully.")
        
        return {"analysis_result": result.raw}
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        # Raise an HTTP exception if anything goes wrong
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze", tags=["Analysis"])
async def analyze_stock(
    stock_selection: str = Query(..., description="The stock symbol to analyze (e.g., AAPL)"),
    date_analysis: date = Query(..., description="The date of analysis (format: YYYY-MM-DD, e.g., 2024-10-05)"),
):
    """
    Accepts a stock symbol and date via query parameters and returns a financial analysis report.
    """
    try:
        # 1. Convert the date object to the required string format for the backend logic
        date_str = date_analysis.strftime("%m/%d/%Y")
        
        # Define a consistent filename based on the inputs
        filename = f"{stock_selection}_{date_analysis.strftime('%Y%m%d')}_analysis.md"
        output_dir = "/home/financial-analysis-api/data" # Define a directory for saving files

        print(f"🚀 Kicking off GET analysis for: {stock_selection} on {date_str}. Output will be saved to '{os.path.join(output_dir, filename)}'")
        
        # 2. Call the refactored crew logic
        result = run_financial_analysis(
            stock_selection=stock_selection,
            date=date_str
        )
        
        # 3. Print the successful result
        print("✅ Analysis completed successfully. Saving result to file...")
        
        # --- NEW FILE SAVING LOGIC STARTS HERE ---
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        full_path = os.path.join(output_dir, filename)

        # Write the raw Markdown content to the file
        with open(full_path, "w", encoding="utf-8") as f:
            # We assume the result object has a .raw attribute containing the Markdown text
            f.write(result.raw) 
        
        print(f"💾 Result successfully saved to: {full_path}")
        
        # --- NEW FILE SAVING LOGIC ENDS HERE ---

        # 4. Process the result for the HTTP response
        html = markdown.markdown(result.raw)
        
        # FastAPI will return the HTML content
        return HTMLResponse(content=html, status_code=200)
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        # Raise an HTTP exception if anything goes wrong
        raise HTTPException(status_code=500, detail=str(e))