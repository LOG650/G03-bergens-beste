import pandas as pd
import numpy as np
import os

def clean_and_merge_data():
    # Stier til filene
    data_dir = "G03-bergens-beste/004 data"
    flyprogram_path = os.path.join(data_dir, "Flyprogram 15jun - 29jun CSV.csv")
    koblede_fly_path = os.path.join(data_dir, "Koblede_Fly_15jun-29jun.csv")
    
    # 1. Last inn flyprogrammet for å få D/I/S og Seats per flynummer
    # Bruker low_memory=False for å unngå advarsler om dtypes
    df_prog = pd.read_csv(flyprogram_path, sep=';', encoding='utf-8')
    
    # Lag en oppslagsbok for metadata per flynummer
    # Vi tar det nyeste/første treffet for hvert flynummer (i virkeligheten kan dette variere, 
    # men for ruter er det ofte stabilt)
    meta_lookup = df_prog.drop_duplicates(subset=['Flight']).set_index('Flight')[['D/I/S', 'Seats', 'Aircraft Type']]
    
    # 2. Last inn koblede fly (rotasjoner)
    df_linked = pd.read_csv(koblede_fly_path, sep=';')
    
    # 3. Koble på metadata
    # Først prøv å koble på In_Flight
    df_merged = df_linked.merge(meta_lookup, left_on='In_Flight', right_index=True, how='left')
    
    # For de som mangler metadata (typisk Nightstops), prøv å koble på Out_Flight
    mask = df_merged['D/I/S'].isna()
    df_merged.loc[mask, ['D/I/S', 'Seats', 'Aircraft Type']] = df_merged.loc[mask, 'Out_Flight'].map(meta_lookup.to_dict('index')).apply(pd.Series)
    
    # 4. Beregn varighet (Turnaround tid)
    # Håndter Nightstops (de har ingen In_Time eller Out_Time i samme rad)
    def calculate_duration(row):
        if row['Status'] == 'Nightstop':
            return 480  # Sett en standard for nattstopp (f.eks 8 timer) for simuleringen
        try:
            # Konverter HH:MM til minutter fra midnatt
            def to_min(t_str):
                h, m = map(int, t_str.split(':'))
                return h * 60 + m
            
            start = to_min(row['In_Time'])
            end = to_min(row['Out_Time'])
            
            # Hvis det går over midnatt
            if end < start:
                return (1440 - start) + end
            return end - start
        except:
            return 45 # Default turnaround
            
    df_merged['duration_min'] = df_merged.apply(calculate_duration, axis=1)
    
    # 5. Rens og lagre
    df_final = df_merged[[
        'Date', 'Carrier', 'In_Flight', 'In_Time', 'Out_Flight', 'Out_Time', 
        'duration_min', 'D/I/S', 'Seats', 'Aircraft Type', 'Status'
    ]]
    
    output_path = os.path.join(data_dir, "simulation_input.csv")
    df_final.to_csv(output_path, index=False)
    print(f"Suksess! Vasket data lagret til: {output_path}")
    print(df_final.head())

if __name__ == "__main__":
    clean_and_merge_data()
