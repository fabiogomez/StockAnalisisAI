import os
import warnings
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Suppress warnings
warnings.filterwarnings('ignore')

def create_financial_crew(stock_selection, date):
    """
    Creates and configures the financial analysis crew.
    """
    # --- LOAD ENVIRONMENT VARIABLES ---
    # It's crucial to load API keys from environment variables
    # This makes your application secure and portable.
    serper_api_key = os.getenv("SERPER_API_KEY")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not all([serper_api_key, azure_api_key, azure_endpoint]):
        raise ValueError("One or more required API keys/endpoints are not set in environment variables.")

    os.environ["SERPER_API_KEY"] = serper_api_key

    # --- TOOLS ---
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    # --- LLM CONFIGURATION ---
    llm = LLM(
        model="azure/gpt-4.1",
        api_version='2025-01-01-preview',
        api_key=azure_api_key,
        base_url=azure_endpoint
    )

    # --- AGENTS ---
    finantial_analyst_agent = Agent(
        role="Financial Analyst",
        goal="Analyze the most valuable ratios and give a score for the company's financial health.",
        backstory="As a value investing specialist, you analyze financial ratios, income statements, and debt over the last 10 years to provide a clear financial health score. Your data-driven insights are the cornerstone of informed investment decisions.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=llm
    )

    intrinsic_value_agent = Agent(
        role="Intrinsic Value Calculator",
        goal="Calculate the intrinsic value for a given stock based on financial analysis.",
        backstory="You are an expert in valuation models. Using the data provided by the Financial Analyst, you calculate the intrinsic value of a stock to determine if it is under or overvalued.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool],
        llm=llm
    )

    # --- TASKS ---
    finantial_analyst_task = Task(
        description=(
            f"Analyze the most valuable financial ratios for the stock ({stock_selection}) as of the date ({date}). "
            "Use your value investor knowledge to provide a clear score for its financial health. "
            "Focus on profitability, debt, and liquidity."
        ),
        expected_output=(
            f"A detailed report with a final financial health score for ({stock_selection}). "
            "The report must describe the reason for the score, citing specific financial ratios."
        ),
        agent=finantial_analyst_agent,
    )

    intrinsic_value_development_task = Task(
        description=(
            f"Calculate the intrinsic value of the stock ({stock_selection}) based on the financial analysis provided."
        ),
        expected_output=(
            "A clear calculation of the intrinsic value per share for {stock_selection}, along with the valuation method used (e.g., DCF, PE ratio). Provide a summary of whether the stock appears undervalued, fairly valued, or overvalued at its current price."
        ),
        agent=intrinsic_value_agent,
    )

    # --- CREW DEFINITION ---
    financial_crew = Crew(
        agents=[finantial_analyst_agent, intrinsic_value_agent],
        tasks=[finantial_analyst_task, intrinsic_value_development_task],
        manager_llm=llm,
        process=Process.hierarchical,
        verbose=True
    )

    return financial_crew

def run_financial_analysis(stock_selection, date):
    """
    Runs the financial analysis crew and returns the result.
    """
    crew = create_financial_crew(stock_selection, date)
    inputs = {
        'stock_selection': stock_selection,
        'date': date,
    }
    result = crew.kickoff(inputs=inputs)
    return result