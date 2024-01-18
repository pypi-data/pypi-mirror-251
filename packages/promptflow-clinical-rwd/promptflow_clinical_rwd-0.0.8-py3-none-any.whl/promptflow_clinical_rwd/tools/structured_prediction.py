from promptflow import tool
from typing import Any, Dict


@tool
def predict(patient_summary: str) -> Dict[str, Any]:
    error: bool = False
    prediction: str = "C50.4"
    if "error" in patient_summary:
        prediction = "ERROR"
        error = True
    return {"prediction": prediction, "error": error}
