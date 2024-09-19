from flask import Flask, request
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
import graph
from pydantic import BaseModel

app = Flask(__name__)

chat = graph.get_app()

@app.route("/chat/")
async def get_response():
    data = request.json

    essay = data.get('input')

    response = chat.invoke({"essay": essay})
    return f"Score: {response["score"]}\n\nRationale: {response["rationale"]}\n\nSuggestions for improvement: {response["generations"]}"

if __name__ == "__main__":
    app.run(debug=True)