import pandas as pd

# Last inn koblede fly og originaldata
df = pd.read_csv('G03-bergens-beste/004 data/Flyprogram 15jun - 29jun CSV.csv', sep=';')
linked_df = pd.read_csv('G03-bergens-beste/004 data/Koblede_Fly_15jun-29jun.csv', sep=';')

# Lag en lookup-tabell for status (D/I/S)
status_map = df.set_index(['Flight Date', 'Flight', 'Arrival/Departure'])['D/I/S'].to_dict()

mixed_rotations = []

for _, row in linked_df.iterrows():
    if row['In_Flight'] == 'NIGHTSTOP' or row['Out_Flight'] == 'STAYOVER/UNKNOWN':
        continue
    
    in_key = (row['Date'], str(row['In_Flight']), 'Arrival')
    out_key = (row['Date'], str(row['Out_Flight']), 'Departure')
    
    in_status = status_map.get(in_key)
    out_status = status_map.get(out_key)
    
    if in_status and out_status and in_status != out_status:
        mixed_rotations.append({
            'Dato': row['Date'],
            'Selskap': row['Carrier'],
            'Fra (Status)': f"{row['In_Flight']} ({in_status})",
            'Til (Status)': f"{row['Out_Flight']} ({out_status})",
            'Tid': f"{row['In_Time']} -> {row['Out_Time']}",
            'Flytype': row['Type']
        })

if mixed_rotations:
    mixed_df = pd.DataFrame(mixed_rotations)
    print(mixed_df.to_string(index=False))
    mixed_df.to_csv('G03-bergens-beste/004 data/Statusendringer_Fly.csv', index=False, sep=';')
else:
    print("Ingen statusendringer funnet.")
