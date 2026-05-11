import sys
import os
import pandas as pd
from tabulate import tabulate

# Legg til src i path hvis nødvendig
sys.path.append(os.path.join(os.getcwd(), 'G03-bergens-beste/src'))
from simulation import run_simulation

def main():
    scenarios = []
    
    # 1. BASELINE
    scenarios.append({
        'name': 'Baseline (2 sjåfører, 0% vekst)',
        'antall_sjåfører': 2,
        'buss_kapasitet': 80,
        'kjøretid': 6,
        'strategisk_remote': True,
        'trafikkvekst': 0,
        'stokastisk': False
    })
    
    # 2. SJÅFØRKAPASITET
    for s in [0, 1, 3]:
        scenarios.append({
            'name': f'Sjåførkapasitet: {s} sjåfører',
            'antall_sjåfører': s,
            'buss_kapasitet': 80,
            'kjøretid': 6,
            'strategisk_remote': True,
            'trafikkvekst': 0,
            'stokastisk': False
        })
        
    # 3. REMOTE-STRATEGI AV
    scenarios.append({
        'name': 'Remote-strategi: AV',
        'antall_sjåfører': 2,
        'buss_kapasitet': 80,
        'kjøretid': 6,
        'strategisk_remote': False,
        'trafikkvekst': 0,
        'stokastisk': False
    })
    
    # 4. TRAFIKKVEKST
    for v in [0.10, 0.20, 0.30]:
        scenarios.append({
            'name': f'Trafikkvekst: +{v*100:.0f}% i peak',
            'antall_sjåfører': 2,
            'buss_kapasitet': 80,
            'kjøretid': 6,
            'strategisk_remote': True,
            'trafikkvekst': v,
            'stokastisk': False
        })
        
    # 5. STOKASTISK (Realistiske forsinkelser)
    # Vi kjører denne 5 ganger og tar snittet for å få mer robuste tall
    stokastisk_results = []
    for i in range(5):
        config = {
            'name': f'Stokastisk run {i+1}',
            'antall_sjåfører': 2,
            'buss_kapasitet': 80,
            'kjøretid': 6,
            'strategisk_remote': True,
            'trafikkvekst': 0,
            'stokastisk': True
        }
        stokastisk_results.append(run_simulation(config))
    
    # Beregn snitt for stokastisk
    avg_stokastisk = {
        'Scenario': 'Stokastiske forsinkelser (snitt 5 kjøringer)',
        'Sjåfører': 2,
        'Vekst': '0%',
        'Remote_Strat': 'PÅ',
        'Stokastisk': 'JA',
        'Fly_Totalt': stokastisk_results[0]['Fly_Totalt'],
        'Gate': sum(r['Gate'] for r in stokastisk_results) / 5,
        'Remote': sum(r['Remote'] for r in stokastisk_results) / 5,
        'Gj_Ventetid': sum(r['Gj_Ventetid'] for r in stokastisk_results) / 5,
        'Maks_Ventetid': sum(r['Maks_Ventetid'] for r in stokastisk_results) / 5,
        'Rejected': sum(r['Rejected'] for r in stokastisk_results) / 5
    }
    
    # 6. FØLSOMHET
    scenarios.append({
        'name': 'Følsomhet: Kjøretid +20% (7.2 min)',
        'antall_sjåfører': 2,
        'buss_kapasitet': 80,
        'kjøretid': 7.2,
        'strategisk_remote': True,
        'trafikkvekst': 0,
        'stokastisk': False
    })
    scenarios.append({
        'name': 'Følsomhet: Busskapasitet 60 pax',
        'antall_sjåfører': 2,
        'buss_kapasitet': 60,
        'kjøretid': 6,
        'strategisk_remote': True,
        'trafikkvekst': 0,
        'stokastisk': False
    })

    # KJØR SIMULERINGER
    all_results = []
    print("Kjører alle scenarioer...")
    for config in scenarios:
        print(f"  - {config['name']}")
        res = run_simulation(config)
        all_results.append(res)
    
    all_results.append(avg_stokastisk)
    
    # PRINT TABELL
    df_res = pd.DataFrame(all_results)
    
    # Formater tall for penere utskrift
    df_res['Gj_Ventetid'] = df_res['Gj_Ventetid'].round(2)
    df_res['Maks_Ventetid'] = df_res['Maks_Ventetid'].round(1)
    df_res['Gate'] = df_res['Gate'].round(1)
    df_res['Remote'] = df_res['Remote'].round(1)
    
    print("\n" + "="*80)
    print("OPPSUMMERING AV ALLE SCENARIOER")
    print("="*80)
    print(tabulate(df_res, headers='keys', tablefmt='pipe', showindex=False))
    print("="*80)
    
    # Lagre til CSV
    output_path = "G03-bergens-beste/004 data/scenario_results.csv"
    df_res.to_csv(output_path, index=False)
    print(f"\nResultater lagret til {output_path}")

if __name__ == "__main__":
    main()
