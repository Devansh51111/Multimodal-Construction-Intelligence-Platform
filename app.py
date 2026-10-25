import json, os
from io import BytesIO
from urllib.parse import quote
import streamlit as st
from PIL import Image
try:
 from google import genai
 from google.genai import types
except ImportError: genai=types=None
st.set_page_config(page_title="Multimodal Construction Intelligence Platform",page_icon="🏗️",layout="wide")
st.markdown("""<style>.stApp{background:#0b1220;color:#e7edf5}[data-testid="stSidebar"]{background:#101a2a}h1,h2,h3{font-family:system-ui;letter-spacing:-.03em}div[data-testid="stMetric"]{background:#121e2e;border:1px solid #26384c;padding:1rem;border-radius:14px}.hero{padding:1.5rem;border:1px solid #294358;border-radius:20px;background:linear-gradient(120deg,#123648,#131f32)}.muted{color:#9eafc3}</style>""",unsafe_allow_html=True)
def key():
 try:return (st.session_state.get("gemini_key","") or st.secrets.get("GEMINI_API_KEY","") or os.getenv("GEMINI_API_KEY","")).strip()
 except Exception:return st.session_state.get("gemini_key","") or os.getenv("GEMINI_API_KEY","")
def client():
 try:return genai.Client(api_key=key()) if key() and genai else None
 except Exception:return None
def analyze(prompt,up=None):
 c=client()
 if not c:raise RuntimeError("Gemini API key not configured.")
 parts=[prompt]
 if up:
  im=Image.open(up).convert("RGB");b=BytesIO();im.save(b,format="JPEG",quality=90);parts.append(types.Part.from_bytes(data=b.getvalue(),mime_type="image/jpeg"))
 r=c.models.generate_content(model="gemini-2.5-flash",contents=parts,config=types.GenerateContentConfig(response_mime_type="application/json",temperature=.2))
 s=(r.text or "").strip()
 if s.startswith("~~~"):s=s.split("\n",1)[-1].removesuffix("~~~").strip()
 return json.loads(s[s.find("{"):s.rfind("}")+1])
def dl(d,n):st.download_button("⬇ Download JSON",json.dumps(d,indent=2),file_name=n,mime="application/json")
def demo_safety():return {"safety_score":78,"overall_status":"Needs Attention","ppe_detection":[{"item":"Safety helmet","detected":True,"notes":"Demo placeholder."},{"item":"High-visibility vest","detected":True,"notes":"Demo placeholder."},{"item":"Steel-toe boots","detected":None,"notes":"Not verified."},{"item":"Safety harness","detected":None,"notes":"Not verified."}],"hazards":[{"hazard":"Potential fall exposure","severity":"High","evidence":"Illustrative only; not image-derived.","corrective_remedy":"Check guardrails and fall-arrest systems before elevated work."},{"hazard":"Housekeeping risk","severity":"Medium","evidence":"Illustrative only.","corrective_remedy":"Clear walkways and segregate materials."}],"limitations":"DEMO MODE: no image was analyzed."}
def demo_crack():return {"defect_type":"Hairline","estimated_crack_width_mm":None,"confidence":"Low (demo)","observations":["Illustrative sample only."],"possible_root_causes":["Drying shrinkage","Thermal movement"],"recommended_repairs":["Document and monitor crack width with a scale.","Have an engineer approve any repair."],"urgency":"Routine inspection (demo only)","immediate_actions":["Photograph with ruler and location/date."],"limitations":"DEMO MODE: no image was analyzed."}
with st.sidebar:
 st.title("🏗️ Site Intelligence");st.caption("Skill Wallet · Capstone Project 1")
 st.text_input("Google Gemini API key",type="password",key="gemini_key")
 st.success("Live mode available") if key() and genai else st.info("Demo mode · add Gemini key for live analysis")
 st.markdown("### Architecture");st.write("Streamlit → validation → Gemini multimodal API → JSON")
 st.markdown("### Modules");st.write("1. Site safety & PPE\n2. Crack diagnostics\n3. Planning & valuation\n4. Daily assistant")
