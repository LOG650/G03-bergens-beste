import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load data
df = pd.read_csv('G03-bergens-beste/004 data/Flyprogram 15jun - 29jun CSV.csv', sep=';')
df['Timestamp'] = pd.to_datetime(df['Flight Date'] + ' ' + df['Scheduled Time'])
df = df.sort_values('Timestamp')

results = []
uncertain_cases = []

# Process day by day
for date in df['Flight Date'].unique():
    day_data = df[df['Flight Date'] == date].copy()
    
    # Process carrier by carrier
    for carrier, group in day_data.groupby('Carrier'):
        arrivals = group[group['Arrival/Departure'] == 'Arrival'].sort_values('Timestamp').to_dict('records')
        departures = group[group['Arrival/Departure'] == 'Departure'].sort_values('Timestamp').to_dict('records')
        
        used_deps = set()
        
        # 1. Nightstops (Before 07:00)
        for i, dep in enumerate(departures):
            if int(dep['Hour']) < 7:
                results.append({
                    'Date': date, 'Carrier': carrier, 'In_Flight': 'NIGHTSTOP', 'In_Time': '-',
                    'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                    'Type': dep['Aircraft Type IATA'], 'Status': 'Nightstop'
                })
                used_deps.add(i)

        # 2. Specific confirmed routes (User overrides)
        if carrier == 'DY':
            for arr in arrivals:
                # DY1315 -> DY1318 (London)
                if arr['Flight'] == 'DY1315':
                    for i, dep in enumerate(departures):
                        if i not in used_deps and dep['Flight'] == 'DY1318':
                            results.append({
                                'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                                'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                                'Type': arr['Aircraft Type IATA'], 'Status': 'User Confirmed (LGW)'
                            })
                            used_deps.add(i); arr['matched'] = True; break
                
                # DY620 -> DY633 (Oslo 25 min)
                elif arr['Flight'] == 'DY620':
                    for i, dep in enumerate(departures):
                        if i not in used_deps and dep['Flight'] == 'DY633':
                            results.append({
                                'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                                'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                                'Type': arr['Aircraft Type IATA'], 'Status': 'User Confirmed (OSL 25m)'
                            })
                            used_deps.add(i); arr['matched'] = True; break

                # DY604 -> DY611 (Oslo 25 min)
                elif arr['Flight'] == 'DY604':
                    for i, dep in enumerate(departures):
                        if i not in used_deps and dep['Flight'] == 'DY611':
                            results.append({
                                'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                                'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                                'Type': arr['Aircraft Type IATA'], 'Status': 'User Confirmed (OSL 25m)'
                            })
                            used_deps.add(i); arr['matched'] = True; break

        # 3. Wizz Air (WMI and GDN/SZZ)
        if carrier == 'W6':
            for arr in arrivals:
                if arr['Flight'] == 'W61419': # WMI
                    for i, dep in enumerate(departures):
                        if i not in used_deps and dep['Flight'] == 'W61420':
                            results.append({
                                'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                                'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                                'Type': arr['Aircraft Type IATA'], 'Status': 'W6-WMI Confirmed'
                            })
                            used_deps.add(i)
                            arr['matched'] = True
                            break
                elif arr['Flight'] == 'W61745': # GDN -> SZZ
                    for i, dep in enumerate(departures):
                        if i not in used_deps and dep['Flight'] == 'W62154':
                            results.append({
                                'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                                'Out_Flight': dep['Flight'], 'Out_Time': dep['Scheduled Time'],
                                'Type': arr['Aircraft Type IATA'], 'Status': 'W6-GDN Confirmed'
                            })
                            used_deps.add(i)
                            arr['matched'] = True
                            break

        # 4. General FIFO linking
        for arr in arrivals:
            if 'matched' in arr: continue
            
            potential = []
            for i, dep in enumerate(departures):
                if i in used_deps: continue
                turn_time = (dep['Timestamp'] - arr['Timestamp']).total_seconds() / 60
                type_match = arr['Aircraft Type IATA'] == dep['Aircraft Type IATA']
                
                # Turnaround window: 25 - 180 mins
                if 25 <= turn_time <= 180 and type_match:
                    potential.append(i)
            
            if potential:
                idx = potential[0] # Take the earliest departure (FIFO)
                if len(potential) > 1:
                    uncertain_cases.append({
                        'Date': date, 'Carrier': carrier, 'Arr': arr['Flight'], 'Arr_Time': arr['Scheduled Time'],
                        'Candidates': [departures[p]['Flight'] + " (" + departures[p]['Scheduled Time'] + ")" for p in potential]
                    })
                
                results.append({
                    'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                    'Out_Flight': departures[idx]['Flight'], 'Out_Time': departures[idx]['Scheduled Time'],
                    'Type': arr['Aircraft Type IATA'], 'Status': 'Auto-Linked' if len(potential) == 1 else 'Uncertain-FIFO'
                })
                used_deps.add(idx)
            else:
                results.append({
                    'Date': date, 'Carrier': carrier, 'In_Flight': arr['Flight'], 'In_Time': arr['Scheduled Time'],
                    'Out_Flight': 'STAYOVER/UNKNOWN', 'Out_Time': '-',
                    'Type': arr['Aircraft Type IATA'], 'Status': 'No Match'
                })

# Save results
pd.DataFrame(results).to_csv('G03-bergens-beste/004 data/Koblede_Fly_15jun-29jun.csv', index=False, sep=';')
print(f"File saved with {len(results)} rows.")

# Output top uncertain cases for manual check
print("\nTOP UNCERTAIN CASES:")
for c in uncertain_cases[:15]:
    print(f"{c['Date']} {c['Carrier']} | Inn: {c['Arr']} ({c['Arr_Time']}) | Mulige ut: {', '.join(c['Candidates'])}")
