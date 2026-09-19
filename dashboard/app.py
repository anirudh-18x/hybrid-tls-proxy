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
# HEADER
# =========================================================

st.title("🔐 Hybrid TLS Security Dashboard")

st.caption(
    "Live monitoring of Classical and Post-Quantum Hybrid TLS"
)


# =========================================================
# NO DATA
# =========================================================

if data is None:

    st.warning(
        "Waiting for TLS proxy metrics..."
    )

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
# CONNECTION STATUS
# =========================================================

st.subheader("Live Connection Status")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Current Mode",
        mode_display
    )


with col2:

    st.metric(
        "TLS Version",
        data.get("tls_version", "Unknown")
    )


with col3:

    st.metric(
        "Key Establishment",
        data.get("backend_group", "Unknown")
    )


if mode == "hybrid":

    st.success(
        f"🟢 HYBRID TLS ACTIVE — "
        f"{mode_description}"
    )

else:

    st.info(
        f"🔵 CLASSICAL TLS ACTIVE — "
        f"{mode_description}"
    )


# =========================================================
# SECURITY DETAILS
# =========================================================

st.subheader("🔐 Security Configuration")

col1, col2, col3 = st.columns(3)


with col1:

    st.write("### Key Establishment")

    st.code(
        data.get(
            "backend_group",
            "Unknown"
        )
    )


with col2:

    st.write("### Authentication")

    st.code(
        data.get(
            "authentication",
            "Unknown"
        )
    )


with col3:

    st.write("### Cipher Suite")

    st.code(
        data.get(
            "cipher",
            "Unknown"
        )
    )


# =========================================================
# PERFORMANCE
# =========================================================

st.subheader("⚡ Performance")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Handshake Time",
        f'{data.get("handshake_time_ms", 0)} ms'
    )


with col2:

    st.metric(
        "Request",
        f'{data.get("request_bytes", 0)} bytes'
    )


with col3:

    st.metric(
        "Response",
        f'{data.get("response_bytes", 0)} bytes'
    )


# =========================================================
# CONNECTION FLOW
# =========================================================

st.subheader("🌐 Current Connection Flow")

if mode == "hybrid":

    st.code(
        """
LEGACY APPLICATION
        │
        │ TLS 1.3
        │ X25519
        ▼
┌─────────────────────┐
│     TLS PROXY       │
│                     │
│ TLS Termination     │
│ Monitoring          │
└──────────┬──────────┘
           │
           │ TLS 1.3
           │ X25519MLKEM768
           │ RSA-PSS
           ▼
     ┌───────────┐
     │  BACKEND  │
     └───────────┘
        """,
        language="text"
    )

else:

    st.code(
        """
LEGACY APPLICATION
        │
        │ TLS 1.3
        │ X25519
        ▼
┌─────────────────────┐
│     TLS PROXY       │
│                     │
│ TLS Termination     │
│ Monitoring          │
└──────────┬──────────┘
           │
           │ TLS 1.3
           │ X25519
           │ RSA-PSS
           ▼
     ┌───────────┐
     │  BACKEND  │
     └───────────┘
        """,
        language="text"
    )


# =========================================================
# EXPLANATION
# =========================================================

st.subheader("📌 What is happening?")

if mode == "hybrid":

    st.markdown(
        """
**Hybrid mode is currently active.**

The proxy is using **X25519MLKEM768**, which combines:

- **X25519** — classical elliptic-curve key establishment
- **ML-KEM-768** — post-quantum key encapsulation

The TLS connection therefore provides a hybrid key-establishment
mechanism while maintaining the existing RSA authentication.
        """
    )

else:

    st.markdown(
        """
**Classical mode is currently active.**

The proxy is using **X25519** for TLS key establishment.

This provides the baseline against which the hybrid
post-quantum configuration can be compared.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Dashboard refreshes automatically every 2 seconds • "
    "Metrics are generated by the TLS proxy"
)
