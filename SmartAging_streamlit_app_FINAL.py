import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="SmartAging", page_icon="🧬", layout="wide")

DATA = Path(__file__).parent / "smartaging_final_demo_100participants.csv"

@st.cache_data
def load_data():
    d = pd.read_csv(DATA)
    d["Month"] = pd.to_numeric(d["Month"], errors="coerce")
    return d

df = load_data()

DOMAIN_INFO = {
    "Function": {
        "icon":"📷", "title":"Camera / Function", "subtitle":"Mobility and physical function",
        "score":"Function_issue_score",
        "metrics":[
            ("Gait_speed_m_s","Gait speed","m/s",False),
            ("Cadence_steps_min","Cadence","steps/min",False),
            ("Gait_symmetry_pct","Gait symmetry","%",False),
            ("Turn_time_s","Turn time","s",True),
            ("Five_times_sit_to_stand_s","5× sit-to-stand","s",True)
        ]
    },
    "Physiology": {
        "icon":"⌚", "title":"Wearable / Physiology", "subtitle":"Recovery, activity and fitness",
        "score":"Physiology_issue_score",
        "metrics":[
            ("Resting_HR_bpm","Resting HR","bpm",True),
            ("HRV_ms","HRV","ms",False),
            ("Sleep_h","Sleep","h",False),
            ("Daily_steps","Daily steps","",False),
            ("VO2max_est_ml_kg_min","Estimated VO₂max","mL/kg/min",False)
        ]
    },
    "Metabolic": {
        "icon":"🩸", "title":"Blood / Biomarkers", "subtitle":"Cardiometabolic and inflammatory markers",
        "score":"Metabolic_issue_score",
        "metrics":[
            ("Fasting_glucose_mmol_L","Fasting glucose","mmol/L",True),
            ("HbA1c_pct","HbA1c","%",True),
            ("Fasting_insulin_uIU_mL","Fasting insulin","µIU/mL",True),
            ("Triglycerides_mmol_L","Triglycerides","mmol/L",True),
            ("HDL_mmol_L","HDL","mmol/L",False),
            ("LDL_mmol_L","LDL","mmol/L",True),
            ("Total_cholesterol_mmol_L","Total cholesterol","mmol/L",True),
            ("ApoB_g_L","ApoB","g/L",True),
            ("hsCRP_mg_L","hs-CRP","mg/L",True),
            ("ALT_U_L","ALT","U/L",True),
            ("Vitamin_D_ng_mL","Vitamin D","ng/mL",False)
        ]
    },
    "Body": {
        "icon":"⚖️", "title":"Body Composition", "subtitle":"Anthropometry and BIA",
        "score":"Body_issue_score",
        "metrics":[
            ("Weight_kg","Weight","kg",True),
            ("BMI","BMI","",True),
            ("Waist_cm","Waist","cm",True),
            ("Body_fat_pct","Body fat","%",True),
            ("BIA_Skeletal_muscle_kg","Skeletal muscle","kg",False),
            ("BIA_Visceral_fat_index","Visceral fat index","",True)
        ]
    }
}

def delta_pct(current, baseline):
    if pd.isna(current) or pd.isna(baseline) or float(baseline)==0:
        return np.nan
    return (float(current)-float(baseline))/abs(float(baseline))*100

def fmt(key, value):
    if pd.isna(value): return "—"
    if key in ("Daily_steps","Resting_HR_bpm","ALT_U_L"):
        return f"{float(value):,.0f}"
    return f"{float(value):.2f}"

def status(score):
    score=float(score)
    if score < 12: return "Stable"
    if score < 30: return "Early change"
    if score < 55: return "Persistent change"
    return "High demo priority"

def delta_label(key, cur, base, adverse_high):
    d=delta_pct(cur,base)
    if pd.isna(d) or abs(d)<0.05: return "At personal baseline"
    adverse = d>0 if adverse_high else d<0
    return f"{'↑' if d>0 else '↓'} {abs(d):.1f}% vs baseline · {'adverse' if adverse else 'favorable'}"

