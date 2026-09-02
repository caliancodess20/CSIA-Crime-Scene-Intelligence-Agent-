from pathlib import Path
import uuid

UPLOAD_DIR = Path("uploads")


def save_evidence(case_id: str, file_name: str, file_content: bytes):
    case_folder = UPLOAD_DIR / case_id
    case_folder.mkdir(parents=True, exist_ok=True)

    evidence_id = "EVD-" + uuid.uuid4().hex[:8]

    file_path = case_folder / f"{evidence_id}_{file_name}"

    with open(file_path, "wb") as file:
        file.write(file_content)

    return evidence_id, str(file_path)