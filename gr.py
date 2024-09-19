import gradio as gr
from langserve import RemoteRunnable
import requests

def get_response(input):
    url = "http://localhost:5000/chat/"

    try:
        data = {"input": input}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.get(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            return "There was an error"
    except requests.exceptions.RequestException as e:
        return e

iface = gr.Interface(
            fn=get_response,
            inputs=gr.Textbox(
                value="Enter your question"
            ),
            outputs="textbox",
            title="GRE Analytical Writing Essay Grader",
            theme=gr.themes.Soft(),
            allow_flagging="never",
            examples=[
                "Give me a Quantitative Reasoning question that uses the concept of the Normal distribution",
                "Give me a Critical Reasoning question as well as its accompanying reading section"
            ]
)

iface.launch(share=True)