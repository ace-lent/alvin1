from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/add")
def add(a: float, b: float):
    return {"result": a + b}

@app.get("/subtract")
def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/multiply")
def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"result": a / b}

# Create a TestClient instance to use FastAPI without an ASGI server
client = TestClient(app)

if __name__ == "__main__":
    import http.server
    import socketserver

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split('?')[0]
            if path.startswith('/add') or path.startswith('/subtract') or path.startswith('/multiply') or path.startswith('/divide'):
                response = client.get(self.path)
                self.send_response(response.status_code)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(404)
                self.end_headers()

    PORT = 8000
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
