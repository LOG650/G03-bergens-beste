import pandas as pd

def analyze_peaks():
    log_path = "/Users/sandrachristensen/.gemini/tmp/log650/tool-outputs/session-2a6c74b6-548a-4ed7-8184-a9986f0f5cb4/run_shell_command_1776847028624_0.txt"
    
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
    analyze_peaks()
