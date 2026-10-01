import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="SmartAging Demo", page_icon="🧬", layout="wide")

DATA = Path(__file__).parent / "smartaging_full_loop_100participants.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()

DOMAIN_INFO = {
    "Physiology": {
        "icon":"⌚", "title":"Wearable / Physiology", "weight":30,
        "metrics":[("Resting_HR_bpm","Resting HR","bpm"),("HRV_ms","HRV","ms"),
                   ("Sleep_h","Sleep","h"),("Daily_steps","Daily steps","")]
    },
    "Metabolic": {
        "icon":"🩸", "title":"Blood / Metabolic", "weight":30,
        "metrics":[("Fasting_glucose_mmol_L","Glucose","mmol/L"),("HbA1c_pct","HbA1c","%"),
                   ("Triglycerides_mmol_L","Triglycerides","mmol/L"),("HDL_mmol_L","HDL","mmol/L"),
                   ("LDL_mmol_L","LDL","mmol/L"),("hsCRP_mg_L","hs-CRP","mg/L")]
    },
    "Body": {
        "icon":"⚖️", "title":"Body Composition / BIA", "weight":25,
        "metrics":[("BMI","BMI",""),("Waist_cm","Waist","cm"),("Body_fat_pct","Body fat","%"),
                   ("BIA_Skeletal_muscle_kg","Skeletal muscle","kg"),
                   ("BIA_Visceral_fat_index","Visceral fat index","")]
    },
    "Function": {
        "icon":"📷", "title":"Camera / Function", "weight":15,
        "metrics":[("Gait_speed_m_s","Gait speed","m/s"),("Cadence_steps_min","Cadence","steps/min"),
                   ("Gait_symmetry_pct","Gait symmetry","%"),("Turn_time_s","Turn time","s")]
    }
}

def flag(score):
    if score < 12: return "Stable"
    if score < 30: return "Early change"
    if score < 55: return "Persistent change"
    return "High demo priority"

