from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import socketserver
import os
import time
import yfinance as yf

# Simple caching
cache = {}  # global dict: {ticker: (data, timestamp)}

def load_env():
    """Load environment variables from .env file."""
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                        except ValueError:
                            print(f"Warning: Skipping malformed .env line: {line}")
        except Exception as e:
            print(f"Warning: Failed to read .env file: {e}")

class FinanceDataError(Exception):
    """Custom exception for finance data retrieval errors."""
    pass

def get_stock_summary(symbol):
    print(f"Retrieve data from API: {symbol}")
    try:
        t = yf.Ticker(symbol)
        info = t.info
        if not info or "shortName" not in info:
            raise FinanceDataError(f"No data found for ticker '{symbol}'")

        return {
            "company": {
                "name": info.get("shortName"),
                "symbol": info.get("symbol"),
                "industry": info.get("industry"),
                "sector": info.get("sector"),
            },
            "market": {
                "currentPrice": info.get("currentPrice"),
                "previousClose": info.get("previousClose"),
                "fiftyTwoWeekRange": info.get("fiftyTwoWeekRange"),
                "marketCap": info.get("marketCap"),
            },
            "performance": {
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "dividendYield": info.get("dividendYield"),
                "earningsGrowth": info.get("earningsGrowth"),
                "revenueGrowth": info.get("revenueGrowth"),
            },
            "analyst": {
                "recommendation": info.get("recommendationKey"),
                "targetMeanPrice": info.get("targetMeanPrice"),
            },
        }
    
    except FinanceDataError:
        raise  # re-raise for upper handler
    except Exception as e:
        # Handle all other unexpected yfinance or network errors
        raise FinanceDataError(f"Failed to retrieve data for '{symbol}': {str(e)}")


def get_stock_summary_cached(symbol, ttl=600):
    now = time.time()
    if symbol in cache:
        data, ts = cache[symbol]
        if now - ts < ttl:
            print(f"Retrieve data from cache: {symbol}")
            return data
    
    data = get_stock_summary(symbol)
    cache[symbol] = (data, now)
    return data

# Load environment variables
load_env()

class SimpleRESTServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for the web interface and message history."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)  # parse query string into dict

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'error',
                'code': 404,
                'message': 'Invalid API endpoint.',
                'available_endpoints': [
                    '/api/ticker'
                ]
            }).encode())
        
        elif path == '/ticker':
            # Support both: ?id=AAPL and ?symbols=AAPL,MSFT
            symbols_param = query.get('symbols', [None])[0] or query.get('id', [None])[0]
            
            if not symbols_param:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'symbols' or 'id'"}).encode())
                return
            
            symbols = [s.strip().upper() for s in symbols_param.split(',') if s.strip()]
            if not symbols:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No valid symbols"}).encode())
                return
            
            results = {}
            for symbol in symbols:
                try:
                    data = get_stock_summary_cached(symbol)
                    # data = {"error": "Error test"}
                    results[symbol] = data
                except FinanceDataError as e:
                    results[symbol] = {"error": str(e)}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        
        else:
            self.send_error(404, 'Not found')
    
    # Handles error response
    def send_error(self, code, message):
        """Send an error response with a JSON body."""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode())

def run(server_class=HTTPServer, handler_class=SimpleRESTServer, port=8000):
    """Start the HTTP server."""
    # Get port from environment variable, fallback to default
    port = int(os.environ.get('SERVER_PORT', port))

    socketserver.TCPServer.allow_reuse_address = True
    server_address = ('', port)
    try:
        httpd = server_class(server_address, handler_class)
        print(f'Starting Sample Finance Server on http://localhost:{port}/...')
        httpd.serve_forever()
    except OSError as e:
        print(f"Error: Could not start server on port {port}: {e}")
        print("Try a different port by setting SERVER_PORT in the .env file.")
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
    finally:
        print("Server stopped.")

if __name__ == '__main__':
    run()
