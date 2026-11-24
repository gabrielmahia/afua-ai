import streamlit as st
import html, os, urllib.request, json

st.set_page_config(page_title="Afua AI — Afya ya Akili", page_icon="🧠", layout="centered")
st.markdown("""<style>
.stApp{background:#0a080f;color:#ede7f6}
.afua-card{background:#1a0a2e;border:1px solid #4a148c;border-radius:10px;padding:14px 18px;margin:8px 0}
.crisis{background:#1a0000;border:2px solid #ff0000;border-radius:8px;padding:12px;margin:8px 0;font-weight:bold}
.stButton>button{background:#6a1b9a;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

def _secret(name):
    """Read a Streamlit secret, falling back to the environment; never crash when no secrets file exists."""
    try:
        v = st.secrets.get(name)
    except Exception:
        v = None
    return v or os.environ.get(name, "")

API_KEY = _secret("GOOGLE_API_KEY") or _secret("GEMINI_API_KEY")
MODEL = _secret("GEMINI_MODEL") or "gemini-3.5-flash-lite"  # the 1.5 Flash model this app used was retired by Google
# Crisis line always visible
st.markdown('<div class="crisis">🆘 MSAADA WA DHARURA: Befrienders Kenya: +254 722 178 177 (simu/SMS/WhatsApp, Jumatatu–Ijumaa saa 3 asubuhi–11 jioni) | befrienderskenya.org<br>Hatari ya haraka au nje ya saa hizo: piga 999 / 112 (bure) au nenda hospitali iliyo karibu SASA.</div>', unsafe_allow_html=True)

SYSTEM = """Wewe ni msaada wa kwanza wa afya ya akili Kenya. Jibu kwa upole na huruma kwa Kiswahili.
KILA WAKATI: Onyesha unataka kumsikiliza. Usitoe ushauri wa haraka.
Kama mtu anaonyesha dalili za hatari kwa nafsi yake au wengine — WEKA nambari ya dharura mara moja: Befrienders Kenya +254 722 178 177 (Jumatatu–Ijumaa saa 3 asubuhi–11 jioni); nje ya saa hizo au hatari ya haraka: 999 au 112. Usibuni nambari nyingine za simu.
Usijaribu kutatua matatizo ya kisaikolojia mazito — elekeza kwa wataalamu.
Toa rasilimali za afya ya akili Kenya. Kupiga vita stigma ni sehemu ya kazi yako."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.4,"maxOutputTokens":600}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":API_KEY},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return html.escape(json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e: return html.escape(f"❌ {e}")

st.markdown("# 🧠 Afua AI")
st.markdown("**Afya ya Akili — Msaada wa Kwanza kwa Kiswahili**")
st.info("💜 Hapa ni salama. Unaweza kuongea kuhusu chochote. Hakuna hukumu.")

tab1,tab2,tab3 = st.tabs(["💬 Zungumza Nami","📚 Habari za Afya ya Akili","🏥 Tafuta Msaada"])

with tab1:
    feeling = st.text_area("Unajisikiaje leo? Unaweza kuniambia kwa uhuru:", height=120,
                           placeholder="Niambie kinachokusumbua au kinachokufurahisha...")
    if st.button("💬 Niambie Zaidi", key="talk_btn") and feeling:
        with st.spinner("Ninakusikiliza..."):
            result = ask(f"Mtu anasema: '{feeling}'. Msikilize kwa huruma na umwulize swali moja la kuelewa zaidi. Usiharakishe kutoa ushauri.")
        st.markdown(f'<div class="afua-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    topic = st.selectbox("Soma kuhusu:", [
        "Msongo wa mawazo (stress) — nini na jinsi ya kudhibiti",
        "Wasiwasi (anxiety) — dalili na msaada",
        "Huzuni (depression) — si udhaifu, ni ugonjwa",
        "Kukosa usingizi — sababu na tiba",
        "Kuongea na mtu kuhusu hali ya akili — jinsi ya kuanza",
        "Stigma ya afya ya akili Kenya — jinsi ya kupigana nayo",
        "Watoto na afya ya akili — dalili za kuwa makini",
    ])
    if st.button("📚 Soma", key="info_btn"):
        with st.spinner("..."): result = ask(topic + " Kenya. Toa habari za kisayansi lakini kwa lugha ya kawaida. Ondoa aibu.")
        st.markdown(f'<div class="afua-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    county3 = st.selectbox("Kaunti yako:", ["Nairobi","Mombasa","Kisumu","Nakuru","Eldoret","Nyeri","Thika"])
    if st.button("🏥 Tafuta Msaada Karibu", key="help_btn"):
        with st.spinner("..."): result = ask(f"Vituo vya afya ya akili na mashauri {county3} Kenya. Toa: Hospitali, mashirika ya NGO, hotlines, bei (pamoja na bure), na jinsi ya kuwasiliana.")
        st.markdown(f'<div class="afua-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🧠 Afua AI v1.0 | 🆘 Befrienders Kenya: +254 722 178 177 (Jtt–Ijm) · Dharura: 999 / 112 | Si mbadala wa daktari | CC BY-NC-ND 4.0")
