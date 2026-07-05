import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Add current workspace directory to sys.path to ensure absolute imports work
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app.agents.extractor import get_extraction_chain, load_guidelines
from app.schemas.report import MedicalReportAnalysis

# Page configuration
st.set_page_config(
    page_title="HMS Medical Report Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .section-card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .status-normal {
        color: #059669;
        font-weight: bold;
    }
    .status-abnormal {
        color: #DC2626;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🏥 Hospital Management System (HMS)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Automated Medical Report Extraction and Clinical Analysis</div>', unsafe_allow_html=True)

# Guidelines database for references
guidelines = load_guidelines()

# Sidebar config
st.sidebar.header("⚙️ Agent Settings")
provider = st.sidebar.selectbox("LLM Provider", ["Google", "OpenAI"])
if provider == "Google":
    # Updated to active production models to resolve 404 errors
    model_name = st.sidebar.selectbox("Model", ["gemini-2.5-flash", "gemini-2.5-pro"])
    api_key_env = os.getenv("GOOGLE_API_KEY", "")
    api_key_input = st.sidebar.text_input("Google API Key", value=api_key_env, type="password")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    api_key_env = os.getenv("OPENAI_API_KEY", "")
    api_key_input = st.sidebar.text_input("OpenAI API Key", value=api_key_env, type="password")

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

# Preset Templates
st.subheader("📝 Report Input")

preset_normal = (
    "PATIENT ID: PT-1002A\n"
    "HOSPITAL LAB REPORT - ROUTINE BLOOD PANEL\n"
    "-----------------------------------------\n"
    "Hemoglobin: 14.5 g/dL\n"
    "WBC: 7,200 cells/uL\n"
    "Glucose: 85 mg/dL\n"
    "Potassium: 4.1 mEq/L\n"
    "Sodium: 139 mEq/L\n"
    "LDL Cholesterol: 92 mg/dL\n"
    "-----------------------------------------\n"
    "Remarks: Overall patient values look stable."
)

preset_critical = (
    "PATIENT ID: PT-409B\n"
    "HOSPITAL LAB REPORT - METABOLIC COMPREHENSIVE\n"
    "---------------------------------------------\n"
    "Hemoglobin: 8.5 g/dL\n"
    "WBC: 16,500 cells/uL\n"
    "Glucose: 155 mg/dL\n"
    "Potassium: 2.8 mEq/L\n"
    "Sodium: 130 mEq/L\n"
    "LDL Cholesterol: 168 mg/dL\n"
    "---------------------------------------------\n"
    "Remarks: Patient complaining of muscle weakness and fatigue. Immediate clinical evaluation advised."
)

col_presets, col_text = st.columns([1, 4])

with col_presets:
    st.markdown("**Load Presets**")
    if st.button("🟢 Normal Lab Report"):
        st.session_state["report_text"] = preset_normal
    if st.button("🔴 Critical Lab Report"):
        st.session_state["report_text"] = preset_critical
    if st.button("🧹 Clear Text"):
        st.session_state["report_text"] = ""

with col_text:
    report_text = st.text_area(
        "Raw Medical Report Text",
        value=st.session_state.get("report_text", ""),
        height=200,
        placeholder="Paste lab text here or select a preset..."
    )

# Run Agent button
run_analysis = st.button("🚀 Run Agent Analysis", type="primary")

def draw_biomarkers_chart(biomarkers, guidelines):
    data = []
    for b in biomarkers:
        name = b.name
        val = b.value
        # Check if name exists in guidelines and value is numeric
        match_key = next((k for k in guidelines if k.lower() in name.lower() or name.lower() in k.lower()), None)
        if match_key and isinstance(val, (int, float)):
            g = guidelines[match_key]
            data.append({
                "Biomarker": name,
                "Value": float(val),
                "Min": float(g["min_value"]),
                "Max": float(g["max_value"]),
                "Unit": b.unit or g.get("unit", ""),
                "Status": b.status
            })
            
    if not data:
        return None
        
    fig = go.Figure()
    
    # We sort data to present cleanly
    for idx, item in enumerate(data):
        # Normal Range band line
        fig.add_trace(go.Scatter(
            x=[item["Min"], item["Max"]],
            y=[item["Biomarker"], item["Biomarker"]],
            mode="lines",
            line=dict(color="#E5E7EB", width=12),
            showlegend=False,
            hoverinfo="skip"
        ))
        
        # Patient's actual value marker
        is_critical = item["Status"].lower() in ["high", "low", "critical"]
        marker_color = "#EF4444" if is_critical else "#10B981"
        
        fig.add_trace(go.Scatter(
            x=[item["Value"]],
            y=[item["Biomarker"]],
            mode="markers",
            marker=dict(color=marker_color, size=15, line=dict(color="white", width=2)),
            name=item["Biomarker"],
            hovertemplate=(
                f"<b>{item['Biomarker']}</b><br>"
                f"Patient Value: {item['Value']} {item['Unit']}<br>"
                f"Reference Range: {item['Min']} - {item['Max']} {item['Unit']}<br>"
                f"Status: {item['Status']}<extra></extra>"
            ),
            showlegend=False
        ))
        
    fig.update_layout(
        title=dict(text="Biomarker Extracted Value vs Reference Guidelines", font=dict(size=16)),
        xaxis_title="Value / Unit",
        yaxis_title="Biomarker",
        margin=dict(l=150, r=40, t=50, b=50),
        height=max(200, 100 + len(data) * 45),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(gridcolor="#F3F4F6", zeroline=False),
        yaxis=dict(gridcolor="#FFFFFF")
    )
    return fig


if run_analysis:
    if not report_text.strip():
        st.warning("Please paste or load medical report text first.")
    else:
        # Dynamically set API key in environment for extractor chain execution
        if api_key_input.strip():
            if provider == "Google":
                os.environ["GOOGLE_API_KEY"] = api_key_input
            else:
                os.environ["OPENAI_API_KEY"] = api_key_input
                
        try:
            with st.spinner("Initializing Clinical AI Extraction Chain..."):
                chain = get_extraction_chain(
                    provider=provider.lower(),
                    model_name=model_name,
                    temperature=temperature
                )
                
            with st.spinner("Extracting parameters and performing clinical analysis comparison..."):
                # Call agent
                analysis: MedicalReportAnalysis = chain.invoke({"report_text": report_text})
                
            st.success("Analysis Complete!")
            
            # Master columns layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📋 Patient Summary & Diagnostics")
                st.markdown(f"**Patient Record Identifier:** `{analysis.patient_id}`")
                
                # Clinical Summary Card
                st.info(analysis.clinical_summary)
                
                # Critical Flags Notice Box
                if analysis.critical_flags:
                    st.error("🚨 **Critical/Abnormal Clinical Flags Detected:**")
                    for flag in analysis.critical_flags:
                        st.markdown(f"- {flag}")
                else:
                    st.success("✅ **No critical reference breaches flagged.**")
                    
            with col2:
                st.subheader("📊 Structured Biomarker Catalog")
                
                # Format biomarkers as table
                table_data = []
                for b in analysis.biomarkers:
                    table_data.append({
                        "Biomarker": b.name,
                        "Value": b.value,
                        "Unit": b.unit or "N/A",
                        "Status": b.status
                    })
                df = pd.DataFrame(table_data)
                
                # Render beautiful custom styling table
                st.dataframe(
                    df,
                    column_config={
                        "Biomarker": st.column_config.TextColumn("Test Name", width="medium"),
                        "Value": st.column_config.NumberColumn("Measured Value", width="small"),
                        "Unit": st.column_config.TextColumn("Unit", width="small"),
                        "Status": st.column_config.TextColumn("Status", width="small")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Draw dynamic range mapping chart
                chart = draw_biomarkers_chart(analysis.biomarkers, guidelines)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Failed to execute agent analysis: {str(e)}")
            st.info(
                "Verify your API key is correctly entered in the sidebar, or check that your network connection is online."
            )