import json
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hybrid TLS Security Dashboard",
    page_icon="🔐",
    layout="wide"
)


# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=2000,
    key="tls_dashboard_refresh"
)


# =========================================================
# HTML RENDER HELPER
# ---------------------------------------------------------
# st.markdown() runs content through a Markdown parser before
# rendering HTML. Any line starting with 4+ spaces of
# indentation is treated as a Markdown "indented code block"
# and shown as literal text instead of rendered HTML/SVG.
# Since f-strings built inside indented functions inherit that
# indentation, we strip leading whitespace from every line
# before handing the string to st.markdown.
# =========================================================
def html(content: str):
    lines = [line.lstrip() for line in content.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


# =========================================================
# NEO-BRUTALISM UI
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* {
    box-sizing: border-box;
}

.stApp {
    background: #f3f0e8;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

h1, h2, h3 {
    color: #111111 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
}

p {
    color: #222222;
}


/* =========================================================
   HEADER
   ========================================================= */

.hero {
    background: #ffffff;
    border: 4px solid #111111;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 9px 9px 0px #111111;
}

.hero-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -2px;
    color: #111111;
}

.hero-subtitle {
    margin-top: 14px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #333333;
}

.badge {
    background: #f4df3a;
    border: 3px solid #111111;
    padding: 10px 15px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 4px 4px 0px #111111;
}


/* =========================================================
   SECTION LABELS
   ========================================================= */

.section-label {
    display: inline-block;
    background: #111111;
    color: #ffffff !important;
    padding: 9px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 18px;
}


/* =========================================================
   CUSTOM METRIC CARDS
   ========================================================= */

.metric-card {
    min-height: 145px;
    padding: 20px;
    border: 4px solid #111111;
    box-shadow: 7px 7px 0px #111111;
    margin-bottom: 15px;
}

.metric-card.blue {
    background: #65b8ff;
}

.metric-card.yellow {
    background: #f4df3a;
}

.metric-card.green {
    background: #68ef76;
}

.metric-card.pink {
    background: #ff78b8;
}

.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 15px;
    color: #111111;
}

.metric-value {
    font-size: 29px;
    font-weight: 700;
    line-height: 1.1;
    color: #111111;
    overflow-wrap: anywhere;
}


/* =========================================================
   STATUS
   ========================================================= */

.status-box {
    border: 4px solid #111111;
    padding: 18px 22px;
    margin: 12px 0 28px 0;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 6px 6px 0px #111111;
}

.status-hybrid {
    background: #68ef76;
}

.status-classical {
    background: #65b8ff;
}

.status-dot {
    display: inline-block;
    width: 13px;
    height: 13px;
    background: #111111;
    margin-right: 10px;
}


/* =========================================================
   SECURITY CARDS
   ========================================================= */

.security-card {
    background: #ffffff;
    border: 4px solid #111111;
    padding: 20px;
    min-height: 145px;
    box-shadow: 6px 6px 0px #111111;
    margin-bottom: 15px;
}

.security-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 15px;
    color: #111111;
}

.security-value {
    background: #eeeeee;
    border: 3px solid #111111;
    padding: 13px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #111111;
    overflow-wrap: anywhere;
}


/* =========================================================
   STREAMLIT METRICS
   ========================================================= */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 4px solid #111111;
    padding: 18px !important;
    box-shadow: 6px 6px 0px #111111;
}

[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    color: #111111 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #111111 !important;
    font-size: 27px !important;
    font-weight: 700 !important;
}


    /* ---------- DIAGRAM ---------- */
    .rb-diagram {
        background: #ffffff;
        border: 4px solid #111111;
        box-shadow: 8px 8px 0px #111111;
        padding: 24px;
        margin-bottom: 30px;
    }
    .rb-legend {
        display: flex; gap: 20px; margin-top: 10px;
        font-size: 0.75rem; color: var(--dim);
    }
    .rb-legend .sw { display:inline-block; width:10px; height:10px; margin-right:6px; vertical-align:middle; border: 1px solid var(--white); }


/* =========================================================
   EXPLANATION
   ========================================================= */

.explanation {
    background: #fff7c7;
    border: 4px solid #111111;
    padding: 25px;
    box-shadow: 7px 7px 0px #111111;
    margin-bottom: 30px;
}

.explanation-heading {
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 15px;
    color: #111111;
}

.explanation p {
    color: #222222;
    line-height: 1.6;
}

.term {
    display: inline-block;
    background: #111111;
    color: #ffffff !important;
    padding: 3px 7px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}


/* =========================================================
   CODE BLOCKS
   ========================================================= */

