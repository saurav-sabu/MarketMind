# 📊 MarketMind — AI Market Analyst

MarketMind is an AI-powered financial analysis assistant that delivers real-time stock insights, company deep-dives, sector analysis, and comparative evaluations across US and Indian markets.

Built using **Agno Framework + Claude AI + YFinance + Streamlit**, MarketMind combines live market data with intelligent AI-driven analysis to generate structured, data-backed financial insights.

---

## 🚀 Features

- 📈 Real-time stock data retrieval (Yahoo Finance)
- 🏢 Company fundamental analysis
- 📊 Stock comparison (multiple tickers)
- 🏭 Sector & industry analysis
- 💰 Analyst recommendations overview
- ⚠️ Risk & valuation insights
- 🌎 Supports US & Indian equities (NSE/BSE)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Claude (Anthropic)
- **Agent Framework:** Agno
- **Market Data:** Yahoo Finance (YFinanceTools)
- **Language:** Python 3.9+

---

## 📂 Project Structure

```

MarketMind/
│
├── app.py              # Streamlit frontend
├── main.py             # FinanceAgent logic
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
└── README.md

````

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/saurav-sabu/MarketMind.git
cd MarketMind
````

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## 💬 Example Queries

* `Analyze AAPL`
* `Compare TSLA, NVDA, AMD`
* `Analyze RELIANCE.NS`
* `Compare TCS.NS, INFY.NS, WIPRO.NS`
* `What's the outlook for the Technology sector?`
* `Give me a deep dive on Microsoft`

---

## 📝 Supported Ticker Formats

| Market      | Example             |
| ----------- | ------------------- |
| US Stocks   | AAPL, TSLA, MSFT    |
| NSE (India) | RELIANCE.NS, TCS.NS |
| BSE (India) | RELIANCE.BO         |

---

## 🧠 How It Works

1. User enters a query via Streamlit chat interface.
2. The FinanceAgent interprets the intent (analyze, compare, sector).
3. YFinanceTools fetch live financial data.
4. Claude AI processes the data and generates structured insights.
5. Results are displayed in a conversational format.

---

## 🔒 Disclaimer

MarketMind is for educational and informational purposes only.
It does not provide financial advice or investment recommendations.
Always conduct your own research before making investment decisions.

---
