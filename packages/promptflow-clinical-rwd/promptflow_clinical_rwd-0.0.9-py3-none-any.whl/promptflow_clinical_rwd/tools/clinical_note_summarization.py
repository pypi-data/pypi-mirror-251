from promptflow import tool
from promptflow.connections import AzureOpenAIConnection
from typing import List


@tool
def summarize_notes(connection: AzureOpenAIConnection, notes: List[str]) -> List[str]:
    return notes
