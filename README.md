
# CSIA – Crime Scene Intelligence Agent

CSIA (Crime Scene Intelligence Agent) is an AI-powered crime-scene intelligence platform designed to help investigators organize evidence, analyze investigation data, build investigation timelines, and receive structured next-step suggestions while keeping humans in control.

---

## 🚀 Current Module

This branch contains the **Timeline & Rule-Based Next-Step Suggestions module**.

The module takes investigation events as input, automatically organizes them chronologically, and generates rule-based suggestions for the investigator's next actions.

### Current Capabilities

* Build a chronological investigation timeline
* Process structured investigation events
* Generate rule-based next-step suggestions
* Expose functionality through a Flask REST API
* Validate the workflow using automated unit tests
* Keep investigator decisions human-controlled

---

## 🏗️ Architecture

```text
                 Investigation Events
                         │
                         ▼
              ┌─────────────────────┐
              │     Flask REST API  │
              │ /timeline/suggestions│
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Timeline Builder  │
              │                     │
              │ Sorts events by     │
              │ timestamp           │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  Next-Step Rule     │
              │      Engine         │
              │                     │
              │ Applies predefined  │
              │ investigation rules │
              └──────────┬──────────┘
                         │
                         ▼
                 Structured Response
                  ┌───────────────┐
                  │ Timeline      │
                  │ Next Steps    │
                  └───────────────┘
```

---

## 📁 Project Structure

```text
CSIA-Crime-Scene-Intelligence-Agent-
│
├── backend/
│   │
│   ├── run.py
│   │
│   └── app/
│       │
│       ├── __init__.py
│       │
│       └── timeline_suggestions/
│           │
│           ├── __init__.py
│           ├── routes.py
│           ├── timeline_builder.py
│           ├── next_step_rules.py
│           │
│           ├── test_timeline.py
│           ├── test_next_steps.py
│           └── test_full_flow.py
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Technologies Used

* Python 3.14
* Flask 3.1.3
* Python unittest
* REST API
* Git & GitHub

---

## 🧩 Timeline Builder

The Timeline Builder receives investigation events containing an event name and timestamp.

### Example Event

```json
{
    "event": "Evidence collected",
    "timestamp": "2026-08-24 15:30"
}
```

The events are sorted chronologically to create an ordered investigation timeline.

### Example Input

```json
[
    {
        "event": "Evidence collected",
        "timestamp": "2026-08-24 15:30"
    },
    {
        "event": "Witness statement",
        "timestamp": "2026-08-24 14:00"
    },
    {
        "event": "Case created",
        "timestamp": "2026-08-24 10:00"
    }
]
```

### Result

```text
2026-08-24 10:00 -> Case created
2026-08-24 14:00 -> Witness statement
2026-08-24 15:30 -> Evidence collected
```

---

## 🧠 Rule-Based Next-Step Engine

The Next-Step Engine analyzes events present in the investigation timeline and suggests reasonable subsequent actions using predefined rules.

It does **not automatically make investigative decisions**.

The investigator remains responsible for reviewing and acting on the suggestions.

### Current Rules

#### Rule 1 — Case Created

If a case has been created but evidence has not been collected:

> Collect and document available physical or digital evidence.

#### Rule 2 — Evidence Collected

If evidence has been collected but forensic analysis has not been completed:

> Perform forensic analysis on the collected evidence.

#### Rule 3 — Witness Statement

If a witness statement exists but a suspect interview has not been completed:

> Conduct a suspect interview based on available witness information.

#### Rule 4 — Forensic Analysis Completed

If forensic analysis is completed but a forensic report has not been generated:

> Generate and document the forensic analysis report.

#### Rule 5 — Forensic Report Generated

If the forensic report exists but the investigation has not been concluded:

> Review all evidence and prepare the investigation conclusion.

---

## 🌐 API

### Endpoint

```text
POST /timeline/suggestions
```

### Base URL

```text
http://127.0.0.1:5000
```

### Complete Endpoint

```text
http://127.0.0.1:5000/timeline/suggestions
```

---

## 📥 Request Format

The API accepts JSON containing an `events` array.

### Example Request

```json
{
    "events": [
        {
            "event": "Case created",
            "timestamp": "2026-08-24 10:00"
        },
        {
            "event": "Witness statement",
            "timestamp": "2026-08-24 14:00"
        },
        {
            "event": "Evidence collected",
            "timestamp": "2026-08-24 15:30"
        }
    ]
}
```

---

## 📤 Response

The API returns the generated timeline and suggested next steps.

### Example Response

```json
{
    "timeline": [
        {
            "event": "Case created",
            "timestamp": "2026-08-24 10:00"
        },
        {
            "event": "Witness statement",
            "timestamp": "2026-08-24 14:00"
        },
        {
            "event": "Evidence collected",
            "timestamp": "2026-08-24 15:30"
        }
    ],
    "next_steps": [
        "Perform forensic analysis on the collected evidence.",
        "Conduct a suspect interview based on available witness information."
    ]
}
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/caliancodess20/CSIA-Crime-Scene-Intelligence-Agent-.git
```

### 2. Navigate to the Project

```bash
cd CSIA-Crime-Scene-Intelligence-Agent-
```

### 3. Switch to the Timeline Module Branch

```bash
git checkout timeline-module
```

### 4. Navigate to the Backend

```bash
cd backend
```

### 5. Install Flask

```bash
python -m pip install flask
```

---

## ▶️ Running the Backend

From the `backend` directory:

```bash
python run.py
```

The Flask development server should start at:

```text
http://127.0.0.1:5000
```

Expected output:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

---

## 🧪 Running Tests

The project contains automated tests for:

* Timeline ordering
* Evidence-based next-step suggestions
* Witness-based next-step suggestions
* Complete timeline + suggestion flow

Run all tests from the `backend` directory:

```bash
python -m unittest discover -s app -p "test_*.py" -v
```

### Expected Result

```text
Ran 4 tests

