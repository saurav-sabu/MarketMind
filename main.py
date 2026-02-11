import asyncio
import os
import sys
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MarketMind")

# Define instructions for the Finance Agent
FINANCE_AGENT_INSTRUCTIONS = """
You are an expert Financial Market Analyst with deep expertise in:
- Stock market analysis and technical indicators
- Fundamental analysis (P/E ratios, EPS, revenue, margins)
- Sector trends and competitive positioning
- Analyst recommendations and price targets
- Risk assessment and market sentiment
- Real-time market data interpretation

**Your Role:**
Provide comprehensive, actionable financial insights with:
1. **Real-time Market Data**: Current prices, volume, 52-week highs/lows, market cap
2. **Financial Deep-Dives**: P/E ratios, EPS, revenue growth, profit margins, debt levels
3. **Analyst Recommendations**: Consensus ratings, price targets, analyst opinions
4. **Sector Analysis**: Industry trends, competitive positioning, sector performance
5. **Risk Assessment**: Volatility, beta, key risk factors
6. **Investment Insights**: Clear, data-driven recommendations

**Output Format:**
- Use markdown formatting with clear sections
- Include emoji indicators (📈 📉 💰 📊 🔍 ⚠️) for visual clarity
- Present data in tables when appropriate
- Provide executive summary first, then detailed analysis
- Cite specific numbers and metrics
- End with actionable insights and recommendations

**Guidelines:**
- Always fetch the latest data using available tools
- Compare companies to their sector/industry when relevant
- Highlight both opportunities and risks
- Be concise but thorough
- Use professional financial terminology appropriately

**Stock Ticker Formats:**
- US Stocks: Use ticker directly (e.g., AAPL, TSLA, MSFT)
- Indian Stocks (NSE): Add .NS suffix (e.g., RELIANCE.NS, TCS.NS, INFY.NS)
- Indian Stocks (BSE): Add .BO suffix (e.g., RELIANCE.BO)
- Other exchanges: Use appropriate suffix (.L for London, .TO for Toronto, etc.)
"""

