import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def analyze_peaks(log_path):
    log_path = Path(log_path)
    if not log_path.exists():
        raise FileNotFoundError(f"Fant ikke loggfil: {log_path}")

    criticals = []
    with open(log_path, 'r') as f:
        for line in f:
            if "KRITISK" in line:
                try:
                    time = float(line.split(':')[0])
                    criticals.append(time)
                except:
                    continue
    
    df = pd.DataFrame(criticals, columns=['time'])
    df['hour'] = (df['time'] / 60).astype(int)
    
    # Grupper per time og tell antall fly som ikke fikk plass
    peak_hours = df.groupby('hour').size().reset_index(name='failed_flights')
    
    print("ANTALL FLY UTEN PLASS PER TIME (0 = Midnatt):")
    print(peak_hours.to_string(index=False))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyser tidspunkt med KRITISK-hendelser fra en simuleringslogg.")
    parser.add_argument("log_path", help="Sti til loggfilen som skal analyseres")
    args = parser.parse_args()
    analyze_peaks(args.log_path)
