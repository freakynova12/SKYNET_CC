# 🚀 Skynet_CC – Agentic Payment Operations Control Center

Skynet_CC is an **agentic AI-powered payment operations system** that simulates, monitors, and autonomously optimizes digital payment flows in real time.  
It demonstrates how an intelligent agent can **observe live signals, reason about failures, make constrained decisions, act safely, and learn continuously**—all under production-style guardrails.

This project is designed to mirror how modern **fintech payment ops teams** operate, replacing static rule-based monitoring with an **adaptive AI decision-maker** and a live analytics dashboard.

---

## 🧠 Core Capabilities

Skynet_CC implements a complete **Observe → Reason → Decide → Act → Learn** loop.

### 1️⃣ Observe
- Ingests simulated payment transactions
- Tracks:
  - Success / failure outcomes
  - Latency (ms)
  - Retry behavior
  - Risk and confidence signals

### 2️⃣ Reason
- Aggregates transactions into rolling metrics
- Detects:
  - Success rate degradation
  - Latency spikes
  - Retry amplification patterns
- Applies confidence and sample-size checks before acting

### 3️⃣ Decide
- Agent evaluates corrective actions such as:
  - Traffic throttling
  - Retry tuning
  - Rerouting recommendations
- Decisions are bounded by **strict guardrails**

### 4️⃣ Act
- Executes actions through a controlled simulation layer
- Ensures:
  - Limited blast radius
  - Rate-limited actions
  - Automatic rollback on negative impact

### 5️⃣ Learn
- Adaptive thresholds evolve based on outcomes
- Agent becomes more conservative or aggressive over time

---

## 📊 Interactive Dashboard

The system includes a **Streamlit-based real-time dashboard** that functions as a Payment Ops Control Center.

### Dashboard Features
- Live transaction simulation
- Success rate & latency graphs
- Agent decision logs
- Agent ON / OFF toggle
- Manual simulation controls
- Transparent reasoning visibility

This makes Skynet_CC ideal for:
- Live demos
- System design interviews
- Agentic AI showcases

---

## 🏗️ Project Structure
Skynet_CC/
├── frontend/
│ └── dashboard.py # Streamlit UI
├── core/
│ ├── agent.py # PaymentOpsAgent logic
│ ├── signals.py # Signal definitions
│ └── policies.py # Decision constraints
├── simulation/
│ └── simulator.py # Payment transaction simulator
├── adaptive.py # Learning & threshold adaptation
├── main.py # Application entry point
├── requirements.txt # Python dependencies
└── README.md
