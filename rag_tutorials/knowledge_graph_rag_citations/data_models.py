from dataclasses import dataclass
from typing import List

@dataclass
class Entity:
    id: str
    name: str
    entity_type: str
    description: str
    source_doc: str
    source_chunk: str

@dataclass
class Relationship:
    source: str
    target: str
    relation_type: str
    description: str
    source_doc: str

@dataclass
class Citation:
    claim: str
    source_document: str
    source_text: str
    confidence: float
    reasoning_path: List[str]

@dataclass
class AnswerWithCitations:
    answer: str
    citations: List[Citation]
    reasoning_trace: List[str]
