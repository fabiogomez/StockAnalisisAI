
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from analysis_crew import run_financial_analysis

# Initialize the FastAPI app
app = FastAPI(
    title="Financial Analysis API",
    description="An API to perform financial analysis on a stock using a multi-agent system.",
    version="1.0.0"
)

# Pydantic model for request body validation
class StockAnalysisRequest(BaseModel):
    stock_selection: str
    date: date = date.today() # Optional: defaults to today's date

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
            date=request.date.strftime("%m/%d/%Y") # Format date as string for the crew
        )
        print("✅ Analysis completed successfully.")
        return {"analysis_result": result}
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        # Raise an HTTP exception if anything goes wrong
        raise HTTPException(status_code=500, detail=str(e))