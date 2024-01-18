from promptflow import tool
from promptflow.connections import AzureOpenAIConnection
from promptflow.contracts.types import PromptTemplate
from typing import Any, Dict


@tool
def predict(
    connection: AzureOpenAIConnection,
    patient_summary: str,
    default_value: str,
    prompt: PromptTemplate,
    **kwargs,
) -> Dict[str, Any]:
    error: bool = False
    prediction: str = default_value
    if "error" in patient_summary:
        prediction = "ERROR"
        error = True
    return {"prediction": prediction, "error": error}