st.markdown('<div class="hero"><h1>Multimodal Construction Intelligence Platform</h1><p class="muted">Safety triage, defect insights, project planning and weather-aware site guidance.</p></div>',unsafe_allow_html=True)
a,b,c,d=st.tabs(["🦺 Site Safety & PPE Audit","🧱 Crack Diagnostics","📐 Planning & Valuation","🌦️ Daily Site Assistant"])
with a:
 st.subheader("Site safety & PPE visual audit");up=st.file_uploader("Site photo (JPG/PNG)",type=["jpg","jpeg","png"],key="safety")
 if up:st.image(up,use_container_width=True)
 p='Return ONLY JSON: {"safety_score":0-100,"overall_status":"Compliant|Needs Attention|Unsafe|Unable to Determine","ppe_detection":[{"item":"Safety helmet|High-visibility vest|Steel-toe boots|Safety harness","detected":true|false|null,"notes":"..."}],"hazards":[{"hazard":"...","severity":"Low|Medium|High|Critical","evidence":"...","corrective_remedy":"..."}],"limitations":"..."}. Use null for obscured PPE, state uncertainty, identify visible hazards only. Consider OSHA construction principles. IS 456 is a concrete design code, not a PPE standard. Never assert legal compliance from a photo.'
 if st.button("Analyze site safety",type="primary"):
  if not up:st.warning("Upload a photo first.")
  else:
   try:st.session_state.safety=analyze(p,up) if client() else demo_safety()
   except Exception as e:st.error(str(e))
 x=st.session_state.get("safety")
 if x:
  m,n,o=st.columns(3);m.metric("Visual score",f'{x.get("safety_score",0)}/100');n.metric("Status",x.get("overall_status","Unknown"));o.metric("Hazards",len(x.get("hazards",[])));st.progress(max(0,min(100,int(x.get("safety_score",0))))/100)
  st.markdown("#### PPE checklist")
  for i in x.get("ppe_detection",[]):st.write(f'{"✅" if i.get("detected") is True else "❌" if i.get("detected") is False else "⚠️"} **{i.get("item")}** — {i.get("notes","")}')
  st.markdown("#### Hazards and remedies")
  for h in x.get("hazards",[]):
   with st.expander(f'{h.get("severity","Unknown")}: {h.get("hazard","Hazard")}'):st.write(h.get("evidence",""));st.write("Remedy:",h.get("corrective_remedy",""))
  st.warning(x.get("limitations","Photo-based triage is uncertain."));dl(x,"site_safety_report.json")
with b:
 st.subheader("Concrete & wall defect triage");st.write("Use a close, well-lit image and include a ruler if possible.")
 up=st.file_uploader("Surface photo (JPG/PNG)",type=["jpg","jpeg","png"],key="crack")
 if up:st.image(up,use_container_width=True)
 p='Return ONLY JSON: {"defect_type":"Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Other/Unclear","estimated_crack_width_mm":number|null,"confidence":"Low|Medium|High","observations":["..."],"possible_root_causes":["..."],"recommended_repairs":["..."],"urgency":"Routine inspection|Prompt engineer review|Urgent - restrict area pending assessment","immediate_actions":["..."],"limitations":"..."}. Estimate width only with visible reliable scale. Distinguish evidence from hypotheses. Recommend epoxy injection or structural re-grouting only if engineer-approved and appropriate. Suspected shear, severe spalling, exposed rebar or deformation requires prompt structural engineer review. Never declare structure safe from a photo.'
 if st.button("Diagnose visible defect",type="primary"):
  if not up:st.warning("Upload a surface photo first.")
  else:
   try:st.session_state.crack=analyze(p,up) if client() else demo_crack()
   except Exception as e:st.error(str(e))
 x=st.session_state.get("crack")
 if x:
  m,n,o=st.columns(3);m.metric("Defect",x.get("defect_type","Unclear"));w=x.get("estimated_crack_width_mm");n.metric("Width",f"{w} mm" if w is not None else "Not measurable");o.metric("Urgency",x.get("urgency","Review"))
  for title,k in [("Observations","observations"),("Possible root causes","possible_root_causes"),("Recommended repairs","recommended_repairs"),("Immediate actions","immediate_actions")]:
   st.markdown("#### "+title)
   for q in x.get(k,[]):st.write("• "+str(q))
  st.warning(x.get("limitations","Photo triage is not engineering sign-off."));dl(x,"crack_diagnostics_report.json")
