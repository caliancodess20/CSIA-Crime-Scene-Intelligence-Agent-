# 🧠 NeuralWatch
### Neuromorphic AI Integrity Monitor for Cybersecurity

> *"Every existing cybersecurity tool monitors network traffic — the road. NeuralWatch monitors the brain driving the car."*

---

## The Problem

Modern AI-powered cybersecurity systems use neural networks to detect threats. These networks store their "knowledge" in **synaptic weights** — numbers that change as the AI learns.

A sophisticated attacker doesn't attack your system directly. They slowly feed the AI tiny amounts of corrupted data over weeks or months — gradually shifting its weights until the AI begins treating real attacks as normal traffic. This is called **neural poisoning**, and no consumer security product watches for it.

By the time the breach happens, the AI itself is compromised. Everyone was watching the door. Nobody was watching the guard.

---

## Our Solution: NeuralWatch

NeuralWatch is a three-layer neuromorphic security system that treats the AI's own neural weights as a security surface.

### Layer 1 — Biometric Gesture Lock
Only an authorized engineer, performing a specific hand gesture detected via webcam, can access the monitoring dashboard. Powered by **MediaPipe hand landmark detection**.

### Layer 2 — Neuromorphic Drift Detection (LIF Model)
NeuralWatch simulates a **Leaky Integrate-and-Fire (LIF) neuron** — the foundational model of neuromorphic computing — to monitor the AI's synaptic weights in real time.

```
Normal learning  →  tiny random weight changes  →  membrane potential leaks away  →  no spike
Attack in progress  →  consistent directional drift  →  membrane builds up  →  SPIKE FIRED  →  ALERT
```

The key insight: we don't just check if weights changed. We check **how they change over time** — using the same temporal pattern recognition that biological neurons use.

### Layer 3 — Cryptographic Tamper-Evident Audit Log
Every monitoring event is written to an **append-only log with SHA-256 chained signatures** — similar to blockchain. Each entry includes the hash of the previous entry. If an attacker gains access and tries to delete their tracks, the chain breaks immediately and a secondary alert fires.

---

## Why This Is Different From Existing AI

| Existing Security AI | NeuralWatch |
|---------------------|-------------|
| Monitors network traffic (the road) | Monitors the AI's brain (the driver) |
| Detects known attack signatures | Detects behavioral drift over time |
| Can be fooled by slow, patient attackers | Catches low-and-slow poisoning via LIF accumulation |
| No audit trail for AI weight changes | Cryptographically signed weight-change history |
| Logs are editable | Tamper-evident chained log — edits are instantly detected |

---

## Neuromorphic Computing Explained

Traditional computers process everything continuously using binary (0s and 1s). Neuromorphic computers mimic the human brain — neurons rest silently, then fire a **spike** only when a meaningful threshold is crossed. The timing between spikes carries the information.

NeuralWatch applies this principle to cybersecurity:

- **Membrane potential** accumulates with each suspicious weight drift
- **Leak rate** naturally dissipates during normal, healthy learning
- **Spike fires** when accumulated drift crosses the threshold — even from a slow, multi-day attack

This is the **Leaky Integrate-and-Fire (LIF) model** — the same model used in neuromorphic research at Intel (Loihi chip) and IBM (TrueNorth chip).

---

## Real-World Relevance

The **SolarWinds attack (2020)** — one of the largest cyberattacks in history — went undetected for 9 months. Attackers moved slowly and patiently. Every AI security system gave them a green light because each individual action looked normal.

NeuralWatch's LIF model would have caught the cumulative drift in the AI's behavior patterns.

---

## Tech Stack

- **Python 3.10+**
- **NumPy** — synaptic weight simulation
- **Streamlit** — real-time dashboard
- **MediaPipe** — hand gesture detection (Layer 1)
- **OpenCV** — webcam access
- **hashlib (SHA-256)** — tamper-evident log chain (Layer 3)

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/neuralwatch
cd neuralwatch

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch NeuralWatch
streamlit run dashboard.py
```

Then open your browser at `http://localhost:8501`

**For gesture authentication:** Allow webcam access and show 2 fingers for 2 seconds.
**For demo without webcam:** Click "Demo Bypass."

---

## Demo Walkthrough

1. **Launch** — Login screen appears, requiring biometric gesture (Layer 1)
2. **Authenticate** — Show 2 fingers to webcam OR click Demo Bypass
3. **Start Monitoring** — Click ▶ Start in sidebar
4. **Observe** — Watch neural drift stay safely below threshold (green)
5. **Activate Attack** — Toggle "Simulate Attacker" in sidebar
6. **Watch** — Drift graph rises, membrane potential builds, spike fires, red alert activates
7. **Rollback** — Click Rollback Brain — brain restored to clean baseline
8. **Tamper Demo** — Click "Simulate Tamper Attack" then "Verify Log Chain" to see tamper detection

---

## Team

Built at [Hackathon Name] | Domain: Cybersecurity | Track: Neuromorphic Computing

---

## References

- Mahowald et al. (2023) — Leaky Integrate-and-Fire neuron models in neuromorphic hardware
- Intel Loihi 2 neuromorphic chip documentation
- MITRE ATT&CK Framework — ML Model Poisoning (T1565)
- SolarWinds attack post-mortem (CISA, 2021)
