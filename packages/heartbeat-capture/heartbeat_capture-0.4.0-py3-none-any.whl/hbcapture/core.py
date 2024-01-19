import uuid

from .writer import HeartbeatCaptureWriter
from .capture import HeartbeatCapture

def writer(root_dir: str, capture_id: uuid.UUID, node_id: str, sample_rate: float) -> HeartbeatCaptureWriter:
    return HeartbeatCaptureWriter(root_dir, capture_id, node_id, sample_rate)

def capture(root_dir: str, capture_id: uuid.UUID) -> HeartbeatCapture:
    return HeartbeatCapture(root_dir, capture_id)