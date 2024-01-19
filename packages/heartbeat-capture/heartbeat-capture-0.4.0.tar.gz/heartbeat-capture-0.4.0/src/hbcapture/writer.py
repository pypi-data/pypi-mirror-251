import re
import uuid
import os
from datetime import datetime
from .file import HeartbeatCaptureLine, HeartbeatCaptureFileInfo


class HeartbeatCaptureWriter:

    def __init__(self, root_dir: str, sample_rate: float, capture_id: uuid.UUID, node_id: str):
        self.created = datetime.now()
        self.capture_id = uuid.uuid4() if capture_id is None else capture_id
        self.node_id = node_id
        self.sample_rate = sample_rate
        self.root_dir = root_dir
        self.open = False
        self.files = [HeartbeatCaptureWriterFile(self.capture_id, 0)]

    def __del__(self):
        if self.open:
            self.write_header()
            self.open = False

    def __enter__(self):
        print(f"Using {self.root_dir} as root directory")

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        else:
            print("Directory %s already exists" % self.root_dir)

        self.current_line = 0
        self.current_file = 0
        self.open = True

        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.open:
            self.write_header()
            self.open = False
    

    def init(self):
        print(f"Using {self.root_dir} as root directory")

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        else:
            print("Directory %s already exists" % self.root_dir)

        self.current_line = 0
        self.current_file = 0
        self.open = True


    def write_line(self, line: HeartbeatCaptureLine):
        """
        Writes a line of HeartbeatCaptureLine data to the writer file.

        Parameters:
            line (HeartbeatCaptureLine): The line of HeartbeatCaptureLine data to write.
        """
        writer_file = self.files[-1]

        if writer_file.lines == 0:
            writer_file.start_time = line.time
            writer_file.end_time = line.time

        with open(os.path.join(self.root_dir, writer_file.get_data_filename()), 'a') as f:
            writer_file.end_time = line.time
            f.write("%s\n" % line.generate_line())

        writer_file.lines += 1
    
    def generate_info(self):
        writer_file = self.files[-1]
        info = HeartbeatCaptureFileInfo(start=writer_file.start_time,
                                         end=writer_file.end_time,
                                         capture_id=self.capture_id,
                                         node_id=self.node_id,
                                         sample_rate=self.sample_rate)
        
        return info

    def write_header(self):
        writer_file = self.files[-1]

        with open(os.path.join(self.root_dir, writer_file.get_header_filename()), 'a') as f:
            f.write("%s\n" % self.generate_info().generate_header())

    def next_file(self):
        self.write_header()
        self.current_line = 0
        self.current_file += 1
        self.files.append(HeartbeatCaptureWriterFile(self.capture_id, self.current_file))
        pass
    

class HeartbeatCaptureWriterFile:

    def __init__(self, capture_id: uuid, index: int):
        self.capture_id = capture_id
        self.index = index
        self.lines = 0
        self.start_time = None
        self.end_time = None

    def __repr__(self):
        return "HeartbeatCaptureWriterFile(%s, %s, %s)" % (self.capture_id, self.index, self.lines) 

    def get_header_filename(self):
        return f"hbcapture_{self.capture_id}_HEADER_{self.index}"
    
    def get_data_filename(self):
        return f"hbcapture_{self.capture_id}_DATA_{self.index}"
    

class HeartbeatCaptureWriterPackager:
    PATTERN_FILENAME = r"hbcapture_([0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})_(DATA|HEADER)_(\d+)"

    def __init__(self, root_dir: str, capture_id: uuid):
        self.root_dir = root_dir
        self.capture_id = capture_id

    def from_writer(writer: HeartbeatCaptureWriter):
        return HeartbeatCaptureWriterPackager(writer.root_dir, writer.capture_id)


    def package(self):
        ls = os.listdir(self.root_dir)
        ls.sort()

        for file in ls:
            if file.startswith(f"hbcapture_{self.capture_id}_DATA"):
                match = re.match(HeartbeatCaptureWriterPackager.PATTERN_FILENAME, file)
                (capture_id, type, index) = match.groups()

                data_path = os.path.join(self.root_dir, file)
                header_path = os.path.join(self.root_dir,
                                            f"hbcapture_{capture_id}_HEADER_{index}")
                header_exists = os.path.isfile(header_path)

                if not header_exists:
                    raise Exception(f"Header file hbcapture_{capture_id}_HEADER_{index} not found")
                
                with open(header_path, 'r') as f:
                    header = f.read()

                file_info = HeartbeatCaptureFileInfo.parse_metadata(header)

                with open(data_path, 'r') as f:
                    data = f.read()


                output_file = os.path.join(self.root_dir, file_info.filename())
                with open(output_file, 'w') as f:
                    f.write(header[:-1])
                    f.write(data[:-1])

    def clean_up(self):
        ls = os.listdir(self.root_dir)

        for file in ls:
            if file.startswith(f"hbcapture_{self.capture_id}_DATA"):
                os.remove(os.path.join(self.root_dir, file))
            elif file.startswith(f"hbcapture_{self.capture_id}_HEAD"):
                os.remove(os.path.join(self.root_dir, file))
