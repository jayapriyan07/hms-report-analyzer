# 🏥 HMS Medical Report Analyzer

**AI-Powered Automated Medical Report Extraction and Clinical Analysis**

An intelligent system that leverages Large Language Models (LLMs) to automatically extract structured clinical data from raw medical reports, evaluate biomarkers against reference guidelines, and provide clinical summaries with flagged critical findings.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Use Case Diagram](#use-case-diagram)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture & Data Flow](#architecture--data-flow)
- [Supported Biomarkers](#supported-biomarkers)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

The **HMS Medical Report Analyzer** is a hospital management system component designed to digitize and intelligently process medical laboratory reports. It uses advanced AI and LLM capabilities to:

1. **Parse** raw medical report text from lab reports
2. **Extract** structured patient data and biomarker measurements
3. **Evaluate** extracted values against clinical reference ranges
4. **Identify** abnormal findings and critical conditions
5. **Visualize** biomarker data with interactive charts
6. **Provide** clinical summaries and actionable insights

### Primary Use Cases:
- Automating medical report analysis in hospital labs
- Reducing manual data entry errors and time
- Flagging critical results for immediate clinical review
- Supporting evidence-based clinical decision-making
- Enabling seamless integration with EHR/EMR systems

---

## 📊 Use Case Diagram

```
                          ┌─────────────────────────────────────┐
                          │   HMS Medical Report Analyzer       │
                          └─────────────────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
            ┌──────────────┐      ┌──────────────┐    ┌──────────────┐
            │   Lab       │      │  Clinical    │    │   Hospital   │
            │   Technician│      │  Physician   │    │  Administrator│
            └──────────────┘      └──────────────┘    └──────────────┘
                    │                    │                    │
                    │ (1) Submit Report   │                   │
                    │                    │                   │
                    ▼                    ▼                   ▼
            ┌────────────────────────────────────────────────────┐
            │          📝 Raw Medical Report Text                │
            │   (Lab values, patient info, clinical notes)       │
            └────────────────────────────────────────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────────────────────┐
            │      AI-Powered Report Analyzer (LLM Agent)        │
            │   - Parse structured patient data                 │
            │   - Extract biomarker measurements                │
            │   - Compare against reference guidelines          │
            │   - Classify status (Normal/High/Low/Critical)   │
            └────────────────────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Patient  │  │Biomarker │  │ Clinical │
        │   Info   │  │  Data    │  │ Summary  │
        │ (ID, etc)│  │ (Values) │  │ & Flags  │
        └──────────┘  └──────────┘  └──────────┘
                │            │            │
                └────────────┼────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │          📊 Interactive Visualization             │
        │   - Biomarker comparison chart                     │
        │   - Reference range display                        │
        │   - Status indicators (Normal/Abnormal)            │
        │   - Critical flags highlighting                    │
        └────────────────────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
            Physician     Hospital      Patient
            Reviews       Records       Portal
            Results       Database      Access


                      SYSTEM INTERACTIONS

        ┌──────────────────────────────────────┐
        │   LLM Providers (Configurable)       │
        │  - Google Gemini 2.5 Flash/Pro       │
        │  - OpenAI GPT-4o/GPT-4o-mini        │
        └──────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │   LangChain Orchestration            │
        │  - Prompt templates                  │
        │  - Structured output parsing         │
        │  - Chain execution                   │
        └──────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │   Reference Guidelines Database      │
        │  - Clinical reference ranges         │
        │  - Biomarker descriptions            │
        │  - Unit specifications               │
        └──────────────────────────────────────┘

```

---

## ✨ Key Features

### 🤖 Intelligent Data Extraction
- **LLM-Powered Parsing**: Uses advanced language models (Google Gemini or OpenAI GPT-4o) to understand and extract data from unstructured medical text
- **Multi-Provider Support**: Toggle between Google Gemini and OpenAI APIs seamlessly
- **Configurable Temperature**: Adjust LLM creativity/determinism for different use cases

### 📋 Structured Data Management
- **Pydantic Models**: Type-safe, validated data structures for patient info and biomarkers
- **Standardized Output**: Consistent JSON schema for downstream integrations
- **Flexible Biomarker Support**: Handles both quantitative (numeric) and qualitative (categorical) test results

### 📊 Clinical Analysis & Flagging
- **Reference Range Comparison**: Compares extracted values against evidence-based clinical guidelines
- **Automatic Status Classification**: Labels biomarkers as Normal, Low, High, or Critical
- **Critical Alerts**: Flags dangerous biomarker deviations for immediate clinical review
- **Clinical Summary Generation**: Provides clinician-friendly synthesis of findings

### 📈 Interactive Visualization
- **Biomarker Comparison Charts**: Plotly-powered interactive visualization showing:
  - Patient's measured values
  - Normal reference ranges
  - Visual status indicators (green for normal, red for abnormal)
  - Hover tooltips with detailed information
- **Responsive Tables**: Formatted biomarker data with real-time updates

### 🎨 User-Friendly Interface
- **Streamlit Web App**: Modern, responsive UI for report submission and analysis
- **Preset Templates**: Pre-loaded example reports (normal and critical scenarios)
- **Real-Time Feedback**: Spinners and progress indicators during analysis
- **Beautiful Styling**: Custom CSS for professional healthcare UI appearance

### 🔧 Flexible Configuration
- **Environment-Based Setup**: Secure API key management via `.env` files
- **Dynamic Model Selection**: Switch between LLM models on-the-fly
- **Temperature Control**: Fine-tune LLM behavior from deterministic (0.0) to creative (1.0)

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit, Plotly | Interactive web UI & data visualization |
| **Backend** | Python 3.8+ | Core application logic |
| **LLM Integration** | LangChain, Pydantic | Prompt management, structured output |
| **AI Models** | Google Gemini 2.5, OpenAI GPT-4o | Intelligent data extraction & analysis |
| **Data Validation** | Pydantic 2.0+ | Type-safe schema definitions |
| **Testing** | Pytest | Unit and integration testing |
| **Environment** | python-dotenv | Configuration management |

---

## 📁 Project Structure

```
hms-report-analyzer/
├── app/
│   ├── __init__.py
│   ├── ui.py                          # Main Streamlit application
│   ├── agents/
│   │   ├── __init__.py
│   │   └── extractor.py               # LLM chain & extraction logic
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration settings
│   │   └── guidelines.json            # Clinical reference ranges
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── report.py                  # Pydantic models (Biomarker, MedicalReportAnalysis)
│   └── tests/
│       └── ...                         # Unit & integration tests
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment template
└── README.md                          # This file
```

### File Descriptions

- **`ui.py`**: Main Streamlit application with report input, preset templates, and results visualization
- **`agents/extractor.py`**: LangChain extraction chain, LLM initialization, and guideline loading
- **`schemas/report.py`**: Pydantic models defining biomarker and report structures
- **`core/config.py`**: Application configuration (API keys, model settings)
- **`core/guidelines.json`**: Clinical reference ranges for biomarkers (extensible)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- API keys for LLM providers (Google or OpenAI)

### Step 1: Clone the Repository

```bash
git clone https://github.com/jayapriyan07/hms-report-analyzer.git
cd hms-report-analyzer
```

### Step 2: Create a Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create --name hms-analyzer python=3.10
conda activate hms-analyzer
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If example exists
# OR create manually:
```

Add your API keys to `.env`:

```env
# For Google Gemini
GOOGLE_API_KEY=your-google-api-key-here

# For OpenAI (optional)
OPENAI_API_KEY=your-openai-api-key-here
```

**To get API keys:**
- **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- **OpenAI**: Visit [OpenAI API Keys](https://platform.openai.com/account/api-keys)

---

## ⚙️ Configuration

### `app/core/config.py`
Centralized configuration management:

```python
# Reads from environment variables or .env file
settings.GOOGLE_API_KEY     # Google Gemini API key
settings.OPENAI_API_KEY     # OpenAI API key
```

### `app/core/guidelines.json`
Reference ranges for biomarkers:

```json
{
  "Hemoglobin": {
    "min_value": 12.0,
    "max_value": 16.0,
    "unit": "g/dL",
    "description": "..."
  },
  ...
}
```

**To add new biomarkers**, edit `guidelines.json` with the structure above.

---

## 🎮 Usage

### Run the Application

```bash
streamlit run app/ui.py
```

The app will open in your default browser at `http://localhost:8501`

### Workflow

1. **Select LLM Provider** (sidebar)
   - Choose between Google Gemini or OpenAI
   - Select model version

2. **Input Medical Report**
   - Paste raw lab report text, OR
   - Use preset templates (Normal/Critical)
   - Adjust LLM temperature if needed

3. **Run Analysis**
   - Click "🚀 Run Agent Analysis"
   - Watch real-time processing spinner

4. **Review Results**
   - Patient summary & critical flags
   - Structured biomarker table
   - Interactive biomarker comparison chart

### Example Input

```
PATIENT ID: PT-1002A
HOSPITAL LAB REPORT - ROUTINE BLOOD PANEL
-----------------------------------------
Hemoglobin: 14.5 g/dL
WBC: 7,200 cells/uL
Glucose: 85 mg/dL
Potassium: 4.1 mEq/L
Sodium: 139 mEq/L
LDL Cholesterol: 92 mg/dL
-----------------------------------------
Remarks: Overall patient values look stable.
```

### Example Output

```json
{
  "patient_id": "PT-1002A",
  "biomarkers": [
    {"name": "Hemoglobin", "value": 14.5, "unit": "g/dL", "status": "Normal"},
    {"name": "WBC", "value": 7200, "unit": "cells/uL", "status": "Normal"},
    {"name": "Glucose", "value": 85, "unit": "mg/dL", "status": "Normal"},
    {"name": "Potassium", "value": 4.1, "unit": "mEq/L", "status": "Normal"},
    {"name": "Sodium", "value": 139, "unit": "mEq/L", "status": "Normal"},
    {"name": "LDL Cholesterol", "value": 92, "unit": "mg/dL", "status": "Normal"}
  ],
  "critical_flags": [],
  "clinical_summary": "All biomarkers within normal reference ranges. Patient appears to be in stable metabolic condition..."
}
```

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                       │
│                    (Streamlit Web UI)                           │
│  - Report text input  │ Preset buttons │ Settings sidebar      │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                             │
│                   (ui.py)                                        │
│  - Session management │ Error handling │ Result visualization  │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTRACTION & ANALYSIS LAYER                    │
│                (agents/extractor.py)                            │
│  - Prompt construction │ LLM invocation │ Output parsing        │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌──────────────────┬──────────────────┬──────────────────┐
│   LLM PROVIDERS  │   DATA SCHEMA    │  GUIDELINES DB   │
│                  │                  │                  │
│ - Google Gemini  │ - Pydantic Model │ - Reference      │
│ - OpenAI GPT     │   Validation     │   Ranges         │
│                  │ - Type Safety    │ - Biomarkers     │
└──────────────────┴──────────────────┴──────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STRUCTURED OUTPUT                              │
│               (MedicalReportAnalysis)                           │
│  - Patient ID │ Biomarkers │ Critical Flags │ Summary          │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               PRESENTATION LAYER                                │
│                (ui.py visualization)                            │
│  - Summary card │ Tables │ Interactive Charts │ Status badges  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Supported Biomarkers

The system comes with reference ranges for these common biomarkers:

| Biomarker | Min | Max | Unit | Clinical Significance |
|-----------|-----|-----|------|----------------------|
| **Hemoglobin** | 12.0 | 16.0 | g/dL | Oxygen-carrying protein; low=anemia, high=polycythemia |
| **WBC** | 4,500 | 11,000 | cells/uL | White blood cells; high=infection/inflammation |
| **Glucose** | 70 | 100 | mg/dL | Fasting blood sugar; high=diabetes risk |
| **Potassium** | 3.5 | 5.0 | mEq/L | Cardiac electrolyte; extremes=arrhythmias |
| **Sodium** | 135 | 145 | mEq/L | Electrolyte for fluid balance; low=edema |
| **LDL Cholesterol** | 0 | 100 | mg/dL | Bad cholesterol; high=cardiovascular risk |

**To add more biomarkers:**
1. Edit `app/core/guidelines.json` with new entries
2. Update system prompt in `app/agents/extractor.py` if needed
3. Restart the application

---

## 📚 Examples

### Example 1: Normal Lab Report
```
PATIENT ID: PT-2024-001
RESULTS:
- Hemoglobin: 14.5 g/dL ✓
- WBC: 7,500 cells/uL ✓
- Glucose: 95 mg/dL ✓
```
**Output**: All biomarkers normal, no critical flags, low-risk summary.

### Example 2: Critical Lab Report
```
PATIENT ID: PT-2024-002
RESULTS:
- Hemoglobin: 8.5 g/dL (LOW)
- WBC: 16,500 cells/uL (HIGH)
- Glucose: 155 mg/dL (HIGH)
- Potassium: 2.8 mEq/L (CRITICAL)
```
**Output**: Multiple critical flags, urgent clinical review recommended, specific medical correlations noted.

---

## 🧪 Testing

Run unit tests with pytest:

```bash
pytest app/tests/ -v
```

Test structure:
```
app/tests/
├── test_extractor.py      # LLM chain tests
├── test_schemas.py        # Pydantic model validation
└── test_guidelines.py     # Reference range logic
```

---

## 🔐 Security Considerations

1. **API Key Management**
   - Never commit `.env` files with real keys
   - Use environment variables for deployment
   - Rotate keys regularly

2. **Data Privacy**
   - This system processes medical data; ensure HIPAA/regulatory compliance
   - Consider adding data encryption for sensitive deployments
   - Implement audit logging for clinical use

3. **Input Validation**
   - All LLM outputs validated against Pydantic schemas
   - Type checking prevents injection attacks
   - Report text sanitization recommended for production

---

## 🚦 Deployment

### Local Development
```bash
streamlit run app/ui.py
```

### Production (Docker)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app/ui.py", "--server.port=8501"]
```

```bash
docker build -t hms-analyzer .
docker run -p 8501:8501 -e GOOGLE_API_KEY=$GOOGLE_API_KEY hms-analyzer
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive

---

## 📝 License

This project is open-source. Check the LICENSE file for details.

---

## 🆘 Troubleshooting

### Issue: "API Key not found"
**Solution**: Ensure `.env` file exists in project root with correct API keys

### Issue: "Model not found" (404 error)
**Solution**: Update model names in sidebar (e.g., `gemini-2.5-flash` for Google, `gpt-4o-mini` for OpenAI)

### Issue: "Rate limit exceeded"
**Solution**: Add delay between requests or upgrade API tier

### Issue: Streamlit app won't start
**Solution**: 
```bash
pip install --upgrade streamlit
streamlit run app/ui.py --logger.level=debug
```

---

## 📞 Support & Contact

For questions, issues, or suggestions:
- Open a GitHub Issue
- Contact: [jayapriyan07](https://github.com/jayapriyan07)

---

## 🙏 Acknowledgments

- Built with [LangChain](https://python.langchain.com/) for LLM orchestration
- Powered by [Google Gemini](https://ai.google.dev/) and [OpenAI APIs](https://openai.com/api/)
- UI built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)
- Data validation with [Pydantic](https://docs.pydantic.dev/)

---

**Last Updated**: July 2026  
**Version**: 1.0.0  
**Status**: Active Development
