from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    evidence_id: str
    case_id: str
    file_name: str
    file_type: str
    file_path: str