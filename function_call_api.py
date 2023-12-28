from fastapi import FastAPI
from openai import OpenAI
import uvicorn
from pydantic import BaseModel

api_key = "your_openai_api_key"

logger = uvicorn.config.logger

app = FastAPI()

function_description = [{
    "name": "local_function",
    "description": "provide service list for user",
    "parameters": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "A question about services that provided",
            },
        },
        "required": ["content"],
    }
}
]

client = OpenAI(api_key=api_key)


class Content(BaseModel):
    content: str


@app.post("/content")
async def func(content: Content):
    content = content.content
    service_provided = meet_caller(content)
    return {"service provided": service_provided}


def local_function(content: str):
    logger.info(f"logger info"
                f"local_function called with content: \n{content}")
    return ["General cleaning", "Specialized cleaning"]


def meet_caller(user_prompt: str):
    function_caller = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        functions=function_description,
        function_call='auto'
    )

    function_maper = {
        "local_function": local_function
    }
    fist_choice = 0
    message = function_caller.choices[fist_choice].message
    function_called = message.function_call.name
    function_called = function_maper.get(function_called, None)
    if function_called is None:
        return
    service_provided = function_called(user_prompt)
    return service_provided