OK
```

### Current Test Status

```text
4/4 tests passing
```

---

## 🔍 Example Workflow

```text
1. Investigator submits investigation events
                    ↓
2. Flask API receives the events
                    ↓
3. Timeline Builder sorts events chronologically
                    ↓
4. Rule Engine evaluates the investigation state
                    ↓
5. Relevant next-step suggestions are generated
                    ↓
6. Investigator reviews the suggestions
                    ↓
7. Investigator decides the actual next action
```

---

## 👮 Human-in-the-Loop Design

CSIA is designed to **support investigators rather than replace them**.

The system provides:

* Organized investigation information
* Chronological timelines
* Rule-based recommendations
* Structured outputs

The system does not independently decide the final investigative action.

Final decisions remain with the authorized investigator.

---

## 🔐 Safety & Design Principles

The project follows these principles:

* Human oversight
* Structured investigation workflows
* Explainable rule-based suggestions
* No automatic investigative decisions
* Modular backend architecture
* Testable components

---

## 📌 Current Development Status

| Component                | Status                 |
| ------------------------ | ---------------------- |
| Flask backend            | ✅ Complete             |
| Timeline Builder         | ✅ Complete             |
| Next-Step Rule Engine    | ✅ Complete             |
| Timeline Suggestions API | ✅ Complete             |
| Automated Tests          | ✅ 4/4 Passing          |
| GitHub Branch            | ✅ `timeline-module`    |
| Frontend                 | 🚧 Not implemented yet |
| Evidence Intake          | 🚧 Future module       |
| Visual Evidence Analysis | 🚧 Future module       |
| Text Analysis            | 🚧 Future module       |
| AI Intelligence Layer    | 🚧 Future module       |

---

## 🌱 Future Development

### Evidence Management

* Evidence metadata management
* Evidence categorization
* Case-based evidence organization
* Digital and physical evidence tracking

### Visual Intelligence

* Crime-scene image analysis
* Object detection
* Evidence identification
* Image-based scene understanding

### Text Intelligence

* Witness statement analysis
* Police report analysis
* Entity extraction
* Important fact extraction

### Investigation Intelligence

* Evidence correlation
* Event relationship detection
* Advanced investigation timelines
* Risk and priority indicators

### User Interface

A web-based dashboard can provide:

* Case overview
* Evidence panel
* Investigation timeline
* Next-step recommendations
* Investigation status
* Human approval controls

---

## 🤝 Contribution

The project is developed collaboratively.

When adding a new module:

1. Create a separate Git branch.
2. Implement the feature.
3. Add automated tests.
4. Run all existing tests.
5. Commit the changes.
6. Push the branch.
7. Review and merge after validation.

Example:

```bash
git checkout -b feature-name
```

---

## 📄 License

This project is licensed under the terms specified in the `LICENSE` file.

---

## 👥 Project

**CSIA – Crime Scene Intelligence Agent**
## 👥 Team Members & Responsibilities

| Sr. No. | Team Member | Registration No. | Area of Work / Responsibility |
|---:|---|---|---|
| 1 | **SANSKRUTI PRASHANT CHANEKAR** | **25BAI10603** | Timeline & Investigation Intelligence |
| 2 | **SAUMYA SINHA** | **25BAI11388** | Frontend (React + Tailwind) |
| 3 | **ANWESHA DHOTE** | **25BAI10996** | Image Analysis (YOLOv8) + OCR (EasyOCR) |
| 4 | **ANMOL PANJWANI** | **25BAI10354** |NLP Engine + Relationship Graph |
| 5 | **TANYA KAKKAR** | **25BAI11581** | Evidence Upload + Report Generator |
| 6 | **YOJIT WAGH** | **25BAI10232** |  Case Management + Search |

An AI-powered platform for structured crime-scene intelligence and investigation support.
