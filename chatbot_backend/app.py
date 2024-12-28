import asyncio
from queue import Queue
from threading import Thread
from dotenv import load_dotenv

from langchain.schema.messages import HumanMessage
from langchain_openai import ChatOpenAI
from llm_streaming import LLMStreamingHandler 

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

load_dotenv()

llm_response_queue = Queue()
cbhandler = LLMStreamingHandler(llm_response_queue)

llm = ChatOpenAI(streaming=True, callbacks=[cbhandler], temperature=0.7)

def generate(query):
    llm.invoke([HumanMessage(content=query)])

def start_generation(query):
    thread = Thread(target=generate, kwargs={"query": query})
    thread.start()

async def response_generator(query):
    start_generation(query)
    while True:
        value = llm_response_queue.get()
        if value == None:
            break
        yield value
        llm_response_queue.task_done()
        await asyncio.sleep(0.01)


"""
This is the FastAPI part of the code that is run when the script is run as a service.

Run it with the following commands: 
- fastapi run app.py
- uvicorn app:app --reload --port 8000

You can query the interface with a browser at 
http://localhost:8000/query-stream/?query="Your query here"
"""
app = FastAPI()

@app.get("/query-stream/")
async def stream(query: str):
    print(f"Query: {query}")
    return StreamingResponse(response_generator(query), media_type="text/event-stream")

"""
This is the cli part of the code that is run when the script is run as a standalone script.
"""
"""
async def main(bstream):
    
    query = "Was waren die wichtigsten Ereignisse im Jahr 2021?"

    if bstream == True:
        async for value in response_generator(query):
            print(value)
    else:
        result = llm.invoke([HumanMessage(content=query)])
        print ("Result: ", result.content)

asyncio.run(main(True))
"""


