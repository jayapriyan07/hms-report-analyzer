import os
from unittest.mock import MagicMock, patch
import pytest

from app.agents.extractor import load_guidelines, get_llm, get_extraction_chain
from app.schemas.report import MedicalReportAnalysis


def test_load_guidelines():
    guidelines = load_guidelines()
    assert isinstance(guidelines, dict)
    assert "Hemoglobin" in guidelines
    assert "Glucose" in guidelines
    assert guidelines["Hemoglobin"]["min_value"] == 12.0
    assert guidelines["WBC"]["max_value"] == 11000.0


def test_get_llm_raises_without_keys():
    # Clear settings and env keys
    with patch.dict(os.environ, {}, clear=True), \
         patch("app.agents.extractor.settings") as mock_settings:
        mock_settings.OPENAI_API_KEY = ""
        mock_settings.GOOGLE_API_KEY = ""

        with pytest.raises(ValueError, match="Google API Key is required"):
            get_llm(provider="google", model_name="gemini-1.5-flash")

        with pytest.raises(ValueError, match="OpenAI API Key is required"):
            get_llm(provider="openai", model_name="gpt-4o")


@patch("app.agents.extractor.ChatGoogleGenerativeAI")
def test_get_extraction_chain_setup(mock_chat_google):
    with patch("app.agents.extractor.settings") as mock_settings:
        mock_settings.GOOGLE_API_KEY = "mock-google-key"

        mock_llm = MagicMock()
        mock_chat_google.return_value = mock_llm

        chain = get_extraction_chain(provider="google", model_name="gemini-1.5-flash")

        # Verify that the structured output binding is called on our schema
        mock_llm.with_structured_output.assert_called_once_with(schema=MedicalReportAnalysis)
        assert chain is not None


import re

def mock_structured_llm_invoke(prompt_value, *args, **kwargs):
    # Intercept prompt value to simulate extraction based on guidelines
    messages = prompt_value.messages
    human_msg = messages[-1].content
    
    # regex extractors
    wbc_match = re.search(r"WBC\s*[:=]?\s*([\d,\.]+)", human_msg, re.IGNORECASE)
    hb_match = re.search(r"Hemoglobin\s*[:=]?\s*([\d,\.]+)", human_msg, re.IGNORECASE)
    glucose_match = re.search(r"Glucose\s*[:=]?\s*([\d,\.]+)", human_msg, re.IGNORECASE)
    
    biomarkers = []
    critical_flags = []
    
    guidelines = load_guidelines()
    
    def evaluate(name, val, unit):
        status = "Normal"
        if name in guidelines:
            g = guidelines[name]
            if val < g["min_value"]:
                status = "Low"
                critical_flags.append(f"{name} Low ({val} {unit})")
            elif val > g["max_value"]:
                status = "High"
                critical_flags.append(f"{name} High ({val} {unit})")
        biomarkers.append({
            "name": name,
            "value": val,
            "unit": unit,
            "status": status
        })
        
    if hb_match:
        evaluate("Hemoglobin", float(hb_match.group(1).replace(",", "")), "g/dL")
    if wbc_match:
        evaluate("WBC", float(wbc_match.group(1).replace(",", "")), "cells/uL")
    if glucose_match:
        evaluate("Glucose", float(glucose_match.group(1).replace(",", "")), "mg/dL")
        
    return MedicalReportAnalysis(
        patient_id="PT-98231",
        critical_flags=critical_flags,
        biomarkers=biomarkers,
        clinical_summary="Extraction verified against guidelines database."
    )


@patch("app.agents.extractor.get_llm")
def test_extract_normal_report(mock_get_llm):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_structured_llm.side_effect = mock_structured_llm_invoke
    mock_structured_llm.invoke.side_effect = mock_structured_llm_invoke
    
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_get_llm.return_value = mock_llm
    
    chain = get_extraction_chain()
    
    # Normal report text
    normal_report = "Patient PT-98231 Lab Results: Hemoglobin: 14.5, WBC: 7,000, Glucose: 85."
    
    result = chain.invoke({"report_text": normal_report})
    
    assert result.patient_id == "PT-98231"
    assert len(result.biomarkers) == 3
    assert len(result.critical_flags) == 0
    assert result.biomarkers[0].status == "Normal"
    assert result.biomarkers[1].status == "Normal"
    assert result.biomarkers[2].status == "Normal"


@patch("app.agents.extractor.get_llm")
def test_extract_critical_report(mock_get_llm):
    # Setup mock LLM
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_structured_llm.side_effect = mock_structured_llm_invoke
    mock_structured_llm.invoke.side_effect = mock_structured_llm_invoke
    
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_get_llm.return_value = mock_llm
    
    chain = get_extraction_chain()
    
    # Critical/Abnormal report text
    critical_report = "Patient PT-98231 Lab Results: Hemoglobin: 9.0, WBC: 15,000, Glucose: 85."
    
    result = chain.invoke({"report_text": critical_report})
    
    assert result.patient_id == "PT-98231"
    assert len(result.biomarkers) == 3
    # Hemoglobin is Low (9.0 < 12.0), WBC is High (15000 > 11000)
    assert len(result.critical_flags) == 2
    assert "Hemoglobin Low (9.0 g/dL)" in result.critical_flags
    assert "WBC High (15000.0 cells/uL)" in result.critical_flags
    
    # Check individual status
    biomarkers_dict = {b.name: b for b in result.biomarkers}
    assert biomarkers_dict["Hemoglobin"].status == "Low"
    assert biomarkers_dict["WBC"].status == "High"
    assert biomarkers_dict["Glucose"].status == "Normal"