st.markdown("""
<style>
.block-container{padding-top:1.1rem;padding-bottom:3rem;max-width:1480px}
.hero{background:linear-gradient(120deg,#eff7f3,#fafcfb);border:1px solid #e1eae5;border-radius:24px;padding:1.5rem 1.7rem;margin-bottom:1rem}
.brand{font-size:2.5rem;font-weight:800;letter-spacing:-.04em;color:#172820}
.tag{font-size:1.12rem;font-weight:650;color:#365449}
.muted{color:#6b7973}.notice{padding:.7rem 1rem;border-radius:12px;background:#fff9e8;border:1px solid #eedda4;font-size:.9rem}
.card{border:1px solid #e2eae6;border-radius:19px;padding:1rem;background:white;min-height:160px}
.kicker{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#728079;font-weight:700}
.big{font-size:1.9rem;font-weight:800;color:#172820}.loop{text-align:center;font-weight:750;padding:.9rem;border-radius:14px;background:#f3f7f5;color:#365449}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><div class="brand">SmartAging</div>
<div class="tag">See change earlier. Act while function is still preserved.</div>
<div class="muted">Camera + wearable + blood + body composition, interpreted against the individual's longitudinal baseline.</div></div>""", unsafe_allow_html=True)
st.markdown('<div class="notice"><b>Synthetic demonstration cohort.</b> Not clinical validation, diagnosis, treatment advice, or a validated risk score.</div>', unsafe_allow_html=True)

profiles=["Stable","Early Change","Persistent Risk","Intervention Response"]
c1,c2,c3=st.columns([1.1,1.1,1])
with c1:
    profile=st.selectbox("Journey",profiles,index=1)
ids=df.loc[df.Profile.eq(profile),"Participant_ID"].unique().tolist()
with c2:
    participant=st.selectbox("Participant",ids)
p=df[df.Participant_ID.eq(participant)].copy().sort_values("Month").reset_index(drop=True)
visits=p["Visit"].tolist()
with c3:
    visit=st.selectbox("Assessment",visits,index=min(3,len(visits)-1))

row=p[p.Visit.eq(visit)].iloc[0]
base=p.loc[p.Month.idxmin()]
st.caption(f"{participant} · Age {int(row.Age)} · {row.Sex} · {visit}")

tabs=st.tabs(["Overview","Camera","Wearable","Blood","Body","SmartAging AI","Action Plan","Progress"])

with tabs[0]:
    st.markdown("### Your longitudinal health picture")
    cols=st.columns(4)
    for col,(name,info) in zip(cols,DOMAIN_INFO.items()):
        s=float(row[info["score"]])
        with col:
            st.markdown(f"""<div class="card"><div class="kicker">{info['icon']} {info['title']}</div>
            <div class="big">{s:.0f}<span class="muted" style="font-size:.85rem"> /100 demo index</span></div>
            <b>{status(s)}</b><br><span class="muted">{info['subtitle']}</span></div>""",unsafe_allow_html=True)

    st.markdown("### Personal trajectory")
    chart=p.set_index("Month")[["Function_issue_score","Physiology_issue_score","Metabolic_issue_score","Body_issue_score"]]
    chart.columns=["Function","Physiology","Metabolic","Body composition"]
    st.line_chart(chart,height=340,x_label="Month (0 = baseline)",y_label="Demo change index")
    st.caption("Baseline → Month 1 → Month 3 → Month 6 → Month 9 → Month 12")
    l,r=st.columns([1.35,1])
    with l:
        st.markdown("#### SmartAging insight")
        st.write(row.SmartAging_insight)
    with r:
        st.markdown("#### Highest-priority signals")
        st.write(f"1. **{row.Priority_1}**")
        st.write(f"2. **{row.Priority_2}**")

def render_domain(domain):
    info=DOMAIN_INFO[domain]
    st.markdown(f"### {info['icon']} {info['title']}")
    st.caption(info["subtitle"]+" · Each measure is shown against the participant's own baseline.")
    metrics=info["metrics"]
    for start in range(0,len(metrics),4):
        cols=st.columns(min(4,len(metrics)-start))
        for col,item in zip(cols,metrics[start:start+4]):
            key,label,unit,adverse_high=item
            cur=float(row[key]); b=float(base[key])
            d=delta_pct(cur,b)
            with col:
                st.metric(label,f"{fmt(key,cur)} {unit}".strip(),f"{d:+.1f}% vs baseline")
                st.caption(delta_label(key,cur,b,adverse_high))
    st.markdown("#### Longitudinal trend")
    keys=[m[0] for m in metrics]
    trends=p.set_index("Month")[keys].copy()
    trends.columns=[m[1] for m in metrics]
    st.line_chart(trends,height=330,x_label="Month")