with c:
 st.subheader("Project planning & indicative valuation");st.info("Planning proxy only, not a certified valuation, BOQ or contractor quote.")
 typ=st.selectbox("Structure type",["Residential RCC","Commercial RCC","Industrial shed","Warehouse","Low-rise masonry"])
 area=st.number_input("Built-up area (sq ft)",100,2000000,2500,100);tier=st.selectbox("Location tier",["Tier 1","Tier 2","Tier 3"]);done=st.slider("Completion (%)",0,100,35,5)
 rate=st.number_input("Construction cost (₹/sq ft)",500,20000,{"Residential RCC":2200,"Commercial RCC":2800,"Industrial shed":1600,"Warehouse":1400,"Low-rise masonry":1500}[typ],100)
 landrate=st.number_input("Land value (₹/sq ft)",0,100000,{"Tier 1":4500,"Tier 2":2200,"Tier 3":900}[tier],100)
 sf=st.number_input("Steel intensity (kg/sq ft)",0.0,30.0,4.0 if typ in ["Industrial shed","Warehouse"] else 4.5,.5);cf=st.number_input("Cement intensity (bags/sq ft)",0.0,2.0,.4,.05)
 budget=area*rate;spent=budget*done/100;land=area*landrate;value=land+spent;steel=area*sf;cement=area*cf
 def money(v):return f"₹{v/1e7:.2f} Cr" if v>=1e7 else f"₹{v/1e5:.2f} L" if v>=1e5 else f"₹{v:,.0f}"
 m,n,o=st.columns(3);m.metric("Construction budget",money(budget));n.metric("CapEx incurred",money(spent));o.metric("Indicative asset value",money(value));st.progress(done/100,text=f"Milestone progress · {done}%")
 m,n,o=st.columns(3);m.metric("Steel estimate",f"{steel/1000:.1f} tonnes");n.metric("Cement estimate",f"{cement:,.0f} bags");o.metric("Remaining budget",money(budget-spent))
 st.caption("Replace assumptions with local quotes, approved drawings and BOQ.")
 prompt=f"Photorealistic conceptual 3D architectural render of a {typ.lower()} in an Indian {tier.lower()} city, approximately {area} sq ft, {done}% construction progress, realistic materials, daylight, no text or logos. Concept only."
 st.markdown("#### Conceptual 3D rendering");st.text_area("Pollinations prompt",prompt)
 st.link_button("Open rendering generator","https://image.pollinations.ai/prompt/"+quote(prompt,safe=""))
 dl({"structure_type":typ,"area_sqft":area,"location_tier":tier,"completion_percent":done,"construction_budget_inr":round(budget),"capex_incurred_inr":round(spent),"land_value_inr":round(land),"indicative_asset_value_inr":round(value),"steel_kg":round(steel),"cement_bags":round(cement),"disclaimer":"Indicative estimate only."},"project_planning_estimate.json")
with d:
 st.subheader("Weather-aware site advisory");weather=st.selectbox("Weather condition",["Normal","High Wind","Heavy Rain","Extreme Heat"])
 advice={"Normal":["Continue toolbox talks, PPE checks and housekeeping.","Follow approved concrete curing specifications."],"High Wind":["Pause crane/lifting work above equipment or lift-plan wind limits.","Secure loose materials and inspect temporary works."],"Heavy Rain":["Restrict flooded or unstable areas; authorized personnel manage electrical isolation.","Inspect excavations, scaffolds, access and drainage before re-entry.","Protect fresh concrete from washout."],"Extreme Heat":["Provide shade, water, cooler work hours and work-rest cycles.","Watch for heat illness and follow emergency response.","Follow approved hot-weather concrete curing protocol."]}
 st.markdown("### "+({"Normal":"🟢 Routine operations","High Wind":"🟠 Wind-risk controls","Heavy Rain":"🔴 Rain and electrical hazards","Extreme Heat":"🟠 Heat-stress controls"}[weather]))
 for q in advice[weather]:st.write("• "+q)
 st.caption("Follow local warnings, equipment manuals and site emergency plans.");st.divider();st.markdown("#### Construction engineering assistant")
 if "chat" not in st.session_state:st.session_state.chat=[]
 for msg in st.session_state.chat:
  with st.chat_message(msg["role"]):st.markdown(msg["content"])
 q=st.chat_input("Ask about materials, workflow, safety or planning…")
 if q:
  st.session_state.chat.append({"role":"user","content":q})
  with st.chat_message("user"):st.markdown(q)
  answer=""
  if client():
   try:
    hist=[{"role":"user" if z["role"]=="user" else "model","parts":[{"text":z["content"]}]} for z in st.session_state.chat[-12:]]
    hist.insert(0,{"role":"user","parts":[{"text":"You are a safety-first construction assistant in India. State assumptions and never replace qualified engineers, approved drawings, codes or emergency services. Current weather: "+weather}]})
    answer=client().models.generate_content(model="gemini-2.5-flash",contents=hist).text or "Please retry."
   except Exception as e:answer="Assistant error: "+str(e)
  else:answer="DEMO MODE: Connect Gemini for live answers. Check approved drawings/specifications and consult the competent site engineer for safety-critical decisions. Your question: "+q
  with st.chat_message("assistant"):st.markdown(answer)
  st.session_state.chat.append({"role":"assistant","content":answer})
st.divider();st.caption("Advisory only. AI is not a certified safety audit or structural diagnosis; estimates are not professional valuation or BOQ.")
