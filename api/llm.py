import os
from dotenv import dotenv_values
from langchain_openai import AzureChatOpenAI
from models import *
from langchain_core.output_parsers import StrOutputParser

def get_llm():
    config = dotenv_values(".env")

    os.environ["OPENAI_API_VERSION"] = config["OPENAI_API_VERSION"]
    os.environ["AZURE_OPENAI_ENDPOINT"] = config["AZURE_OPENAI_ENDPOINT"]
    os.environ["AZURE_OPENAI_API_KEY"] = config["AZURE_OPENAI_API_KEY"]
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = config["AZURE_OPENAI_DEPLOYMENT"]
    os.environ["TAVILY_API_KEY"] = config["TAVILY_API_KEY"]

    return AzureChatOpenAI(deployment_name="test-gpt-deployment")

get_llm()