import sys
import os
import logging
import asyncio
from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

print("Starting imports...", file=sys.stderr)
print("All imports completed", file=sys.stderr)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("math_server")

# Initialize FastAPI app
app = FastAPI(
    title="Math MCP Server",
    description="A FastAPI server that provides math operations",
    version="0.1.0"
)

# Pydantic models for request/response
class MathOperation(BaseModel):
    a: int
    b: int

class MathResult(BaseModel):
    result: int
    operation: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to Math MCP Server!", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/add", response_model=MathResult)
async def add_endpoint(operation: MathOperation):
    """Add two numbers together."""
    try:
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = operation.a + operation.b
        logger.info(f"add({operation.a}, {operation.b}) = {result}")
        return MathResult(result=result, operation=f"{operation.a} + {operation.b}")
    except Exception as e:
        logger.error(f"Error in add operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/subtract", response_model=MathResult)
async def subtract_endpoint(operation: MathOperation):
    """Subtract second number from first number."""
    try:
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = operation.a - operation.b
        logger.info(f"subtract({operation.a}, {operation.b}) = {result}")
        return MathResult(result=result, operation=f"{operation.a} - {operation.b}")
    except Exception as e:
        logger.error(f"Error in subtract operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multiply", response_model=MathResult)
async def multiply_endpoint(operation: MathOperation):
    """Multiply two numbers together."""
    try:
        await asyncio.sleep(0.1)  # Small delay to demonstrate async
        result = operation.a * operation.b
        logger.info(f"multiply({operation.a}, {operation.b}) = {result}")
        return MathResult(result=result, operation=f"{operation.a} * {operation.b}")
    except Exception as e:
        logger.error(f"Error in multiply operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoints for simple operations (easier to test)
@app.get("/add/{a}/{b}")
async def add_get(a: int, b: int):
    """Add two numbers via GET request."""
    try:
        result = a + b
        logger.info(f"add({a}, {b}) = {result}")
        return {"result": result, "operation": f"{a} + {b} = {result}"}
    except Exception as e:
        logger.error(f"Error in add operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/subtract/{a}/{b}")
async def subtract_get(a: int, b: int):
    """Subtract two numbers via GET request."""
    try:
        result = a - b
        logger.info(f"subtract({a}, {b}) = {result}")
        return {"result": result, "operation": f"{a} - {b} = {result}"}
    except Exception as e:
        logger.error(f"Error in subtract operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/multiply/{a}/{b}")
async def multiply_get(a: int, b: int):
    """Multiply two numbers via GET request."""
    try:
        result = a * b
        logger.info(f"multiply({a}, {b}) = {result}")
        return {"result": result, "operation": f"{a} * {b} = {result}"}
    except Exception as e:
        logger.error(f"Error in multiply operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/docs")
async def get_docs():
    """Redirect to FastAPI auto-generated docs."""
    return {"message": "Visit /docs for interactive API documentation"}

def main():
    """Main entry point for the Math server."""
    try:
        print("Starting Math server...", file=sys.stderr)
        
        # Get port from environment variable (Render sets this)
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"  # Bind to all interfaces for Render
        
        logger.info(f"Server starting on {host}:{port}")
        print(f"About to run uvicorn on {host}:{port}...", file=sys.stderr)
        
        # Run as a web service using uvicorn
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