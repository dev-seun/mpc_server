import asyncio
from urllib import response

import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
load_dotenv()

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPEN_ROUTER_URL=os.getenv("OPEN_ROUTER_URL", "https://openrouter.ai/api/v1")

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI



client = MultiServerMCPClient({
    "weather": {
        "url": "http://127.0.0.1:8000",
        "transport": "stdio",
        # "headers": {"Content-Type": "text/stream"}
    }
})

async def get_agent(): 
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENROUTER_API_KEY, base_url=OPEN_ROUTER_URL)
    tools = await client.get_tools()

    agent =  create_react_agent(llm, tools)
    return agent
 
async def main():
    agent = await get_agent()
    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "Get weather forecast for 40.7128, -74.0060"}
        ]
    })
    print("Agent response: ---------------")
    print(response)
    print("End Agent response: ---------------")
    return response


if __name__ == "__main__": 
    asyncio.run(main())