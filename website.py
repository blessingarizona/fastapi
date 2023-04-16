from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
        <html>
            <head>
                <title>Welcome to TECH64</title>
            </head>
            <body>
                <h1>This is tech64 official web page</h1>
                <p>we welcome you to tech 64 official web page, where we believe in everything good<p>
            </body>
        </html>
    """
