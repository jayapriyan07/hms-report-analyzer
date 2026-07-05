import pytest
from pydantic import ValidationError
from app.schemas.report import Biomarker, MedicalReportAnalysis


def test_valid_numeric_biomarker():
    biomarker = Biomarker(
        name="Hemoglobin",
        value=14.5,
        unit="g/dL",
        status="Normal"
    )
    assert biomarker.name == "Hemoglobin"
    assert biomarker.value == 14.5
    assert biomarker.unit == "g/dL"
    assert biomarker.status == "Normal"


def test_valid_qualitative_biomarker():
    biomarker = Biomarker(
        name="Hepatitis B Surface Antigen",
        value="Non-reactive",
        unit=None,
        status="Normal"
    )
    assert biomarker.name == "Hepatitis B Surface Antigen"
    assert biomarker.value == "Non-reactive"
    assert biomarker.unit is None
    assert biomarker.status == "Normal"


def test_invalid_biomarker_type():
    with pytest.raises(ValidationError):
        # value must be Union[float, str], passing a dict should fail
        Biomarker(
            name="Glucose",
            value={"wrong": "type"},
            unit="mg/dL",
            status="High"
        )


def test_valid_medical_report_analysis():
    data = {
        "patient_id": "PT-98231",
        "critical_flags": ["Glucose High", "LDL Cholesterol High"],
        "biomarkers": [
            {
                "name": "Glucose",
                "value": 140.0,
                "unit": "mg/dL",
                "status": "High"
            },
            {
                "name": "LDL Cholesterol",
                "value": 160.0,
                "unit": "mg/dL",
                "status": "High"
            },
            {
                "name": "Hemoglobin",
                "value": 15.0,
                "unit": "g/dL",
                "status": "Normal"
            }
        ],
        "clinical_summary": "Patient shows elevated fasting glucose and LDL cholesterol level. Recommend dietary modifications and lipid profile followup in 3 months."
    }
    report = MedicalReportAnalysis(**data)
    assert report.patient_id == "PT-98231"
    assert len(report.biomarkers) == 3
    assert "Glucose High" in report.critical_flags
    assert report.biomarkers[0].name == "Glucose"
    assert report.biomarkers[0].value == 140.0


def test_json_schema_serialization():
    # Verify we can obtain the JSON schema for LangChain tool binding / LLM structured outputs
    schema = MedicalReportAnalysis.model_json_schema()
    assert "properties" in schema
    assert "patient_id" in schema["properties"]
    assert "critical_flags" in schema["properties"]
    assert "biomarkers" in schema["properties"]
    assert "clinical_summary" in schema["properties"]

