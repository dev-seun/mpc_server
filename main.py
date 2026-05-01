from tools import mcp
import os

def main():
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
    
if __name__ == "__main__":
    main()
    