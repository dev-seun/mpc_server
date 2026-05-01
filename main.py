
import json
import os 
from tools import mcp
from helper_functions import BASE_DIR, load_data
from infers import  logger 

def main():  
    load_data()
    logger.info("Data loaded at startup.")
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
    # mcp.run(transport="sse")
    
if __name__ == "__main__":
    main()
    