import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SmartAging MVP", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1250px;}
[data-testid="stMetric"] {background:#f7f9fb; border:1px solid #e6e9ee; padding:14px; border-radius:14px;}
.small {color:#68707d;font-size:0.85rem}
</style>
""", unsafe_allow_html=True)

st.title("SmartAging")
st.caption("Multimodal preventive-health prototype • synthetic demonstration data • not for diagnosis")

scenario = st.selectbox("Demo scenario", ["Early multidomain change", "Healthy / stable"])

months = ["Baseline", "Month 3", "Month 6"]
if scenario == "Early multidomain change":
    data = pd.DataFrame({
        "Time": months,
        "Gait speed (m/s)": [1.35, 1.29, 1.20],
        "Cadence (steps/min)": [112,108,102],
        "Gait symmetry (%)": [97,95,91],
        "Resting HR (bpm)": [62,65,69],
        "HRV (ms)": [48,42,35],
        "Sleep (h)": [7.4,6.8,6.2],
        "Daily steps": [9200,7600,6100],
        "HbA1c (%)": [5.2,5.5,5.8],
        "Triglycerides (mmol/L)": [0.9,1.2,1.6],
        "HDL (mmol/L)": [1.55,1.42,1.25],
        "hs-CRP (mg/L)": [0.7,1.0,1.4],
        "Waist (cm)": [78,81,85],
        "Body fat (%)": [25,27,29],
    })
    status = "⚠️ Multidomain change detected"
    explanation = ("Functional, physiological, metabolic and body-phenotype measures are moving "
                   "together away from this participant's baseline.")
    action = ("Priority: cardiometabolic + functional prevention. Confirm persistent/abnormal laboratory "
              "findings with an appropriate clinician; review physical activity, resistance/aerobic exercise, "
              "nutrition and sleep; then re-measure to assess response.")
else:
    data = pd.DataFrame({
        "Time": months,
        "Gait speed (m/s)": [1.35,1.36,1.34],
        "Cadence (steps/min)": [112,113,112],
        "Gait symmetry (%)": [97,97,98],
        "Resting HR (bpm)": [62,61,62],
        "HRV (ms)": [48,50,49],
        "Sleep (h)": [7.4,7.5,7.4],
        "Daily steps": [9200,9400,9300],
        "HbA1c (%)": [5.2,5.2,5.1],
        "Triglycerides (mmol/L)": [0.9,0.9,0.8],
        "HDL (mmol/L)": [1.55,1.57,1.58],
        "hs-CRP (mg/L)": [0.7,0.6,0.6],
        "Waist (cm)": [78,78,77.5],
        "Body fat (%)": [25,24.8,24.7],
    })
    status = "✅ Stable personal trajectory"
    explanation = "No persistent adverse multidomain trend is demonstrated in this synthetic example."
    action = ("Maintain current healthy habits and routine preventive care. Continue periodic measurement "
              "to strengthen the personal baseline and detect meaningful future change.")

latest = data.iloc[-1]
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.subheader("📷 Function")
    st.metric("Gait speed", f"{latest['Gait speed (m/s)']:.2f} m/s")
    st.metric("Symmetry", f"{latest['Gait symmetry (%)']:.0f}%")
with c2:
    st.subheader("⌚ Physiology")
    st.metric("HRV", f"{latest['HRV (ms)']:.0f} ms")
    st.metric("Sleep", f"{latest['Sleep (h)']:.1f} h")
with c3:
    st.subheader("🩸 Metabolic")
    st.metric("HbA1c", f"{latest['HbA1c (%)']:.1f}%")
    st.metric("Triglycerides", f"{latest['Triglycerides (mmol/L)']:.1f} mmol/L")
with c4:
    st.subheader("👤 Body phenotype")
    st.metric("Waist", f"{latest['Waist (cm)']:.1f} cm")
    st.metric("Body fat", f"{latest['Body fat (%)']:.1f}%")

st.divider()
st.header("Personal health trajectory")
st.subheader(status)
st.write(explanation)

# Normalize each variable to its own baseline to visualize direction without inventing a clinical score.
trend_cols = ["Gait speed (m/s)", "HRV (ms)", "Daily steps", "HbA1c (%)", "Waist (cm)"]
norm = data[trend_cols].div(data[trend_cols].iloc[0]).mul(100)
norm.insert(0, "Time", data["Time"])
fig = go.Figure()
for col in trend_cols:
    fig.add_trace(go.Scatter(x=norm["Time"], y=norm[col], mode="lines+markers", name=col))
fig.update_layout(height=390, yaxis_title="Change vs personal baseline (%)",
                  legend_title="", margin=dict(l=20,r=20,t=20,b=20))
st.plotly_chart(fig, use_container_width=True)
st.caption("Each series is indexed to 100 at baseline. This is a trajectory visualization, not a validated clinical risk score.")

a,b = st.columns([2,1])
with a:
    st.subheader("🎯 Preventive action")
    st.info(action)
    st.markdown("**Closed loop:** Measure → detect change → act → re-measure → assess response")
with b:
    st.subheader("🧲 SmartAging Deep")
    st.write("Optional deep phenotyping / validation")
    st.write("• MRI body composition")
    st.write("• Metabolomics / lipidomics")
    st.caption("Not required for routine scalable monitoring.")

with st.expander("Show synthetic source data"):
    st.dataframe(data, use_container_width=True)

st.caption("Research/demo prototype. All participant values are synthetic and illustrative. "
           "Outputs are not medical diagnoses or validated treatment recommendations.")
