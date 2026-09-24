import time
import os
import csv
from src.inference.pipeline import analyze
from src.config import Config

def watch_directory():
    config = Config.load()
    incoming = config.incoming_dir
    log_path = os.path.join(config.predictions, "realtime_log.csv")
    
    print("Starting MineIQ Real-Time Pipeline...")
    print(f"Watching {incoming} for new images...")
    
    processed = set()
    while True:
        try:
            files = [f for f in os.listdir(incoming) if f.endswith(('.png', '.jpg', '.h5'))]
            for f in files:
                if f not in processed:
                    full_path = os.path.join(incoming, f)
                    res = analyze(full_path)
                    
                    # Print branded formatting
                    print(f"\n--- New Sample: {f} ---")
                    print(f"Confidence: {res['confidence']}")
                    print(f"Latency: {res['latency_ms']}ms")
                    for dec in res['decisions']:
                        print(f"[{dec['priority']}] {dec['message']}")
                        
                    # Log to CSV
                    # TODO(person-3): Enhance logging with more metrics
                    with open(log_path, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([time.time(), f, res['confidence'], res['latency_ms']])
                        
                    processed.add(f)
                    
            time.sleep(config.poll_interval_seconds)
        except KeyboardInterrupt:
            print("Stopping...")
            break
