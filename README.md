# CSIA — Crime Scene Intelligence Assistant

An AI-assisted case organization platform for forensic education, training, and mock investigations.

> **CSIA assists. Humans decide.** Every AI output — object detections, statement summaries, next-step suggestions — is a prompt for human review, never an autonomous decision.

---

## Table of Contents

- [About](#about)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Running](#setup--running)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Team & Responsibilities](#team--responsibilities)
- [Limitations & Disclaimer](#limitations--disclaimer)
- [Academic Information](#academic-information)

---

## About

CSIA brings scattered crime-scene evidence — photos, witness statements, CCTV frames — into a single case record, then applies AI to structure it:

- Unified case dashboard
- AI-assisted evidence analysis (object detection + OCR)
- Witness statement summarization
- Automatic, chronological timelines
- Rule-based next-step suggestions
- Exportable case reports
- Case & evidence search

It is built for **university demonstrations, forensic education, police training, and mock investigations** — not for live criminal casework.

## Problem Statement

A crime-scene photo, a witness statement, and a CCTV frame from the same case typically end up in separate files or folders, making it easy to miss a connection between them. CSIA pulls every evidence type into one case record and applies AI to surface structure and connections a manual review might miss.

**Trade-off worth stating plainly:** centralizing everything also means a single breach or bug could expose an entire case.

## Objectives

| Objective | What it does |
|---|---|
| Unified Dashboard | Single view of every active case |
| AI Evidence Analysis | Vision models scan uploaded images |
| Statement Summarization | NLP condenses witness accounts |
| Automatic Timelines | Events sequenced from evidence |
| Next-Step Suggestions | Rule-based — e.g. *"check nearby CCTV"* |
| Exportable Reports | Structured output for review |

## System Architecture

All modules run as **one FastAPI application, one process, one port** —
mounted via `include_router()` in `backend/app/main.py`, sharing a single
Postgres database through `case_management`'s schema. No module runs as a
separate standalone service.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI (Python) |
| Computer Vision | YOLOv8 (Ultralytics) |
| OCR | EasyOCR |
| NLP | spaCy + Sentence Transformers |
| Database | PostgreSQL |

### Feasibility notes

- **Budget:** fully open-source stack — student-friendly
- **Performance:** YOLOv8 / EasyOCR run slowly without a GPU (CUDA recommended)
- **Hosting:** a live/hosted version needs a real server, not a laptop
- **Training data:** needs labeled examples the team may not legally have access to for real forensic imagery

## Project Structure

```text
CSIA-Crime-Scene-Intelligence-Agent/
│
├── backend/
│   │
│   ├── app/
│   │   ├── case_management/
│   │   │   ├── API_REFERENCE.md
│   │   │   ├── __init__.py
│   │   │   ├── crud.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   ├── requirements.txt
│   │   │   ├── routes.py
│   │   │   ├── sample_case.json
│   │   │   └── schemas.py
│   │   │
│   │   ├── image_analysis/
│   │   │   ├── ocr_reader.py
│   │   │   ├── routes.py
│   │   │   └── yolo_detector.py
│   │   │
│   │   ├── nlp_engine/
│   │   │   ├── __init__.py
│   │   │   ├── entity_extraction.py
│   │   │   └── routes.py
│   │   │
│   │   ├── shared/
│   │   │   ├── auth.py
│   │   │   ├── exceptions.py
│   │   │   └── utils.py
│   │   │
│   │   ├── timeline_suggestions/
│   │   │   ├── next_step_rules.py
│   │   │   ├── routes.py
│   │   │   ├── test_full_flow.py
│   │   │   ├── test_next_steps.py
│   │   │   ├── test_timeline.py
│   │   │   └── timeline_builder.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── API_REFERENCE.md
│   ├── requirements.txt
│   ├── run.py
│   └── sample_case.json
│
├── frontend/
│   ├── src/
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── README.md
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── ml_models/
│   └── yolo/
│
├── evidence_analysis.py
├── evidence_pipeline.py
├── format_spec.py
├── main.py
├── report_builder.py
├── routes.py
├── storage.py
│
├── .gitignore
├── LICENSE
└── README.md
```

## Setup And Running
### Prerequisites
- Python 3.10+
- Docker (for Postgres)

### 1. Start Postgres
```bash
docker run --name csia-db \
  -e POSTGRES_USER=csia_user \
  -e POSTGRES_PASSWORD=csia_password \
  -e POSTGRES_DB=csia_db \
  -p 5432:5432 \
  -d postgres:16
```

### 2. Install dependencies (from the repo root)

```bash
pip install -r backend/app/case_management/requirements.txt
pip install ultralytics easyocr opencv-python-headless torch
```

### 3. Point the app at the database

```bash
export DATABASE_URL="postgresql://csia_user:csia_password@localhost:5432/csia_db"
```

### 4. Run it

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Database tables are created automatically on startup. First run downloads
YOLOv8 and EasyOCR model weights — needs outbound internet once.

### 5. Verify it's alive

```bash
curl http://127.0.0.1:8000/
# {"message":"CSIA Backend is running!"}
```

## API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/cases` | Create a case |
| `GET` | `/cases` | List cases (paginated) |
| `GET` | `/cases/{case_id}` | Get one case with its evidence |
| `PUT` | `/cases/{case_id}` | Update a case |
| `DELETE` | `/cases/{case_id}` | Delete a case |
| `POST` | `/cases/{case_id}/evidence` | Attach evidence directly |
| `POST` | `/cases/{case_id}/evidence/upload` | Upload a file as evidence |
| `POST` | `/cases/{case_id}/evidence/image` | Upload + run YOLOv8/EasyOCR, store result |
| `GET` | `/cases/{case_id}/timeline` | Chronological timeline + next-step suggestions |
| `GET` | `/cases/{case_id}/report` | Generate a PDF case report |
| `GET` | `/evidence/{evidence_id}` | Get one evidence item |
| `GET` | `/search/cases` | Search/filter cases |
| `GET` | `/search/evidence` | Search/filter evidence |

**Evidence fields:** `id`, `case_id`, `evidence_type`, `description`, `source`, `file_url`, `collected_by`, `collected_at`, `extra_metadata`, `chain_of_custody`.
**`evidence_type` values:** `image`, `video`, `document`, `witness_statement`, `cctv_frame`, `physical`, `other`.

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

`test_timeline_suggestions.py` covers both a clean case (based on a real
sample case) and a messy case: a low-detail photo, two contradictory
witness statements, and one piece of evidence with no timestamp.

## Team & Responsibilities

| Member | Reg. No. | Track |
|---|---|---|
| **Sanskruti Prashant Chanekar** (Team Lead) | 25BAI10603 | Timeline Generator + Next-Step Suggestions |
| Yojit Wagh | 25BAI10232 | Case Management + Search Dashboard |
| Anwesha Dhote | 25BAI10996 | Image Analysis (YOLOv8) + OCR (EasyOCR) |
| Anmol Panjwani | 25BAI10354 | NLP Engine + Relationship Graph |
| Tanya Kakkar | 25BAI11581 | Evidence Upload + Report Generator |
| Saumya Sinha | 25BAI11388 | Frontend (React + Tailwind) |

## Limitations & Disclaimer

CSIA is an educational prototype intended for university demonstrations,
forensic education, police training, and mock investigations — **not for
live criminal investigations or real evidentiary casework.**

- AI detections, summaries, and suggestions may be incorrect and must not
  be treated as definitive evidence.
- Timeline ordering reflects when evidence was *collected*, not
  necessarily when the underlying incident occurred.
- Requires labeled training data, secure storage, and chain-of-custody
  controls beyond this prototype's scope for any real-world use.

## Academic Information

| | |
|---|---|
| University | VIT Bhopal University |
| Course | Project Exhibition 1 |
| Course Code | DSN 2098 |
| Branch | AI & ML | 



