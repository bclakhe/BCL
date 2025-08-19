import sys
import fastapi
import os

print("Starting imports...", file=sys.stderr)

try:
    from mcp.server.fastmcp import FastMCP
    print("FastMCP import successful", file=sys.stderr)
except ImportError as e:
    print(f"FastMCP import failed: {e}", file=sys.stderr)

import logging
import asyncio
from typing import Annotated, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import traceback

print("All imports completed", file=sys.stderr)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("math_server")

# Initialize FastMCP server with stateless HTTP for better deployment
mcp = FastMCP(
    "Math",
    stateless_http=True
)

@mcp.tool()
async def add(
    a: Annotated[int, "First number to add"],
    b: Annotated[int, "Second number to add"]
) -> int:
    """Add two numbers together."""
    try:
        # Simulate some async operation
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = a + b
        logger.info(f"add({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in add operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.tool()
async def sub(
    a: Annotated[int, "Number to subtract from"],
    b: Annotated[int, "Number to subtract"]
) -> int:
    """Subtract second number from first number."""
    try:
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = a - b
        logger.info(f"sub({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in sub operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.tool()
async def multiply(
    a: Annotated[int, "First number to multiply"],
    b: Annotated[int, "Second number to multiply"]
) -> int:
    """Multiply two numbers together."""
    try:
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = a * b
        logger.info(f"multiply({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in multiply operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.prompt()
async def Add_Prompt(
    a: Annotated[int, "First number to add"],
    b: Annotated[int, "Second number to add"]
) -> str:
    """Prompt to add two numbers."""
    await asyncio.sleep(0.1)  # Small delay to demonstrate async
    prompt = f"Add {a} and {b}."
    logger.info(f"Add_Prompt({a}, {b}) -> {prompt}")
    return prompt

@mcp.prompt()
async def Sub_Prompt(
    a: Annotated[int, "Number to subtract from"],
    b: Annotated[int, "Number to subtract"]
) -> str:
    """Prompt to subtract two numbers."""
    await asyncio.sleep(0.1)  # Small delay to demonstrate async
    prompt = f"Subtract {b} from {a}."
    logger.info(f"Sub_Prompt({a}, {b}) -> {prompt}")
    return prompt

@mcp.prompt()
async def Multiply_Prompt(
    a: Annotated[int, "First number to multiply"],
    b: Annotated[int, "Second number to multiply"]
) -> str:
    """Prompt to multiply two numbers."""
    await asyncio.sleep(0.1)  # Small delay to demonstrate async
    prompt = f"Multiply {a} and {b}."
    logger.info(f"Multiply_Prompt({a}, {b}) -> {prompt}")
    return prompt

async def print_registered_tools():
    """Print the list of registered tools asynchronously."""
    try:
        tools = await mcp.list_tools()
        print("Registered tools:", tools)
        return tools
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def create_app():
    """Create FastAPI app with mounted MCP server."""
    # Create FastAPI app with proper lifespan management
    app = FastAPI(
        title="Math MCP Server", 
        description="A FastAPI server that provides math operations through MCP",
        version="0.1.0",
        lifespan=lambda app: mcp.session_manager.run()
    )

    # Add health check endpoint
    @app.get("/")
    async def root():
        return {"message": "Math MCP Server is running", "mcp_endpoint": "/math/mcp"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "Math MCP Server is running"}

    # Mount the MCP server - the actual MCP endpoint will be at /math/mcp
    app.mount("/math", mcp.streamable_http_app())
    
    return app

def main():
    """Main entry point for the Math MCP server."""
    try:
        print("Starting Math MCP server...", file=sys.stderr)
        
        # Get port from environment variable (Render provides this)
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"  # Bind to all interfaces for Render
        
        # Log server startup using standard logging
        logger.info(f"Server starting on {host}:{port}")
        print(f"About to start server on {host}:{port}...", file=sys.stderr)
        print(f"MCP endpoint will be available at: http://{host}:{port}/math/mcp", file=sys.stderr)
        
        # Create the FastAPI app with mounted MCP server
        app = create_app()
        
        # Run uvicorn directly with full control over host and port
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()