import json
import os
from pathlib import Path
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.report import MedicalReportAnalysis

# Locate guidelines file relative to this file
GUIDELINES_PATH = Path(__file__).parent.parent / "core" / "guidelines.json"


def load_guidelines() -> Dict[str, Any]:
    """
    Loads normal reference ranges from guidelines.json.
    """
    try:
        if GUIDELINES_PATH.exists():
            with open(GUIDELINES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    # Fallback to in-memory lookup if guidelines.json is missing or corrupted
    return {
        "Hemoglobin": {"min_value": 12.0, "max_value": 16.0, "unit": "g/dL"},
        "WBC": {"min_value": 4500.0, "max_value": 11000.0, "unit": "cells/uL"},
        "Glucose": {"min_value": 70.0, "max_value": 100.0, "unit": "mg/dL"},
        "Potassium": {"min_value": 3.5, "max_value": 5.0, "unit": "mEq/L"},
        "Sodium": {"min_value": 135.0, "max_value": 145.0, "unit": "mEq/L"},
        "LDL Cholesterol": {"min_value": 0.0, "max_value": 100.0, "unit": "mg/dL"}
    }


def get_llm(provider: str, model_name: str, temperature: float = 0.0) -> Any:
    """
    Instantiates the appropriate ChatModel based on provider and configurations.
    """
    # Enforce API keys from configuration or environment
    openai_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    google_key = settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")

    if provider.lower() == "google":
        if not google_key:
            raise ValueError(
                "Google API Key is required but not set in settings or GOOGLE_API_KEY environment variable."
            )
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=google_key,
            temperature=temperature
        )
    elif provider.lower() == "openai":
        if not openai_key:
            raise ValueError(
                "OpenAI API Key is required but not set in settings or OPENAI_API_KEY environment variable."
            )
        return ChatOpenAI(
            model=model_name,
            api_key=openai_key,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def get_extraction_chain(
    provider: str = "google",
    model_name: str = "gemini-2.5-flash",  # Updated to fix the 404 NOT_FOUND error
    temperature: float = 0.0
) -> Any:
    """
    Creates and returns the structured extraction chain for medical reports.
    """
    guidelines = load_guidelines()
    guidelines_str = json.dumps(guidelines, indent=2).replace("{", "{{").replace("}", "}}")

    system_prompt = (
        "You are an expert AI clinical data analyst at a world-class hospital. Your objective is to read the "
        "raw medical lab report text, extract structured patient data, and evaluate values against normal range guidelines.\n\n"
        "Here are the reference range guidelines you must adhere to:\n"
        f"{guidelines_str}\n\n"
        "INSTRUCTIONS:\n"
        "1. Extract the patient ID or name accurately. If not found, use a reasonable placeholder or identifier.\n"
        "2. Parse all biomarkers from the report. For each biomarker, extract the name, measured value (float or str), "
        "the unit, and evaluate its status.\n"
        "3. Look up the biomarker in the reference guidelines. If it is present:\n"
        "   - Compare the measured value against min_value and max_value.\n"
        "   - If the value is within the range, classify the status as 'Normal'.\n"
        "   - If it is below min_value, classify the status as 'Low'.\n"
        "   - If it is above max_value, classify the status as 'High'.\n"
        "   - For exceptionally dangerous deviations (e.g. Potassium < 3.0 or > 6.0 mEq/L, or any flag explicitly stated "
        "     as critical in the report), classify status as 'Critical'.\n"
        "4. If a biomarker is not in the guidelines list, evaluate it based on standard clinical knowledge or references in the report.\n"
        "5. Under 'critical_flags', list all biomarkers that have 'Low', 'High', or 'Critical' status with their value and units "
        "(e.g., ['Glucose High (140.0 mg/dL)', 'Potassium Low (2.9 mEq/L)']). If all are normal, return an empty list.\n"
        "6. Provide a concise, clinical-grade summary of the overall report, pointing out critical flags and recommending "
        "appropriate next clinical/diagnostic steps."
    )

    llm = get_llm(provider=provider, model_name=model_name, temperature=temperature)
    structured_llm = llm.with_structured_output(schema=MedicalReportAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Raw Medical Report Text:\n{report_text}")
    ])

    return prompt | structured_llm