# Function call service
a demo for llm function call
Please taking these requirement to get the results:
1. ``pip install requirements.txt``
2. ``In function_call_api.py, change variable apy_key to your actual openai api key``\
And then, run these command to get the results:
3. `` uvicorn very_simple_api:app --port 8090 ``
4. `` http POST http://127.0.0.1:8090/content content="What services do you provide?"``
