from fastmcp import FastMCP
from datetime import date
from analysis_crew import run_financial_analysis
import markdown
import os
import sys

# Configure UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Initialize the FastMCP server
mcp = FastMCP("Financial Analysis MCP Server")


@mcp.tool()
def analyze_stock(
    stock_selection: str,
    date_analysis: str = None,
    save_to_file: bool = False,
    output_dir: str = None
) -> str:
    """
    Performs a financial analysis on a stock using a multi-agent system.
    
    Args:
        stock_selection: The stock symbol to analyze (e.g., AAPL, MSFT, GOOGL)
        date_analysis: The date of analysis in format YYYY-MM-DD (e.g., 2024-10-05). 
                      If not provided, defaults to today's date.
        save_to_file: Whether to save the analysis result to a markdown file. Defaults to False.
        output_dir: Directory path to save the analysis file. If not provided and save_to_file is True,
                   defaults to "./data" directory.
    
    Returns:
        A markdown-formatted financial analysis report containing financial health score
        and intrinsic value calculation.
    """
    try:
        # Handle date conversion
        if date_analysis:
            # Parse the date string (YYYY-MM-DD format)
            date_obj = date.fromisoformat(date_analysis)
            date_str = date_obj.strftime("%m/%d/%Y")
        else:
            # Use today's date if not provided
            date_obj = date.today()
            date_str = date_obj.strftime("%m/%d/%Y")
        
        try:
            print(f"🚀 Kicking off analysis for: {stock_selection} on {date_str}")
        except UnicodeEncodeError:
            print(f"[START] Kicking off analysis for: {stock_selection} on {date_str}")
        
        # Call the refactored crew logic
        result = run_financial_analysis(
            stock_selection=stock_selection,
            date=date_str
        )
        
        try:
            print("✅ Analysis completed successfully.")
        except UnicodeEncodeError:
            print("[SUCCESS] Analysis completed successfully.")
        
        # Save to file if requested
        if save_to_file:
            # Determine output directory
            if output_dir is None:
                output_dir = "./data"
            
            # Define a consistent filename based on the inputs
            filename = f"{stock_selection}_{date_obj.strftime('%Y%m%d')}_analysis.md"
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            full_path = os.path.join(output_dir, filename)
            
            # Write the raw Markdown content to the file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(result.raw)
            
            try:
                print(f"💾 Result successfully saved to: {full_path}")
            except UnicodeEncodeError:
                print(f"[SAVED] Result successfully saved to: {full_path}")
        
        # Return the markdown result
        return result.raw
        
    except Exception as e:
        error_msg = f"Error occurred during analysis: {e}"
        try:
            print(error_msg)
        except UnicodeEncodeError:
            print(f"Error occurred during analysis: {str(e)}")
        raise Exception(error_msg)


@mcp.tool()
def analyze_stock_with_html(
    stock_selection: str,
    date_analysis: str = None
) -> str:
    """
    Performs a financial analysis on a stock and returns the result as HTML.
    
    Args:
        stock_selection: The stock symbol to analyze (e.g., AAPL, MSFT, GOOGL)
        date_analysis: The date of analysis in format YYYY-MM-DD (e.g., 2024-10-05).
                      If not provided, defaults to today's date.
    
    Returns:
        An HTML-formatted financial analysis report.
    """
    try:
        # Handle date conversion
        if date_analysis:
            date_obj = date.fromisoformat(date_analysis)
            date_str = date_obj.strftime("%m/%d/%Y")
        else:
            date_obj = date.today()
            date_str = date_obj.strftime("%m/%d/%Y")
        
        try:
            print(f"🚀 Kicking off analysis for: {stock_selection} on {date_str}")
        except UnicodeEncodeError:
            print(f"[START] Kicking off analysis for: {stock_selection} on {date_str}")
        
        # Call the refactored crew logic
        result = run_financial_analysis(
            stock_selection=stock_selection,
            date=date_str
        )
        
        try:
            print("✅ Analysis completed successfully.")
        except UnicodeEncodeError:
            print("[SUCCESS] Analysis completed successfully.")
        
        # Convert markdown to HTML
        html = markdown.markdown(result.raw)
        
        return html
        
    except Exception as e:
        error_msg = f"Error occurred during analysis: {e}"
        try:
            print(error_msg)
        except UnicodeEncodeError:
            print(f"Error occurred during analysis: {str(e)}")
        raise Exception(error_msg)


# Run the MCP server
if __name__ == "__main__":
    mcp.run("sse")