from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Biomarker(BaseModel):
    """
    Structured model representing an individual biomarker extracted from a medical report.
    """

    name: str = Field(
        ...,
        description="The standardized name of the biomarker, lab test, or analyte analyzed (e.g., 'Hemoglobin', 'WBC', 'Cholesterol')."
    )
    value: Union[float, str] = Field(
        ...,
        description="The measured result value of the biomarker. Can be numeric (e.g., 14.5) or qualitative (e.g., 'Positive', 'Reactive')."
    )
    unit: Optional[str] = Field(
        None,
        description="The unit of measurement associated with the value (e.g., 'g/dL', 'mg/dL', '10^3/uL'). Should be null/None for qualitative tests."
    )
    status: str = Field(
        ...,
        description="The clinical status classification of the biomarker based on the reference range (e.g., 'Normal', 'High', 'Low', 'Critical')."
    )


class MedicalReportAnalysis(BaseModel):
    """
    Master model for structured extraction and clinical interpretation of a raw medical lab report.
    """

    patient_id: str = Field(
        ...,
        description="The unique identifier, name, or record number of the patient from the report."
    )
    critical_flags: List[str] = Field(
        default_factory=list,
        description="A list of specific biomarker names or conditions that fall into 'Critical', 'High', or 'Low' categories requiring clinical review."
    )
    biomarkers: List[Biomarker] = Field(
        ...,
        description="A list of all individual biomarkers and lab measurements extracted from the report."
    )
    clinical_summary: str = Field(
        ...,
        description="A concise, synthesized clinical overview of the patient's lab results, highlight anomalies, and suggesting potential next steps or correlations."
    )