def delta_text(current, baseline, unit=""):
    if baseline == 0: return ""
    pct=(current-baseline)/abs(baseline)*100
    sign="+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}% vs baseline"

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1450px;}
.hero {padding: 1.2rem 1.4rem; border-radius: 18px; background: linear-gradient(120deg,#f4f8f6,#f7f8fb); margin-bottom: 1rem;}
.hero h1 {margin:0; font-size:2.4rem;}
.muted {color:#667085;}
.card {border:1px solid #e5e7eb; border-radius:18px; padding:1rem 1.05rem; min-height:220px; background:white;}
.bigscore {font-size:2rem; font-weight:750;}
.stable {color:#18794e;font-weight:700}.early {color:#b7791f;font-weight:700}
.persistent {color:#c05621;font-weight:700}.high {color:#b42318;font-weight:700}
.loop {font-size:1.05rem; font-weight:650; padding:.8rem; border-radius:14px; background:#f7f7f8; text-align:center;}
.notice {padding:.75rem 1rem;border-radius:12px;background:#fff8e6;border:1px solid #f4d58d;}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>SmartAging</h1>
<div style="font-size:1.25rem;font-weight:600">Longitudinal Multimodal Health Intelligence</div>
<div class="muted">Measure → Detect → Prioritize → Recommend → Re-measure → Assess response</div></div>""", unsafe_allow_html=True)

st.markdown('<div class="notice"><b>Synthetic demonstration cohort.</b> This prototype is not clinical validation, medical diagnosis, or a validated risk score.</div>', unsafe_allow_html=True)

a,b,c,d = st.columns(4)
a.metric("Participants", df.Participant_ID.nunique())
b.metric("Assessments", len(df))
c.metric("Follow-up", "12 months")
d.metric("Health domains", "4")

st.divider()

profiles=["Stable","Early Change","Persistent Risk","Intervention Response"]
c1,c2,c3=st.columns([1.2,1.2,1])
with c1:
    profile=st.selectbox("Trajectory profile", profiles, index=1)
ids=df.loc[df.Profile.eq(profile),"Participant_ID"].unique().tolist()
with c2:
    participant=st.selectbox("Participant", ids)
visits=["Baseline","Month 1","Month 3","Month 6","Month 9","Month 12"]
with c3:
    visit=st.selectbox("Assessment", visits, index=3)

p=df[df.Participant_ID.eq(participant)].sort_values("Month")
row=p[p.Visit.eq(visit)].iloc[0]
base=p.iloc[0]

st.subheader(f"{participant}  ·  {profile}  ·  {visit}")
st.caption(f"Synthetic participant · Age {int(row.Age)} · {row.Sex}")

# Domain cards
cols=st.columns(4)
for col,(domain,info) in zip(cols,DOMAIN_INFO.items()):
    score=float(row[f"{domain}_issue_score"])
    status=flag(score)
    cls="stable" if score<12 else "early" if score<30 else "persistent" if score<55 else "high"
    # Show two representative metrics
    metrics=info["metrics"][:2]
    mhtml=""
    for key,label,unit in metrics:
        val=row[key]
        bval=base[key]
        fmt=f"{val:,.0f}" if key in ["Daily_steps","Resting_HR_bpm","Cadence_steps_min"] else f"{val:.2f}"
        mhtml += f"<div><b>{label}</b>: {fmt} {unit}<br><span class='muted'>{delta_text(val,bval)}</span></div><br>"
    with col:
        st.markdown(f"""<div class="card">
        <div style="font-size:1.15rem;font-weight:700">{info['icon']} {info['title']}</div>
        <div class="muted">Demo weight {info['weight']}%</div>
        <div class="bigscore">{score:.0f}<span style="font-size:.9rem"> /100</span></div>
        <div class="{cls}">{status}</div><hr>{mhtml}</div>""", unsafe_allow_html=True)

st.caption("Domain scores are transparent demo-prioritization indicators derived from change versus the participant's own baseline; they are not validated clinical scores.")

st.divider()

left,right=st.columns([1.35,1])
with left:
    st.subheader("Personal trajectory")
    chart=p.set_index("Visit")[["Physiology_issue_score","Metabolic_issue_score","Body_issue_score","Function_issue_score"]]
    chart.columns=["Physiology","Metabolic","Body composition","Function"]
    st.line_chart(chart, height=330)
    if profile=="Intervention Response":
        st.info("🎯 **Month 6: simulated AI-guided preventive action plan.** Post-action points illustrate a synthetic response scenario.")

with right:
    score=float(row.Overall_demo_score)
    st.subheader("SmartAging Insight")
    st.metric("Demo prioritization score", f"{score:.0f}/100", help="Not a validated clinical risk score.")
    st.markdown(f"**Status:** {row.Overall_flag}")
    st.write(row.SmartAging_insight)
    st.markdown("**Highest-priority signals**")
    st.write(f"1. {row.Priority_1}")
    st.write(f"2. {row.Priority_2}")

st.divider()
st.subheader("From detection to action")
x1,x2,x3=st.columns(3)
with x1:
    st.markdown("### 1 · What changed?")
    st.write(f"**{row.Priority_1}** and **{row.Priority_2}** currently contribute most to the demo prioritization.")
with x2:
    st.markdown("### 2 · Suggested next actions")
    st.write(row.Recommended_action_1)
    st.write(row.Recommended_action_2)
with x3:
    st.markdown("### 3 · Re-measure")
    st.write(row.Follow_up)
    if profile=="Intervention Response" and row.Month>6:
        m6=p[p.Month.eq(6)].iloc[0]
        change=float(row.Overall_demo_score)-float(m6.Overall_demo_score)
        if change < -3:
            st.success(f"Response signal: demo score improved by {abs(change):.0f} points vs Month 6.")
        elif change > 3:
            st.warning(f"Response signal: demo score increased by {change:.0f} points vs Month 6.")
        else:
            st.info("Response signal: broadly stable versus Month 6.")

st.markdown('<div class="loop">MEASURE → DETECT → PRIORITIZE → RECOMMEND → RE-MEASURE → ASSESS RESPONSE</div>', unsafe_allow_html=True)

with st.expander("See all biomarker values"):
    show=["Visit"]
    for info in DOMAIN_INFO.values():
        show += [m[0] for m in info["metrics"]]
    st.dataframe(p[show], use_container_width=True, hide_index=True)

with st.expander("Methods & transparency"):
    st.write("""
    This application uses a fully synthetic cohort created for product demonstration.
    The domain weights (Physiology 30%, Metabolic 30%, Body Composition 25%, Function 15%)
    are prototype product-design assumptions, not clinically validated weights.
    Recommendations are simple curated preventive-action examples. In a clinical product,
    recommendation logic, thresholds, safety rules and escalation pathways would require
    appropriate evidence, validation, governance and regulatory assessment.
    The Intervention Response trajectory is explicitly simulated and does not demonstrate
    that SmartAging or AI caused an improvement.
    """)
    st.markdown("**SmartAging Deep:** optional MRI + metabolomics/lipidomics for deeper phenotyping and future validation.")
