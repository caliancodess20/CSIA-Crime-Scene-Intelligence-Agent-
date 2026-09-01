
# 🔎 Crime Scene Intelligence Assistant (CSIA)

<p align="center">
  <b>🕵️ Organize Evidence · 🧠 Analyze Information · 📊 Support Investigation</b>
</p>

<p align="center">
  An AI-powered educational investigation-assistance platform combining
  <br>
  Computer Vision, OCR, NLP, Timeline Generation, Relationship Graphs and Reporting.
</p>

<p align="center">

![AI & ML](https://img.shields.io/badge/AI%20%26%20ML-Project-blue?style=for-the-badge)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-YOLOv8-orange?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20Sentence%20Transformers-green?style=for-the-badge)
![OCR](https://img.shields.io/badge/OCR-EasyOCR-purple?style=for-the-badge)

![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Tailwind-61DAFB?style=flat-square)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20MongoDB-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Educational%20Prototype-success?style=flat-square)

</p>

---

## 📚 Table of Contents

* [✨ About CSIA](#-about-csia)
* [🎯 Problem Statement](#-problem-statement)
* [🚀 Objectives](#-objectives)
* [🎬 Mock Robbery Scenario](#-mock-robbery-scenario)
* [🏗️ System Architecture](#️-system-architecture)
* [🧩 Core Modules](#-core-modules)
* [🔄 End-to-End Workflow](#-end-to-end-workflow)
* [🤖 AI Pipeline](#-ai-pipeline)
* [🕸️ Relationship Graph](#️-relationship-graph)
* [🕐 Investigation Timeline](#-investigation-timeline)
* [💡 Next-Step Suggestions](#-next-step-suggestions)
* [📊 Dashboard](#-dashboard)
* [📈 Scalability](#-scalability)
* [💡 Advantages](#-advantages)
* [⚠️ Limitations](#️-limitations)
* [🔐 Privacy & Ethics](#-privacy--ethics)
* [🚧 Challenges](#-challenges)
* [🔮 Future Scope](#-future-scope)
* [🛠️ Technology Stack](#️-technology-stack)
* [🚀 Getting Started](#-getting-started)
* [🧪 Testing](#-testing)
* [📁 Project Structure](#-project-structure)
* [👥 Team](#-team)
* [🎓 Academic Information](#-academic-information)
* [📌 Disclaimer](#-disclaimer)
* [🏁 Conclusion](#-conclusion)

---

# ✨ About CSIA

**Crime Scene Intelligence Assistant (CSIA)** is an educational platform designed to help investigators organize and understand crime-scene information.

Instead of keeping photographs, witness statements, CCTV frames and other evidence in separate locations, CSIA brings them together into a **single case workflow**.

> 🧠 **CSIA assists. Humans decide.**

The system provides:

* 📁 Case organization
* 🖼️ Evidence analysis
* 📝 Statement summarization
* 🕐 Timeline generation
* 🕸️ Relationship visualization
* 💡 Next-step suggestions
* 📄 Report generation

CSIA is designed as a **helper tool, not a replacement for investigators**. Human users remain responsible for decisions and verification of system outputs.

---

# 🎯 Problem Statement

Investigation information can be distributed across different files and sources:

```text
📷 Crime Scene Photo
        │
        └── Separate File

📝 Witness Statement
        │
        └── Separate File

📹 CCTV Frame
        │
        └── Separate File
```

When information is separated, it becomes harder to identify relationships and connections between different pieces of evidence.

## 💡 The CSIA Approach

```text
        📷 Image
           │
        📝 Statement
           │
        📹 CCTV
           │
           ▼
    🗂️ SINGLE CASE RECORD
           │
           ▼
      🧠 CSIA ANALYSIS
           │
           ▼
    📊 STRUCTURED OUTPUT
```

CSIA brings the information together into a unified case record to make investigation information easier to organize and review.

---

# 🚀 Objectives

CSIA focuses on six major objectives:

| 🎯  | Objective                         |
| --- | --------------------------------- |
| 🖥️ | **Unified Dashboard**             |
| 👁️ | **AI Evidence Analysis**          |
| 📝  | **Statement Summarization**       |
| 🕐  | **Automatic Timeline Generation** |
| 💡  | **Next-Step Suggestions**         |
| 📄  | **Report Generation**             |

These objectives transform raw uploads into structured and reviewable investigation information.

---

# 🎬 Mock Robbery Scenario

The project uses a **mock robbery case** to demonstrate the complete workflow.

## 📥 Input

```text
┌─────────────────────┐
│  📷 Shop Image      │
├─────────────────────┤
│  📝 Witness Report  │
├─────────────────────┤
│  📹 CCTV Frame      │
└─────────────────────┘
```

## ⚙️ Processing

```text
             📥 UPLOAD
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     IMAGE   STATEMENT   CCTV
       │        │        │
       ▼        ▼        ▼
    YOLOv8     NLP     EasyOCR
       │        │        │
       └────────┼────────┘
                ▼
       🗂️ STRUCTURED INFORMATION
                │
       ┌────────┴────────┐
       ▼                 ▼
   🕐 TIMELINE       🕸️ RELATIONSHIP
   GENERATOR             GRAPH
       │                 │
       └────────┬────────┘
                ▼
       💡 NEXT-STEP SUGGESTION
                │
                ▼
          📄 CASE REPORT
```

For the demonstration scenario, the system can detect objects such as a **knife** and **backpack**, extract names and locations from a witness statement, generate a timeline, and suggest an action such as checking nearby CCTV.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │   🖥️ CSIA DASHBOARD  │
                         └───────────┬──────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │   📁 CASE MANAGEMENT │
                         └───────────┬──────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │   📤 EVIDENCE UPLOAD │
                         └───────────┬──────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                      ▼
       ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
       │   👁️ YOLOv8 │        │  🔤 EasyOCR │        │   🧠 NLP    │
       │ Object      │        │ Text        │        │ Statement   │
       │ Detection   │        │ Extraction  │        │ Processing  │
       └──────┬──────┘        └──────┬──────┘        └──────┬──────┘
              │                      │                      │
              └──────────────────────┼──────────────────────┘
                                     ▼
                         ┌──────────────────────┐
                         │ 🗂️ STRUCTURED DATA  │
                         └───────────┬──────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
          🕐 Timeline          🕸️ Relationship      📄 Reports
          Generator               Graph              Generator
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     ▼
                              🔍 SEARCH DASHBOARD

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
 origin/timeline-module
```

---

# 🧩 Core Modules

| #  | Module                     | Purpose                                               |
| -- | -------------------------- | ----------------------------------------------------- |
| 01 | 📁 **Case Management**     | Manage investigation cases and associated information |
| 02 | 📤 **Evidence Upload**     | Upload and associate evidence with cases              |
| 03 | 👁️ **Image Analysis**     | Detect objects using YOLOv8                           |
| 04 | 🔤 **OCR**                 | Extract text using EasyOCR                            |
| 05 | 🧠 **NLP Engine**          | Process and summarize witness statements              |
| 06 | 🕐 **Timeline Generator**  | Organize investigation events chronologically         |
| 07 | 🕸️ **Relationship Graph** | Connect entities and relationships                    |
| 08 | 📄 **Report Generator**    | Generate structured investigation reports             |
| 09 | 🔍 **Search Dashboard**    | Search and filter investigation information           |

---

# 🔄 End-to-End Workflow

```text
                         ┌─────────────┐
                         │    START    │
                         └──────┬──────┘
                                ▼
                      ┌──────────────────┐
                      │ Create / Select  │
                      │      Case        │
                      └────────┬─────────┘
                               ▼
                      ┌──────────────────┐
                      │ Upload Evidence  │
                      └────────┬─────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          🖼️ Image         📝 Statement       📹 CCTV
              │                │                │
              ▼                ▼                ▼
           YOLOv8             NLP            EasyOCR
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    🗂️ Structured Information
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              🕐 Timeline           🕸️ Relationship
                 View                   Graph
                    │                     │
                    └──────────┬──────────┘
                               ▼
                     💡 Next-Step Prompt
                               │
                               ▼
                        📄 Case Report
                               │
                               ▼
                        🖥️ Dashboard
                               │
                               ▼
                              END
=======
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
>>>>>>> origin/timeline-module
```

---

<<<<<<< HEAD
# 🤖 AI Pipeline

## 👁️ Computer Vision — YOLOv8

YOLOv8 is used for object detection within crime-scene images.

```text
📷 Crime Scene Image
        ↓
      YOLOv8
        ↓
┌─────────────────────┐
│ Detected Objects    │
├─────────────────────┤
│ Knife               │
│ Backpack            │
│ Other Objects       │
└─────────────────────┘
```

## 🔤 OCR — EasyOCR

EasyOCR extracts visible text from images and CCTV frames.

```text
📹 CCTV / Image
       ↓
    EasyOCR
       ↓
📝 Extracted Text
```

## 🧠 Natural Language Processing

The NLP pipeline processes witness statements and extracts meaningful information.

Technologies include:

* **spaCy**
* **Sentence Transformers**

```text
📝 Witness Statement
        ↓
       NLP
        ↓
┌────────────────────┐
│ Summary            │
│ Names              │
│ Locations          │
│ Entities           │
└────────────────────┘
=======
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

# 🕸️ Relationship Graph

The relationship graph represents connections between entities extracted from investigation information.

Example:

```text
             ┌─────────────┐
             │   Witness   │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │    Shop     │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │   Suspect   │
             └─────────────┘
```

This makes relationships easier to visualize and understand.

---

# 🕐 Investigation Timeline

Investigation events can be arranged chronologically using their timestamps.

Example:

```text
10:00 ─── 🟢 Case Created
             │
14:00 ─── 🔵 Witness Statement
             │
15:30 ─── 🟠 Evidence Collected
             │
             ▼
       💡 Next-Step Prompt
```

The timeline converts timestamped investigation events into a structured sequence.

---

# 💡 Next-Step Suggestions

CSIA provides **rule-based suggestions** rather than autonomous investigative decisions.

Example:

```text
Evidence Available
       ↓
Rule Evaluation
       ↓
💡 "Check nearby CCTV"
```

The purpose is to provide a useful prompt for human review.

---

# 📊 Dashboard

The unified dashboard acts as the central interface for the system.

### 🖥️ Main Views

```text
┌─────────────────────────────────────────────┐
│                 CSIA DASHBOARD              │
├──────────────┬──────────────────────────────┤
│ 📁 Cases     │ Active Case                  │
│ 🔍 Search    │                              │
│ 📤 Evidence  │ 🖼️ Evidence Analysis        │
│ 🕐 Timeline  │ 📝 Statement Summary         │
│ 🕸️ Graph     │ 💡 Suggestions              │
│ 📄 Reports   │                              │
└──────────────┴──────────────────────────────┘
=======
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

# 📈 Scalability

The modular architecture allows different components to potentially scale independently.

```text
             CSIA
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
   Vision    NLP    Reporting
     │        │        │
  Server A Server B Server C
```

For example, the image-analysis service could receive additional computing resources without requiring changes to the NLP service.

> ⚠️ Independent scaling is a future architectural possibility and has not been validated under real production load.

---

# 💡 Advantages

|     | Benefit                                          |
| --- | ------------------------------------------------ |
| 📁  | Better organization of investigation information |
| ⚡   | Reduced manual information handling              |
| 👁️ | Demonstrates Computer Vision                     |
| 🧠  | Demonstrates NLP                                 |
| 🕸️ | Visualizes relationships                         |
| 🕐  | Automatically structures timelines               |
| 📄  | Generates structured reports                     |
| 📈  | Modular and potentially scalable architecture    |

---

# ⚠️ Limitations

CSIA is an educational prototype and has important limitations.

### 🧠 AI Accuracy

AI models can produce incorrect results.

### 📚 Training Data

Reliable detection requires suitable labeled training data.

### 🔐 Privacy

Crime-scene and case information can be highly sensitive.

### 💻 Computational Requirements

YOLOv8 and EasyOCR can be computationally heavy, especially without GPU support.

### 🎓 Educational Scope

The system is intended for education, demonstrations and training rather than live casework.

---

# 🔐 Privacy & Ethics

CSIA follows an important principle:

> ## 🧠 AI assists. Humans remain responsible.

Important considerations include:

* 🔐 Secure storage
* 🛡️ Access control
* ⚖️ Bias evaluation
* 🔍 Explainability
* 📜 Chain of custody
* 👤 Human verification

A production forensic system would require significantly stronger privacy, security and evidence-management controls.

---

# 🚧 Challenges

Major challenges include:

```text
        ┌───────────────────────┐
        │ Legal Training Data   │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │     AI Model Bias     │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Explainability      │
        └───────────┬───────────┘
                    │
             ┌──────┴──────┐
             ▼             ▼
       🔐 Security    📜 Chain of
                         Custody
```

Other practical challenges include:

* Blurry photographs
* Contradictory witness statements
* Missing timestamps
* Limited training datasets
* Computational requirements
* Secure evidence storage

---

# 🔮 Future Scope

| 🚀 Future Feature             | Possible Extension                 |
| ----------------------------- | ---------------------------------- |
| 🧊 **3D Reconstruction**      | 3D crime-scene visualization       |
| 🌐 **Multilingual AI**        | Support multiple languages         |
| 🥽 **AR / VR**                | Immersive investigation training   |
| 🚁 **Drone Analysis**         | Analyze aerial crime-scene footage |
| 📹 **CCTV Analytics**         | Process surveillance footage       |
| 🎙️ **Voice Assistant**       | Voice-based interaction            |
| 📍 **Crime Hotspot Analysis** | Analyze potential crime patterns   |

These are future possibilities and are not claimed as current MVP features.

---

# 🛠️ Technology Stack

## 🎨 Frontend

```text
React
Tailwind CSS
```

## ⚙️ Backend

```text
FastAPI
```

## 🤖 AI / ML

```text
YOLOv8
EasyOCR
spaCy
Sentence Transformers
```

## 🗄️ Database

```text
PostgreSQL / MongoDB
```

### Stack Overview

```text
┌─────────────────────────────────────┐
│             🖥️ FRONTEND             │
│          React + Tailwind            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│              ⚙️ BACKEND             │
│               FastAPI               │
└──────────────────┬──────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     YOLOv8     EasyOCR      NLP
                            │
                    spaCy + ST
        │          │          │
        └──────────┼──────────┘
                   ▼
          🗄️ PostgreSQL /
             MongoDB
=======
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
>>>>>>> origin/timeline-module
```

---

<<<<<<< HEAD
# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd CSIA-Crime-Scene-Intelligence-Agent
```

## 2️⃣ Backend Setup

Navigate to the backend:
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


Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend using the project's configured entry point.

## 3️⃣ Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

> ⚠️ Update the commands above if the final repository uses a different folder structure or entry point.

---

# 🧪 Testing

Testing should include both clean and imperfect investigation cases.

## ✅ Clean Case

```text
Clear image
Consistent statement
Complete timestamps
```

## ⚠️ Messy Case

```text
Blurry photograph
Contradictory statement
Missing timestamp
```

Testing imperfect cases helps demonstrate how the system behaves outside the ideal demonstration scenario.

---

# 📁 Project Structure

```text
CSIA-Crime-Scene-Intelligence-Agent/
│
├── 📁 frontend/
│   ├── src/
│   ├── components/
│   └── ...
│
├── 📁 backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   │   ├── image_analysis/
│   │   ├── ocr/
│   │   ├── nlp/
│   │   ├── timeline/
│   │   └── reports/
│   └── ...
│
├── 📄 README.md
└── 📄 ...
```

---

# 👥 Team

| #  | Name                            | Registration No. | GitHub                                                               |
| -- | ------------------------------- | ---------------- | -------------------------------------------------------------------- |
| 01 | **SANSKRUTI PRASHANT CHANEKAR** | **25BAI10603**   | [@caliancodess20](https://github.com/caliancodess20)                 |
| 02 | **YOJIT WAGH**                  | **25BAI10232**   | —                                                                    |
| 03 | **ANWESHA DHOTE**               | **25BAI10996**   | [@anweshabuilds25](https://github.com/anweshabuilds25)               |
| 04 | **SAUMYA SINHA**                | **25BAI11388**   | [@saumya25bai11388-sys](https://github.com/saumya25bai11388-sys)     |
| 05 | **ANMOL PANJWANI**              | **25BAI10354**   | [@Anmol25bai10354](https://github.com/Anmol25bai10354)               |
| 06 | **TANYA KAKKAR**                | **25BAI11581**   | [@tanya25bai11581-source](https://github.com/tanya25bai11581-source) |

---

# 🎓 Academic Information

|                    | Details                            |
| ------------------ | ---------------------------------- |
| 🏫 **University**  | VIT Bhopal University              |
| 📚 **Course**      | Project Exhibition 1               |
| 🔢 **Course Code** | DSN 2098                           |
| 🧠 **Branch**      | AI & ML                            |
| 🔎 **Project**     | Crime Scene Intelligence Assistant |

---

# 📌 Disclaimer

> ⚠️ **CSIA is an educational investigation-assistance prototype.**

The system is intended for:

* 🎓 University demonstrations
* 🔬 Forensic education
* 👮 Police training
* 💻 Cyber-forensics laboratories
* 🧪 Mock investigations

It is **not intended for live criminal investigations or real-world casework**.

AI-generated detections, summaries, relationships and suggestions may be incorrect and must not be treated as definitive evidence or autonomous investigative decisions.

---

# 🏁 Conclusion

## 🔎 From Raw Evidence → Structured Intelligence

CSIA combines multiple AI and software technologies into one educational investigation platform.

```text
       📷 EVIDENCE
            │
            ▼
     🤖 AI ANALYSIS
            │
            ▼
   🗂️ STRUCTURED DATA
            │
      ┌─────┴─────┐
      ▼           ▼
   🕐 Timeline   🕸️ Graph
      │           │
      └─────┬─────┘
            ▼
      💡 Suggestions
            │
            ▼
        📄 Report
            │
            ▼
      👤 HUMAN REVIEW
```

The project demonstrates how **Computer Vision, OCR, NLP, data management and visualization** can work together to organize investigation information within a single educational platform.

---

<h2 align="center">🔎 CSIA</h2>

<p align="center">
  <b>Organize Evidence · Connect Information · Support Investigation</b>
</p>

<p align="center">
  Made with ❤️ by the AI & ML Team<br>
  <b>VIT Bhopal University</b>
</p>
=======
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

