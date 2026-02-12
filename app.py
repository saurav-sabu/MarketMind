"""
MarketMind - AI Market Analyst
This Streamlit application serves as the frontend for the Finance Agent.
It provides a chat interface for users to interact with the agent,
visualize stock data, and get market insights.
"""

import streamlit as st
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Import the FinanceAgent class from main.py
from main import FinanceAgent

# Load environment variables
load_dotenv()

# Configure the Streamlit page settings
st.set_page_config(
    page_title="MarketMind -- AI Market Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for the interface
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "initialized" not in st.session_state:
    st.session_state.initialized = False

async def get_agent_response(agent, user_input: str):
    """
    Asynchronously get response from the FinanceAgent.
    
    Args:
        agent: The initialized FinanceAgent instance.
        user_input (str): The user's query text.
        
    Returns:
        str: The agent's response or analysis result.
    """
    text = user_input.strip()
    if not text:
        return "Please enter a query"
    
    if text.lower().startswith("analyze "):
        ticker = text.replace("analyze","",1).strip()
        return await agent.analyze_company(ticker)
    
    if text.lower().startswith("compare "):
        ticker_str = text.replace("compare","",1).strip()
        tickers = [t.strip().upper() for t in ticker_str.replace(" and ",",").split(",")]
        return await agent.compare_companies(tickers)
    
    if "sector" in text.lower() or "industry" in text.lower():
        sector = text.replace("sector","").replace("industry","").strip()

        if not sector or sector.lower() in ("the","for","of"):
            sector="Technology"

        return await agent.sector_analysis(sector)

    return await agent.analyze(text)
    
@st.cache_resource
def initialize_agent():
    """
    Initialize the FinanceAgent.
    Cached to prevent re-initialization on every rerun.
    
    Returns:
        tuple: (agent instance, error message if any)
    """
    try:
        if not os.getenv("ANTHROPIC_API_KEY"):
            return None, "❌ Error: ANTHROPIC_API_KEY not found in environment variables."
        
        agent = FinanceAgent()
        return agent, None
    
    except Exception as e:
        return None, f"❌ Error initializing agent: {str(e)}"
    

# Sidebar Configuration
with st.sidebar:
    st.title("📊 MarketMind")
    st.markdown("---")
    
    st.subheader("ℹ️ About")
    st.markdown("""
    An AI-powered market analyst that provides:
    - 📈 Real-time stock market data
    - 💰 Financial deep-dives
    - 📊 Analyst recommendations
    - 🔍 Sector analysis
    - ⚠️ Risk assessment
    """)
    
    st.markdown("---")
    
    st.subheader("💡 Example Queries")
    example_queries = [
        "Analyze AAPL",
        "Compare TSLA, NVDA, and AMD",
        "What's the outlook for Technology sector?",
        "Analyze RELIANCE.NS",
        "Compare TCS.NS, INFY.NS, WIPRO.NS",
        "Give me a deep dive on Microsoft"
    ]
    
    for query in example_queries:
        if st.button(f"💬 {query}", key=f"example_{query}", use_container_width=True):
            st.session_state.example_query = query
    
    st.markdown("---")
    
    st.subheader("📝 Stock Ticker Formats")
    st.markdown("""
    - **US Stocks**: `AAPL`, `TSLA`, `MSFT`
    - **Indian Stocks (NSE)**: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`
    - **Indian Stocks (BSE)**: `RELIANCE.BO`
    - **Common Indian stocks** work without suffix too!
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Main Header Display
st.markdown('<h1 class="main-header">📊 MarketMind</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI Market Analyst | Real-time Stock Insights</p>', unsafe_allow_html=True)


# Initialize the agent if not already present
if st.session_state.agent is None:
    with st.spinner("🚀 Initializing MarketMind..."):
        agent, error = initialize_agent()

        if error:
            st.error(error)
            st.stop()

        st.session_state.agent = agent
        st.session_state.initialized=True

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle example queries clicked from sidebar
if "example_query" in st.session_state:
    user_query = st.session_state.example_query
    del st.session_state.example_query

    st.session_state.messages.append({"role":"user","content":user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(get_agent_response(st.session_state.agent,user_query))
                loop.close()

                st.markdown(response)
                st.session_state.messages.append({"role":"assistant","content":response})

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role":"assistant","content":error_msg})

    st.rerun()



# Chat Input Handling
if prompt := st.chat_input("Ask about stocks, companies, or market trends..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(get_agent_response(st.session_state.agent,prompt))

                loop.close()

                st.markdown(response)

                st.session_state.messages.append({"role":"assistant","content":response})

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}\n\nPlease check:\n- Your API key is set correctly\n- The stock ticker is valid\n- Your internet connection is active"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
# Footer Section
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>💡 <strong>Tip:</strong> Try asking about specific stocks, comparing companies, or analyzing sectors!</p>
        <p><strong>MarketMind</strong> — Powered by Agno Framework + Claude AI + YFinance</p>
    </div>
    """,
    unsafe_allow_html=True
)



