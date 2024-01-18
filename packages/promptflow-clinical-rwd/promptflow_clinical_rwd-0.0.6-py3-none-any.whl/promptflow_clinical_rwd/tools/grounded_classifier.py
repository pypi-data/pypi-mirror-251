from promptflow import tool
from typing import Any, Dict


@tool
def grounded_classifier(patient_summary: str, **kwargs) -> Dict[str, Any]:
    error = False
    answer = "C50"
    print(f"kwargs: {kwargs}")
    if "error" in kwargs:
        error = bool(kwargs["error"])
    if "answer" in kwargs:
        answer = str(kwargs["answer"])
    return {"prediction": answer, "error": error}
