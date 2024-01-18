from promptflow import tool
from typing import List


@tool
def summarize_notes(notes: List[str]) -> List[str]:
    return notes
