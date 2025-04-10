import os
from typing import Annotated
from openai import AsyncOpenAI, OpenAI
from fastapi import Depends

from dotenv import load_dotenv

load_dotenv()


def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )


def get_openai_client_sync() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )


OpenAIClientDep = Annotated[AsyncOpenAI, Depends(get_openai_client)]

SyncOpenAIClientDep = Annotated[OpenAI, Depends(get_openai_client_sync)]
