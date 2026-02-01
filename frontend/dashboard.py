import streamlit as st
import pandas as pd
import asyncio
import time
import random
import numpy as np
import altair as alt

from core.agent import PaymentOpsAgent, PaymentSignal

# ==================================================
# PAGE SETUP
# ==================================================
st.set_page_config(layout="wide")
st.title("💳 Payment Operations Agent")

agent = PaymentOpsAgent()

# ==================================================
# SESSION STATE
# ==================================================
if "signals" not in st.session_state:
    st.session_state.signals = []

if "batch_id" not in st.session_state:
    st.session_state.batch_id = 1

# ==================================================
# SIDEBAR – INPUTS
# ==================================================
st.sidebar.header("Manual Transaction Input")

total_tx = st.sidebar.number_input("Total Transactions", min_value=1, value=50)
success_tx = st.sidebar.number_input("Successful Transactions", min_value=0, value=40)
failed_tx = st.sidebar.number_input("Failed Transactions", min_value=0, value=10)

valid = (success_tx + failed_tx == total_tx)
if not valid:
    st.sidebar.error("❌ Successful + Failed must equal Total")

avg_latency = st.sidebar.slider("Average Latency (ms)", 50, 3000, 300)
p95_latency = st.sidebar.slider("P95 Latency (ms)", 50, 3000, 600)

issuer = st.sidebar.selectbox("Issuer", ["HDFC", "CITI", "CHASE", "HSBC"])
processor = st.sidebar.selectbox("Processor", ["VISA", "MASTERCARD", "AMEX"])
payment_method = st.sidebar.selectbox("Payment Method", ["CARD", "UPI", "NETBANKING"])

amount = st.sidebar.number_input("Avg Transaction Value ($)", min_value=1.0, value=100.0)

add_tx = st.sidebar.button("➕ Add Transactions", disabled=not valid)
clear_log = st.sidebar.button("🧹 Clear Log")

# ==================================================
# CLEAR LOG
# ==================================================
if clear_log:
    st.session_state.signals.clear()
    st.session_state.batch_id = 1
    st.success("🧹 Log cleared")

# ==================================================
# ADD TRANSACTIONS (NEW BATCH)
# ==================================================
if add_tx and valid:
    now = time.time()
    batch = st.session_state.batch_id

    for _ in range(success_tx):
        sig = PaymentSignal(
            transaction_id=f"S-{len(st.session_state.signals)}",
            amount=random.uniform(amount * 0.7, amount * 1.3),
            status="success",
            issuer_bank=issuer,
            processor=processor,
            payment_method=payment_method,
            latency_ms=random.uniform(avg_latency * 0.7, avg_latency * 1.1),
            timestamp=now - random.uniform(0, 600),  # IMPORTANT FIX
        )
        sig.batch_id = batch
        asyncio.run(agent.process_payment_signal(sig))
        st.session_state.signals.append(sig)

    for _ in range(failed_tx):
        sig = PaymentSignal(
            transaction_id=f"F-{len(st.session_state.signals)}",
            amount=random.uniform(amount * 0.7, amount * 1.3),
            status="failure",
            issuer_bank=issuer,
            processor=processor,
            payment_method=payment_method,
            latency_ms=random.uniform(p95_latency * 0.9, p95_latency * 1.3),
            error_code="TIMEOUT",
            timestamp=now - random.uniform(0, 600),  # IMPORTANT FIX
        )
        sig.batch_id = batch
        asyncio.run(agent.process_payment_signal(sig))
        st.session_state.signals.append(sig)

    st.session_state.batch_id += 1
    st.success(f"✅ Batch {batch} added")

# ==================================================
# BUILD DATAFRAME
# ==================================================
if not st.session_state.signals:
    st.info("No transactions yet.")
    st.stop()

df = pd.DataFrame([{
    "Status": s.status,
    "Issuer": s.issuer_bank,
    "Processor": s.processor,
    "Payment Method": s.payment_method,
    "Latency": s.latency_ms,
    "Amount": s.amount,
    "Timestamp": pd.to_datetime(s.timestamp, unit="s"),
    "Batch": getattr(s, "batch_id", 0),
} for s in st.session_state.signals])

# ==================================================
# METRICS
# ==================================================
c1, c2, c3 = st.columns(3)
c1.metric("Success Rate", f"{(df['Status']=='success').mean()*100:.1f}%")
c2.metric("Avg Latency", f"{df['Latency'].mean():.0f} ms")
c3.metric("Total Transactions", len(df))

# ==================================================
# GRAPH 1 — OUTCOMES PER BATCH (STACKED BAR)
# ==================================================
st.subheader("📊 Transaction Outcomes per Iteration")

batch_counts = (
    df.groupby(["Batch", "Status"])
    .size()
    .reset_index(name="Count")
)

chart1 = alt.Chart(batch_counts).mark_bar().encode(
    x=alt.X("Batch:N", title="Iteration"),
    y=alt.Y("Count:Q", title="Transactions"),
    color=alt.Color(
        "Status:N",
        scale=alt.Scale(
            domain=["success", "failure"],
            range=["#2ca02c", "#d62728"]
        )
    ),
    tooltip=["Batch", "Status", "Count"]
)

st.altair_chart(chart1, use_container_width=True)

# ==================================================
# GRAPH 2 — LATENCY DISTRIBUTION (BOXPLOT)
# ==================================================
st.subheader("⏱ Latency Distribution (Success vs Failure)")

chart2 = alt.Chart(df).mark_boxplot(extent="min-max").encode(
    x=alt.X("Status:N", title="Status"),
    y=alt.Y("Latency:Q", title="Latency (ms)"),
    color=alt.Color(
        "Status:N",
        scale=alt.Scale(
            domain=["success", "failure"],
            range=["#2ca02c", "#d62728"]
        )
    )
)

st.altair_chart(chart2, use_container_width=True)

# ==================================================
# GRAPH 3 — FAILURE RATE OVER TIME (LINE)
# ==================================================
st.subheader("📈 Failure Rate Over Time")

time_fail = (
    df.assign(is_failure=df["Status"] == "failure")
      .set_index("Timestamp")
      .resample("1min")["is_failure"]
      .mean()
      .mul(100)
)

st.line_chart(time_fail)

# ==================================================
# GRAPH 4 — FAILURE RATE BY AMOUNT PER BATCH
# ==================================================
st.subheader("💸 Failure Rate by Transaction Amount (per Iteration)")

df["Amount Bucket"] = pd.cut(
    df["Amount"],
    bins=[0, 50, 100, 200, 500, np.inf],
    labels=["0–50", "50–100", "100–200", "200–500", "500+"],
)

amount_fail = (
    df.assign(is_failure=df["Status"] == "failure")
      .groupby(["Batch", "Amount Bucket"], observed=True)["is_failure"]
      .mean()
      .mul(100)
      .reset_index()
)

chart4 = alt.Chart(amount_fail).mark_bar().encode(
    x=alt.X("Amount Bucket:N", title="Transaction Amount ($)"),
    y=alt.Y("is_failure:Q", title="Failure Rate (%)"),
    color=alt.Color("Batch:N", title="Iteration"),
    column=alt.Column("Batch:N", title="Batch"),
    tooltip=["Batch", "Amount Bucket", "is_failure"]
)

st.altair_chart(chart4, use_container_width=True)

# ==================================================
# RAW LOG
# ==================================================
st.subheader("📡 Transaction Log")
st.dataframe(df, use_container_width=True)
