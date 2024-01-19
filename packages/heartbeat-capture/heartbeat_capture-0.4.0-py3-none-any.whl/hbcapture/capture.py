import os
import uuid
import re
import pandas as pd
from .file import HeartbeatCaptureFileInfo, HeartbeatCaptureFile


class HeartbeatCapture:

    FILE_PATTERN = r"(\d{8}_\d{6})-(\d{8}_\d{6})_([A-Z]{2}\d{4})_([0-9a-fA-F]{8})"

    def __init__(self, root_dir: str, capture_id: uuid.UUID, scan_on_init: bool = False):
        self.root_dir = root_dir
        self.capture_id = capture_id
        self.files = []
        if scan_on_init:
            self.scan()


    def scan(self):
        """
        Scans the root directory for capture files matching the specified capture ID.
        """
        print(f"Scanning {self.root_dir} for capture {self.capture_id}")
        
        ls = os.listdir(self.root_dir)

        for file in ls:
            match = re.match(HeartbeatCapture.FILE_PATTERN, file)
            if match is None:
                continue

            (start, end, node_id, capture_id) = match.groups()

            if capture_id != self.capture_id.hex[:8]:
                continue

            self.files.append(HeartbeatCaptureFile.load(os.path.join(self.root_dir, file)))

        self.sample_rate = self.files[0].info.sample_rate
        self.files.sort(key=lambda x: x.info.start)

        self.start = self.files[0].info.start
        self.end = self.files[-1].info.end

        pass

    def df_all(self) -> pd.DataFrame:
        items = []

        for file in self.files:
            file.load_all_lines()
            for line in file.lines:
                items.append((line.time, line.data))

        df = pd.DataFrame(items, columns=["timestamp", "data"])

        return df
    
    def from_capture_file(file_path: str):
        pass