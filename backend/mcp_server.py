from mcp.server import MCPServer

app = MCPServer()


@app.tool()
def get_brand_colors(brand: str) -> dict:
    """Returns official brand hex colours from Azure Blob"""
    return {"primary": "#0078D4", "accent": "#5E06FF"}


@app.tool()
def save_slide_asset(filename: str, data: bytes) -> str:
    """Saves a generated asset to Azure Blob Storage"""
    return f"https://storage.blob.core.windows.net/assets/{filename}"
