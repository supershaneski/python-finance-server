# python-finance-server

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![yfinance](https://img.shields.io/badge/yfinance-v0.2.66-green)](https://github.com/ranaroussi/yfinance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight server built with Python's built-in `http.server` and powered by the [`yfinance`](https://github.com/ranaroussi/yfinance) library. This project fetches real-time and fundamental stock ticker data (company info, price, ratios, analyst ratings, etc.) via a simple REST-like API.

---

Python の組み込みモジュール `http.server` を使用して構築された軽量な **Backend For Frontend (BFF)** サーバーで、`yfinance`￼ ライブラリによって動作します。このプロジェクトは、シンプルな REST 風 API を通じて、リアルタイムおよび基本的な株式ティッカー情報（企業情報、株価、各種比率、アナリスト評価など）を取得します。

### Main Goal / 主な目的

Learn how to use `yfinance` effectively while building a clean, cache-aware microservice that serves as a **Backend For Frontend (BFF)** for a client application. The server provides a simple, consistent API for stock ticker data, optimizes response times with caching, and allows the client app to focus on presentation and interaction logic.

---

`yfinance` を効果的に活用しつつ、クライアントアプリ向けの **Backend For Frontend (BFF)** として機能する、クリーンでキャッシュ対応のマイクロサービスを構築する方法を学ぶことが主な目的です。このサーバーは、株式ティッカー情報のシンプルで一貫性のある API を提供し、キャッシュによってレスポンス速度を最適化し、クライアントアプリは表示や操作に集中できる設計になっています。

### Features

* **Simple HTTP API**:

  * Single ticker: `GET /ticker?id=AAPL`
  * Multi-tickers: `GET /tickers?symbols=AAPL,MSFT`
* **Caching**: 10-minute in-memory cache (configurable TTL)
* **Consistent JSON responses** keyed by ticker symbol (`{ SYMBOL: {...} }`)
* **Zero dependencies** beyond `yfinance`

### API Endpoint

#### `GET /ticker?id=<TICKER>`

**Notes:** Only supports a single ticker. Returns JSON keyed by symbol.

**Example:**
```
http://localhost:8000/ticker?id=MSFT
```

**Sample Response:**
```json
{
  "MSFT": {
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
    },
    "metadata": {
      "cachedAt": "2025-11-15T09:00:00Z",
      "lastTradeAt": "2025-11-15T06:00:00Z",
      "marketState": "closed"
    }
  }
}
```

**Error Example:**
```json
{ "error": "No data found for ticker 'INVALID'" }
```

---

#### `GET /tickers?symbols=<TICKER1,TICKER2,...>`

**Notes:** Supports multiple comma-separated tickers. Returns JSON keyed by symbol.

**Example:**

```
http://localhost:8000/tickers?symbols=AAPL,MSFT
```

**Sample Response:**

```json
{
  "AAPL": { ... },
  "MSFT": { ... }
}
```

**Error Example (per ticker):**

```json
{
  "AAPL": { ... },
  "INVALID": { "error": "No data found for ticker 'INVALID'" }
}
```

### Setup

1. **Clone or download this project**
    ```sh
    git clone https://github.com/<yourname>/python-finance-server.git
    cd python-finance-server
    ```

2. **Create and activate Virtual Environment**:
   ```sh
   python3 -m venv venv

   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows
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
   copy .env.example .env  # Windows
   ```

   Set the server port you want to use:
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
curl "http://localhost:8000/ticker?id=AAPL"
curl "http://localhost:8000/tickers?symbols=AAPL,MSFT"
```

**Javascript / Fetch**
```js
fetch('http://localhost:8000/ticker?id=AAPL')
  .then(r => r.json())
  .then(data => console.log(data));

fetch('http://localhost:8000/tickers?symbols=AAPL,MSFT')
  .then(r => r.json())
  .then(data => console.log(data));
```

---