class FinanceAgent:
    """
    A class to represent a Finance Agent that can analyze stocks, sectors, and compare companies.
    """

    # Set of common Indian stock tickers to automatically append .NS suffix
    INDIAN_STOCKS = {
        'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'HDFC', 'ICICIBANK', 'BHARTIARTL',
        'SBIN', 'KOTAKBANK', 'LT', 'HINDUNILVR', 'ITC', 'AXISBANK', 'ASIANPAINT',
        'MARUTI', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'BAJFINANCE', 'WIPRO',
        'ONGC', 'TECHM', 'SUNPHARMA', 'NTPC', 'POWERGRID', 'INDUSINDBK', 'TATAMOTORS'
    }

    def __init__(self, model_id: str = "claude-sonnet-4-20250514", temperature: float = 0.3):
        """
        Initialize the FinanceAgent with a model and tools.
        
        Args:
            model_id (str): The ID of the model to use (default: Claude Sonnet 4).
            temperature (float): The temperature for the model (default: 0.3).
        """
        self.model = Claude(id=model_id, temperature=temperature)
        # Explicitly enable tools to ensure fresh data fetching
        self.yfinance_tools = YFinanceTools()

        self.agent = Agent(
            name="Finance Analyst",
            model=self.model,
            tools=[self.yfinance_tools],
            instructions=FINANCE_AGENT_INSTRUCTIONS,
            markdown=True
        )
        logger.info(f"FinanceAgent initialized with model: {model_id}")


    def _format_ticker(self, ticker: str) -> str:
        """
        Format the ticker symbol, appending .NS for known Indian stocks if no suffix is present.
        
        Args:
            ticker (str): The stock ticker symbol.
            
        Returns:
            str: The formatted ticker symbol.
        """
        ticker = ticker.upper().strip()

        if "." in ticker:
            return ticker
        
        if ticker in self.INDIAN_STOCKS:
            return f"{ticker}.NS"
        
        return ticker


    
    async def analyze(self, prompt: str) -> str:
        """
        Run the analysis using the agent.
        
        Args:
            prompt (str): The prompt to send to the agent.
            
        Returns:
            str: The analysis result or an error message.
        """
        try:
            logger.info(f"Starting analysis for prompt: {prompt[:50]}...")
            response = await self.agent.arun(prompt)
            return response.content
        
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return f"❌ Error during analysis: {str(e)}.\n\n Please check:\n Your API Key is set in .env (ANTHROPIC_API_KEY)\n- The stock ticker is valid\n- Your internet connection is active."
        

    async def analyze_company(self, ticker: str) -> str:
        """
        Analyze a specific company based on its ticker.
        
        Args:
            ticker (str): The stock ticker of the company.
            
        Returns:
            str: Comprehensive financial analysis of the company.
        """
        formatted_ticker = self._format_ticker(ticker)
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""
        Today is {current_date}.
        Provide a comprehensive financial analysis of {formatted_ticker}. Include:

        1. **Current Market Status**
           - Current price, volume, market cap (Data as of {current_date})
           - 52-week high/low
           - Day/Week/Month/Year performance

        2. **Financial Deep-Dive**
           - P/E ratio, EPS, revenue, profit margins
           - Balance sheet highlights (if available)
           - Growth trends

        3. **Analyst Recommendations**
           - Consensus rating
           - Price targets
           - Analyst opinions summary

        4. **Sector & Competitive Analysis**
           - Industry sector performance
           - Competitive positioning
           - Market share insights (if available)

        5. **Risk Assessment**
           - Beta, volatility
           - Key risk factors
           - Market sentiment

        6. **Investment Insights**
           - Key strengths and opportunities
           - Risks and concerns
           - Overall recommendation

        Format the response in clear markdown with sections and tables.
        """
        return await self.analyze(prompt)


    async def sector_analysis(self, sector: str) -> str:
        """
        Analyze a specific sector.
        
        Args:
            sector (str): The name of the sector to analyze.
            
        Returns:
            str: Analysis of the sector including trends, top performers, and opportunities.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        prompt = f"""
        Today is {current_date}.
        Analyze the {sector} sector. Include:
        
        1. **Sector Overview**
           - Overall sector performance
           - Key trends and drivers
        
        2. **Top Performers**
           - Leading companies in the sector
           - Market leaders analysis
        
        3. **Sector Trends**
           - Growth patterns
           - Market dynamics
           - Future outlook
        
        4. **Investment Opportunities**
           - Best positioned companies
           - Sector-specific risks
           - Recommendations
        
        Focus on actionable insights for investors.
        """

        return await self.analyze(prompt)
    

    async def compare_companies(self, tickers: list[str]) -> str:
        """
        Compare multiple companies.
        
        Args:
            tickers (list[str]): A list of stock tickers to compare.
            
        Returns:
            str: A side-by-side comparison of the companies.
        """
        formatted_tickers = [self._format_ticker(t) for t in tickers]
        ticker_list = ", ".join(formatted_tickers)
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""
        Today is {current_date}.
        Compare the following companies: {ticker_list}
        
        Provide a side-by-side comparison including:
        - Current market metrics (price, market cap, P/E ratio)
        - Financial performance (revenue, EPS, margins)
        - Growth trends
        - Analyst ratings
        - Risk profiles
        - Investment recommendation ranking
        
        Present in a clear comparative format with tables.
        """

        return await self.analyze(prompt)
    
async def interactive_session():
    """
    Start an interactive session for the user to query the Finance Agent.
    """
    agent = FinanceAgent()

    print("=" * 70)
    print("📊 MarketMind — AI Market Analyst")
    print("=" * 70)
    print("\n💡 Example queries:")
    print("  US Stocks:")
    print("    - 'Analyze AAPL'")
    print("    - 'Compare TSLA, NVDA, and AMD'")
    print("  Indian Stocks:")
    print("    - 'Analyze RELIANCE.NS' or 'Analyze RELIANCE'")
    print("    - 'Compare TCS.NS, INFY.NS, and WIPRO.NS'")
    print("    - 'Give me a deep dive on HDFCBANK.NS'")
    print("  General:")
    print("    - 'What's the outlook for the Technology sector?'")
    print("    - 'What are analyst recommendations for Apple?'")
    print("\n💡 Note: For Indian stocks, use .NS (NSE) or .BO (BSE) suffix.")
    print("   Common Indian stocks (RELIANCE, TCS, INFY) work without suffix too!")
    print("\nType 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("💼 Your query: ").strip()

            if not user_input:
                continue
            
            if user_input.lower() in ("exit","quit","q"):
                print("\n👋 Thank you for using Finance Agent. Goodbye!")
                break
            
            print("\n" + "─" * 70)
            print("🔍 Analyzing...\n")

            if user_input.lower().startswith("analyze "):
                ticker = user_input.replace("analyze","").strip()
                response = await agent.analyze_company(ticker)

            elif user_input.lower().startswith("compare "):
                tickers = [t.strip().upper() for t in user_input.replace("compare ","").split(",")]
                response = await agent.compare_companies(tickers)
            
            elif "sector" in user_input.lower() or "industry" in user_input.lower():
                sector = user_input.replace("sector","").replace("industry","").strip()

                if not sector or sector.lower() in ["the","for","of"]:
                    sector="Technology"

                response = await agent.sector_analysis(sector)
            else:
                response = await agent.analyze(user_input)

            print(response)
            print("\n" + "-" * 70 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Session error: {str(e)}")
            print(f"\n❌ Error: {str(e)}\n")


async def single_query(query: str):
    """
    Run a single query from the command line.
    
    Args:
        query (str): The query string to analyze.
    """
    agent = FinanceAgent()

    print("🔍 Analyzing...\n")
    response = await agent.analyze(query)
    print(response)


def main():
    """
    Main entry point of the script. 
    Checks for API key and runs either interactive session or single query based on arguments.
    """
    # specific fix for windows console encoding
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.critical("ANTHROPIC_API_KEY not found.")
        print("❌ Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please create a .env file with: ANTHROPIC_API_KEY=your_key_here") 
        sys.exit(1)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        asyncio.run(single_query(query))
    
    else:
        asyncio.run(interactive_session())


if __name__ == "__main__":
    main()
                
        
