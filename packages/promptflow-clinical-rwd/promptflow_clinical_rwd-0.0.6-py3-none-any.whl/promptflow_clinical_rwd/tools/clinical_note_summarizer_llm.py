from jinja2 import Template
from promptflow import tool
from promptflow.connections import CustomConnection
from promptflow.contracts.types import PromptTemplate


@tool
def llm_summarizer(
    connection: CustomConnection, prompt: PromptTemplate, **kwargs
) -> str:
    # Customize your own code to use the connection and prompt here.
    rendered_prompt = Template(
        prompt, trim_blocks=True, keep_trailing_newline=True
    ).render(**kwargs)
    return rendered_prompt
