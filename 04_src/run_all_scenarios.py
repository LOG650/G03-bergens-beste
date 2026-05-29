import sys
from pathlib import Path
import pandas as pd
from tabulate import tabulate

# Legg til src i path hvis nødvendig
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "04_src"
DATA_DIR = PROJECT_ROOT / "03_data"
sys.path.append(str(SRC_DIR))
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
        'stokastisk': False,
        'seed': 42
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
            'stokastisk': False,
            'seed': 42 + s
        })
        
    # 3. REMOTE-STRATEGI AV
    scenarios.append({
        'name': 'Remote-strategi: AV',
        'antall_sjåfører': 2,
        'buss_kapasitet': 80,
        'kjøretid': 6,
        'strategisk_remote': False,
        'trafikkvekst': 0,
        'stokastisk': False,
        'seed': 42
    })
    
    # 4. TRAFIKKVEKST
    for idx, v in enumerate([0.10, 0.20, 0.30], start=1):
        scenarios.append({
            'name': f'Trafikkvekst: +{v*100:.0f}% i peak',
            'antall_sjåfører': 2,
            'buss_kapasitet': 80,
            'kjøretid': 6,
            'strategisk_remote': True,
            'trafikkvekst': v,
            'stokastisk': False,
            'seed': 100 + idx
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
            'stokastisk': True,
            'seed': 200 + i
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
        'stokastisk': False,
        'seed': 42
    })
    for kapasitet in [60, 70, 90]:
        scenarios.append({
            'name': f'Følsomhet: Busskapasitet {kapasitet} pax',
            'antall_sjåfører': 2,
            'buss_kapasitet': kapasitet,
            'kjøretid': 6,
            'strategisk_remote': True,
            'trafikkvekst': 0,
            'stokastisk': False,
            'seed': 42
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
    output_path = DATA_DIR / "scenario_results.csv"
    df_res.to_csv(output_path, index=False)
    print(f"\nResultater lagret til {output_path}")

if __name__ == "__main__":
    main()
