import click
import datetime as dt
import numpy as np
import random
import uuid
from . import HeartbeatCaptureFileInfo
from pytz import timezone

@click.group()
def cli():
    pass

@click.command()
@click.option("--location", default="Cleveland, OH")
@click.option("--node", default="ET0001")
@click.option("--capture_id", default=uuid.uuid4())
@click.option("--file", default=None)
@click.argument('start')
@click.argument('end')
def generate(location, node, capture_id, file, start, end):
    dt_start = dt.datetime.fromtimestamp(float(start), tz=timezone('UTC'))
    dt_end = dt.datetime.fromtimestamp(float(end), tz=timezone('UTC'))

    capture_id = uuid.UUID(capture_id)

    print("Generating Heartbeat capture file from %s to %s" % (dt_start, dt_end))
    print("Will generate %d lines" % (dt_end - dt_start).total_seconds())

    header = HeartbeatCaptureFileInfo(start=dt_start, 
                                  end=dt_end, 
                                  capture_id=capture_id,
                                  node_id=node,
                                  sample_rate=20000)

    current_time = dt_start
    sample_rate = header.sample_rate
    pulse_duration = 20
    after_length = 10

    print("Samples per line = %d" % (sample_rate * pulse_duration / 1000))

    filename = file if file else header.filename()

    with open(filename, 'w') as f:
        f.write(header.generate_header())

        counter = 0

        while current_time < dt_end:
            delay = (random.random() * 1)+4
            
            t_data = np.arange(0, (pulse_duration)/1000, 1/sample_rate)
            intensity = np.power(np.abs(np.sin(counter/40)), 1) 
            intensity = intensity + np.random.normal(0, 0.3, len(t_data))
            y_data = np.sin(2*np.pi*1000*t_data) * intensity
            data = np.concatenate([np.random.normal(0, 0.2, int(delay * sample_rate / 1000)), y_data])
            data = np.concatenate([data, np.random.normal(0, 0.2, int((after_length - delay) * sample_rate / 1000))])
            data = np.round(data * 512 + 512).astype(int)

            f.write("%f," % (current_time.timestamp() + (random.random()/2.0 - 1.0)))

            for index in range(len(data) - 1):
                f.write("%d," % data[index])
                
            f.write("%d\n" % data[-1])

            current_time += dt.timedelta(seconds = 1)
            counter += 1

@click.command()
@click.argument('filename')
def info(filename):
    with open(filename, 'r') as f:
        header_text = ""

        while True:
            line = f.readline()
            if not line:
                break

            if line.startswith("#"):
                header_text += line
                continue
        
            break

        line_count = 0

        while True:
            line = f.readline()
            if not line:
                break

            line_count += 1
    
    info = HeartbeatCaptureFileInfo.parse_metadata(header_text)
    print(f"Info for file \"{filename}\"")
    duration = info.end - info.start
    utc = timezone("UTC")
    print("{start} -> {end}, total duration is {duration}"
          .format(start=info.start.astimezone(utc).strftime('%H:%M:%S %B %d, %Y UTC'),
                    end=info.end.astimezone(utc).strftime('%H:%M:%S %B %d, %Y UTC'),
                    duration=duration))
    
    print(f"Found {line_count} lines")

    

cli.add_command(generate)
cli.add_command(info)

if __name__ == '__main__':
    cli()