with tabs[1]:
    render_domain("Function")
    st.info("Camera-derived function is SmartAging's key additional layer: it measures how the participant moves, not only physiology or laboratory status.")

with tabs[2]:
    render_domain("Physiology")

with tabs[3]:
    render_domain("Metabolic")

with tabs[4]:
    render_domain("Body")

with tabs[5]:
    st.markdown("### SmartAging AI")
    st.caption("Prototype logic: detect persistent change → identify co-changing domains → prioritize → explain.")
    l,r=st.columns([1.25,1])
    with l:
        st.markdown("#### What changed?")
        st.write(row.SmartAging_insight)
        domain_scores=pd.DataFrame({
            "Domain":["Function","Physiology","Metabolic","Body composition"],
            "Change index":[row.Function_issue_score,row.Physiology_issue_score,row.Metabolic_issue_score,row.Body_issue_score]
        }).set_index("Domain")
        st.bar_chart(domain_scores,height=300)
    with r:
        st.metric("Demo prioritization index",f"{float(row.Overall_demo_score):.0f}/100")
        st.write(f"**{row.Overall_flag}**")
        st.markdown("#### Priorities")
        st.write(f"1. **{row.Priority_1}**")
        st.write(f"2. **{row.Priority_2}**")
        st.caption("This index is a prototype prioritization construct, not a disease probability or validated clinical risk score.")

with tabs[6]:
    st.markdown("### Personalized preventive Action Plan")
    a,b=st.columns(2)
    with a:
        st.markdown("#### Priority action 1")
        st.write(row.Recommended_action_1)
    with b:
        st.markdown("#### Priority action 2")
        st.write(row.Recommended_action_2)
    st.markdown("#### Re-measure")
    st.success(row.Follow_up)
    if profile=="Intervention Response":
        st.info("Month 6 is the simulated action-plan point. Later visits demonstrate how SmartAging would reassess the trajectory.")

with tabs[7]:
    st.markdown("### Progress & response")
    prog=p.set_index("Month")[["Overall_demo_score"]].copy()
    prog.columns=["Overall demo prioritization"]
    st.line_chart(prog,height=330,x_label="Month",y_label="Demo prioritization index")
    if profile=="Intervention Response" and float(row.Month)>6:
        m6=p[p.Month.eq(6)].iloc[0]
        domain_cols=["Function_issue_score","Physiology_issue_score","Metabolic_issue_score","Body_issue_score"]
        improved=sum(float(row[c])<float(m6[c]) for c in domain_cols)
        change=float(row.Overall_demo_score)-float(m6.Overall_demo_score)
        st.markdown(f"### {improved}/4 domains improved versus Month 6")
        if change<0:
            st.success(f"Synthetic response signal: prioritization index decreased by {abs(change):.0f} points versus Month 6.")
        else:
            st.warning(f"Synthetic response signal: prioritization index increased by {change:.0f} points versus Month 6.")
        st.caption("Synthetic response only; this does not demonstrate that SmartAging or AI caused the improvement.")
    elif profile=="Intervention Response":
        st.info("Select Month 9 or Month 12 to view the simulated post-action reassessment.")
    else:
        st.write("Repeated measurements are compared with the participant's personal baseline to identify persistence, stabilization or improvement.")

st.divider()
st.markdown('<div class="loop">MEASURE → DETECT → UNDERSTAND → ACT → RE-MEASURE → ASSESS RESPONSE</div>',unsafe_allow_html=True)

with st.expander("Methods & transparency"):
    st.write("""The cohort and trajectories are fully synthetic and are intended only to demonstrate the SmartAging product workflow. Domain and overall indices are prototype constructs. Recommendations are curated preventive examples. Clinical deployment would require evidence-based thresholds, validation, safety and escalation logic, governance and regulatory assessment.""")
    st.markdown("**SmartAging Deep:** optional MRI + metabolomics/lipidomics for deeper phenotyping and future validation.")

with st.expander("Raw participant data"):
    st.dataframe(p,use_container_width=True,hide_index=True)
