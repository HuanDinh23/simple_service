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
    return {"response": service_provided}


def local_function(content: str):
    logger.info(f"logger info\n"
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
    function_called = message.function_call
    if function_called is None:
        return
    function_called = function_maper.get(function_called.name, None)
    service_provided = function_called(user_prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You answer the user's question with the `information`, "
                        f"say less than 3 sentence, and simplify your answer "
                        f" `information`: `{service_provided}` "},
            {"role": "user", "content": f"{user_prompt}"}
        ],
        seed=42,
    )
    response_message = response.choices[fist_choice].message.content
    return response_message


