# python-finance-server

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![yfinance](https://img.shields.io/badge/yfinance-v0.2.66-green)](https://github.com/ranaroussi/yfinance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight server built with Python's built-in `http.server` and powered by the [`yfinance`](https://github.com/ranaroussi/yfinance) library. This project fetches real-time and fundamental stock ticker data (company info, price, ratios, analyst ratings, etc.) via a simple REST-like API.

**Main Goal**: Learn how to use `yfinance` effectively while building a clean, cache-aware, microservice.

---

Python の組み込みモジュール `http.server` を使用して構築された軽量な **Backend For Frontend (BFF)** サーバーで、`yfinance`￼ ライブラリによって動作します。このプロジェクトは、シンプルな REST 風 API を通じて、リアルタイムおよび基本的な株式ティッカー情報（企業情報、株価、各種比率、アナリスト評価など）を取得します。

**主な目的**：`yfinance` を効果的に活用しながら、クリーンでキャッシュ対応のマイクロサービスを構築する方法を学ぶこと。

### Features

- **Simple HTTP API**: `GET /ticker?id=AAPL`
- **Caching**: 10-minute in-memory cache (configurable TTL)
- **Clean JSON responses** with structured financial data
- **Zero dependencies** beyond `yfinance`

### API Endpoint

#### `GET /ticker?id=<TICKER>`

**Example:**
```
http://localhost:8000/ticker?id=MSFT
```

**Sample Response:**
```json
{
  "company": {
    "name": "Microsoft Corporation",
    "symbol": "MSFT",
    "industry": "Software—Infrastructure",
    "sector": "Technology"
  },
  "market": {
    "currentPrice": 378.91,
    "previousClose": 376.02,
    "fiftyTwoWeekRange": "309.42 - 384.52",
    "marketCap": 2814592000000
  },
  "performance": {
    "trailingPE": 36.81,
    "forwardPE": 32.15,
    "dividendYield": 0.0079,
    "earningsGrowth": 0.187,
    "revenueGrowth": 0.152
  },
  "analyst": {
    "recommendation": "buy",
    "targetMeanPrice": 415.24
  }
}
```

**Error Example:**
```json
{ "error": "No data found for ticker 'INVALID'" }
```

### Setup

1. **Clone or download this project**
    ```sh
    git clone https://github.com/supershaneski/python-finance-server.git
    cd python-finance-server
    ```

2. **Create and activate Virtual Environment**:
   ```sh
   python3 -m venv venv
   ```

   - Linux/macOS:
    ```sh
    source venv/bin/activate
    ```
   - Windows:
    ```sh
    venv\Scripts\activate
    ```
   To deactivate

   ```sh
   deactivate
   ```
  
   **Note:** Use `python` instead of `python3` if your system defaults to Python 3.

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Setup the environment file**:
   
   Copy the example file `.env.example` to `.env` in the project root:
   ```sh
   cp .env.example .env  # Linux/macOS
   # or
   copy .env.example .env  # Windows
   ```

   Set the port you want to use
   ```env
   SERVER_PORT=8000
   ```

5. **Run the server**:
   ```sh
   python3 server.py
   ```

   Server starts at: `http://localhost:8000` (or your custom port)

### Example Usage

**curl**
```bash
curl "http://localhost:8000/ticker?id=TSLA"
```

**Javascript / Fetch**
```js
fetch('http://localhost:8000/ticker?id=AAPL')
  .then(r => r.json())
  .then(data => console.log(data));
```