.stCodeBlock {
    border: 4px solid #111111 !important;
    box-shadow: 7px 7px 0px #111111;
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {
    border: 4px solid #111111 !important;
    border-radius: 0px !important;
    box-shadow: 5px 5px 0px #111111;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {
    border: none !important;
    border-top: 4px solid #111111 !important;
    margin-top: 35px !important;
    margin-bottom: 20px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    border: 4px solid #111111;
    padding: 16px 20px;
    box-shadow: 5px 5px 0px #111111;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #111111;
}

.footer-left {
    font-weight: 700;
}

.footer-right {
    text-align: right;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .hero-title {
        font-size: 30px;
    }

    .hero-top {
        flex-direction: column;
    }

    .flow-row {
        flex-direction: column;
    }

    .flow-arrow {
        transform: rotate(90deg);
    }

    .footer {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FILE LOCATION
# =========================================================

RESULT_FILE = Path("results/latest.json")


# =========================================================
# LOAD LATEST METRICS
# =========================================================

def load_metrics():

    if not RESULT_FILE.exists():
        return None

    try:

        with open(RESULT_FILE, "r") as file:
            return json.load(file)

    except Exception:

        return None


data = load_metrics()


# =========================================================
# ANIMATED CONNECTION FLOW DIAGRAM (SVG)
# =========================================================
def flow_diagram(mode, data):
    hybrid = mode == "hybrid"

    leg1_color = "#9e9797"
    leg2_color = "#39ff6a" if hybrid else "#9e9797"
    leg2_label_top = "TLS 1.3 · X25519MLKEM768" if hybrid else "TLS 1.3 · X25519"
    leg2_label_bottom = ""
    handshake = data.get("handshake_time_ms", "—")

    pq_badge = ""
    if hybrid:
        pq_badge = (
            '<g transform="translate(555,55)">'
            '<rect x="-34" y="-13" width="68" height="22" fill="#39ff6a" stroke="#f2f2f2" stroke-width="1.5"/>'
            '<text x="0" y="2" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            'font-size="10" font-weight="700" fill="#050505">HYBRID</text>'
            '</g>'
        )

    svg = f"""<svg viewBox="0 0 900 210" width="100%" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="arrow1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{leg1_color}"/></marker>
<marker id="arrow2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{leg2_color}"/></marker>
</defs>
<g transform="translate(30,75)">
<rect width="150" height="60" fill="#0c0c0c" stroke="#f2f2f2" stroke-width="3"/>
<text x="75" y="28" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#e8e8e8">LEGACY</text>
<text x="75" y="44" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#e8e8e8">APPLICATION</text>
</g>
<line x1="180" y1="105" x2="345" y2="105" stroke="{leg1_color}" stroke-width="2" marker-end="url(#arrow1)"/>
<line x1="180" y1="105" x2="345" y2="105" stroke="{leg1_color}" stroke-width="2" stroke-dasharray="6 10" opacity="0.9">
<animate attributeName="stroke-dashoffset" from="32" to="0" dur="1s" repeatCount="indefinite"/>
</line>
<circle r="4" fill="{leg1_color}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M180,105 L345,105"/></circle>
<text x="262" y="90" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#7a7a7a">TLS 1.3 · X25519</text>
<g transform="translate(345,55)">
<rect width="210" height="100" fill="#0c0c0c" stroke="{leg2_color}" stroke-width="3"/>
<text x="105" y="32" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="#e8e8e8">TLS PROXY</text>
<text x="105" y="52" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#7a7a7a">termination · monitoring</text>
<text x="105" y="78" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="{leg2_color}">handshake: {handshake} ms</text>
</g>
{pq_badge}
<line x1="555" y1="105" x2="720" y2="105" stroke="{leg2_color}" stroke-width="2" marker-end="url(#arrow2)"/>
<line x1="555" y1="105" x2="720" y2="105" stroke="{leg2_color}" stroke-width="2" stroke-dasharray="6 10" opacity="0.9">
<animate attributeName="stroke-dashoffset" from="32" to="0" dur="0.9s" repeatCount="indefinite"/>
</line>
<circle r="4" fill="{leg2_color}"><animateMotion dur="1.4s" repeatCount="indefinite" path="M555,105 L720,105"/></circle>
<text x="637" y="90" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="{leg2_color}">{leg2_label_top}</text>
<text x="637" y="128" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#7a7a7a">{leg2_label_bottom}</text>
<g transform="translate(720,75)">
<rect width="150" height="60" fill="#0c0c0c" stroke="#f2f2f2" stroke-width="3"/>
<text x="75" y="36" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#e8e8e8">BACKEND</text>
</g>
</svg>"""

    html(
        f"""
        <div class="rb-diagram">
            {svg}
            <div class="rb-legend">
                <span><span class="sw" style="background:{leg1_color};"></span>client &harr; proxy (classical)</span>
                <span><span class="sw" style="background:{leg2_color};"></span>proxy &harr; backend ({'hybrid post-quantum' if hybrid else 'classical'})</span>
            </div>
        </div>
        """
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
<div class="hero-top">

<div>

<div class="hero-title">
🔐 HYBRID TLS<br>SECURITY DASHBOARD
</div>

<div class="hero-subtitle">
LIVE MONITORING • CLASSICAL + POST-QUANTUM TLS
</div>

</div>

<div class="badge">
● LIVE MONITOR
</div>

</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# NO DATA
# =========================================================

if data is None:

    st.markdown("""
<div class="status-box status-classical">
<span class="status-dot"></span>
WAITING FOR TLS PROXY METRICS
</div>
""", unsafe_allow_html=True)

    st.info(
        "Start the TLS proxy and establish a connection."
    )

    st.stop()


# =========================================================
# CURRENT MODE
# =========================================================

mode = data.get("mode", "unknown").lower()


if mode == "hybrid":

    mode_display = "HYBRID"

    mode_description = (
        "Post-quantum hybrid key establishment is active."
    )

else:

    mode_display = "CLASSICAL"

    mode_description = (
        "Classical X25519 key establishment is active."
    )


# =========================================================
# LIVE CONNECTION STATUS
# =========================================================

st.markdown(
    '<div class="section-label">01 / LIVE CONNECTION STATUS</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    if mode == "hybrid":
        card_color = "green"
    else:
        card_color = "blue"

    st.markdown(f"""
<div class="metric-card {card_color}">

<div class="metric-label">
CURRENT MODE
</div>

<div class="metric-value">
{mode_display}
</div>

</div>
""", unsafe_allow_html=True)


with col2:

    st.markdown(f"""
<div class="metric-card yellow">

<div class="metric-label">
TLS VERSION
</div>

<div class="metric-value">
{data.get("tls_version", "Unknown")}
</div>

</div>
""", unsafe_allow_html=True)


with col3:

    st.markdown(f"""
<div class="metric-card pink">

<div class="metric-label">
KEY ESTABLISHMENT
</div>

<div class="metric-value">
{data.get("backend_group", "Unknown")}
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# ACTIVE STATUS
# =========================================================

if mode == "hybrid":

    st.markdown(f"""
<div class="status-box status-hybrid">
<span class="status-dot"></span>
HYBRID TLS ACTIVE — {mode_description}
</div>
""", unsafe_allow_html=True)

else:

    st.markdown(f"""
<div class="status-box status-classical">
<span class="status-dot"></span>
CLASSICAL TLS ACTIVE — {mode_description}
</div>
""", unsafe_allow_html=True)


# =========================================================
# SECURITY CONFIGURATION
# =========================================================

st.markdown(
    '<div class="section-label">02 / SECURITY CONFIGURATION</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(f"""
<div class="security-card">

<div class="security-title">
🔑 KEY ESTABLISHMENT
</div>

<div class="security-value">
{data.get("backend_group", "Unknown")}
</div>

</div>
""", unsafe_allow_html=True)


with col2:

    st.markdown(f"""
<div class="security-card">

<div class="security-title">
🛡️ AUTHENTICATION
</div>

<div class="security-value">
{data.get("authentication", "Unknown")}
</div>

</div>
""", unsafe_allow_html=True)


with col3:

    st.markdown(f"""
<div class="security-card">

<div class="security-title">
🔒 CIPHER SUITE
</div>

<div class="security-value">
{data.get("cipher", "Unknown")}
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-label">03 / PERFORMANCE</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "HANDSHAKE TIME",
        f'{data.get("handshake_time_ms", 0)} ms'
    )


with col2:

    st.metric(
        "REQUEST",
        f'{data.get("request_bytes", 0)} bytes'
    )


with col3:

    st.metric(
        "RESPONSE",
        f'{data.get("response_bytes", 0)} bytes'
    )


# CONNECTION FLOW (dynamic diagram)
# =========================================================
st.markdown(
    '<div class="section-label">04 / CONNECTION FLOW</div>',
    unsafe_allow_html=True
)

flow_diagram(mode, data)



# =========================================================
# WHAT IS HAPPENING?
# =========================================================

st.markdown(
    '<div class="section-label">05 / WHAT IS HAPPENING?</div>',
    unsafe_allow_html=True
)


if mode == "hybrid":

    st.markdown("""
<div class="explanation">

<div class="explanation-heading">
🟢 Hybrid mode is currently active
</div>

<p>
The TLS proxy is using a hybrid key-establishment mechanism.
</p>

<p>
<span class="term">X25519</span>
provides the classical elliptic-curve component.
</p>

<p>
<span class="term">ML-KEM-768</span>
provides the post-quantum key-establishment component.
</p>

<p>
Both mechanisms contribute to the TLS key establishment,
allowing the legacy application to communicate through
the proxy without requiring changes to the application.
</p>

<p>
Authentication remains based on the configured
authentication mechanism.
</p>

</div>
""", unsafe_allow_html=True)

else:

    st.markdown("""
<div class="explanation">

<div class="explanation-heading">
🔵 Classical mode is currently active
</div>

<p>
The TLS proxy is currently using the classical
<span class="term">X25519</span>
key-establishment mechanism.
</p>

<p>
This configuration acts as the baseline for comparing
classical TLS with the hybrid post-quantum configuration.
</p>

<p>
The legacy application continues to communicate through
the TLS proxy without requiring application-level changes.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

<div class="footer-left">
🔐 TLS PROXY MONITOR
</div>

<div class="footer-right">
AUTO REFRESH: 2 SEC<br>
METRICS SOURCE: TLS PROXY
</div>

</div>
""", unsafe_allow_html=True)