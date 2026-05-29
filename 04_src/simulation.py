import simpy
import pandas as pd
import numpy as np
from pathlib import Path

# --- KONFIGURASJON (DEFAULTS) ---
BUSS_KAPASITET_DEFAULT = 80
KJØRETID_DEFAULT = 6 
DEFAULT_SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "03_data"

INNLAND_FASTE = [15, 16, 17, 18, 19, 20] 
NON_SCHENGEN_BASE = [23]
FLEX_NS_S = [24, 25, 26, 27]     
FLEX_S_D = [28, 29, 30, 31, 32] 

REMOTE_STANDS = [3, 4, 5, 6, 7, 41, 43, 9, 11]

class Flyplass:
    def __init__(self, env, antall_sjåfører, buss_kapasitet):
        self.env = env
        self.busser = simpy.Resource(env, capacity=4)
        self.antall_sjåfører = antall_sjåfører
        if antall_sjåfører > 0:
            self.sjåfører = simpy.Resource(env, capacity=antall_sjåfører)
        else:
            self.sjåfører = None
        self.buss_kapasitet = buss_kapasitet
        self.gate_status = {g: None for g in INNLAND_FASTE + NON_SCHENGEN_BASE + FLEX_NS_S + FLEX_S_D}
        self.remote_status = {s: None for s in REMOTE_STANDS}
        self.active_flight_zones = {}
        self.stats = {
            'gate_count': 0,
            'remote_count': 0,
            'wait_times': [],
            'rejected': 0
        }
        self.gate_ledig_event = env.event()
        self.aktive_buss_oppdrag = 0

    def sjekk_sone_konflikt(self, gate, sone):
        if gate in FLEX_NS_S:
            for g in FLEX_NS_S:
                if self.gate_status[g] is not None:
                    if self.active_flight_zones.get(self.gate_status[g]) != sone:
                        return False
        return True

    def finn_ledig_gate(self, sone):
        rekkefølge = []
        if sone == 'D': rekkefølge = INNLAND_FASTE + [32, 31, 30, 29, 28]
        elif sone == 'S': rekkefølge = [28, 29, 30, 31, 32] + FLEX_NS_S
        elif sone == 'I': rekkefølge = NON_SCHENGEN_BASE + FLEX_NS_S
            
        for g in rekkefølge:
            if self.gate_status[g] is None and self.sjekk_sone_konflikt(g, sone):
                if sone == 'D' and g not in (INNLAND_FASTE + FLEX_S_D): continue
                if sone == 'S' and g not in (FLEX_NS_S + FLEX_S_D): continue
                if sone == 'I' and g not in (NON_SCHENGEN_BASE + FLEX_NS_S): continue
                return g
        return None

def busstransport(env, flyplass, fly_id, pax, kjøretid):
    if flyplass.sjåfører is None:
        return # Kan ikke transportere uten sjåfør
    flyplass.aktive_buss_oppdrag += 1
    turer = int(np.ceil(pax / flyplass.buss_kapasitet))
    def tur():
        with flyplass.busser.request() as rb, flyplass.sjåfører.request() as rs:
            yield rb & rs
            yield env.timeout(kjøretid)
    yield simpy.AllOf(env, [env.process(tur()) for _ in range(turer)])
    flyplass.aktive_buss_oppdrag -= 1

def fly_prosess(env, fly_data, flyplass, smp, config):
    fly_id = fly_data['In_Flight'] if fly_data['In_Flight'] != 'NIGHTSTOP' else fly_data['Out_Flight']
    sone = fly_data['D/I/S']
    pax = fly_data['Seats'] if not np.isnan(fly_data['Seats']) else 150
    ankomst_min = env.now
    
    # Sjekk peak (15:00-17:30 = 900-1050 min fra midnatt)
    aktuelt_tidspunkt = smp + env.now
    er_peak = (900 <= aktuelt_tidspunkt <= 1050)
    er_lite_fly = (pax < 120)

    # LOGIKK: Strategisk Remote i Peak
    if config['strategisk_remote'] and er_lite_fly and er_peak:
        if flyplass.sjåfører and flyplass.aktive_buss_oppdrag < config['antall_sjåfører']:
            remote = next((s for s, v in flyplass.remote_status.items() if v is None), None)
            if remote:
                flyplass.remote_status[remote] = fly_id
                flyplass.stats['remote_count'] += 1
                flyplass.stats['wait_times'].append(0) 
                yield env.process(busstransport(env, flyplass, fly_id, pax, config['kjøretid']))
                yield env.timeout(max(0, fly_data['duration_min'] - config['kjøretid']))
                flyplass.remote_status[remote] = None
                if not flyplass.gate_ledig_event.triggered:
                    flyplass.gate_ledig_event.succeed()
                    flyplass.gate_ledig_event = flyplass.env.event()
                return

    # Vanlig gate-søk med ventetid
    while True:
        gate = flyplass.finn_ledig_gate(sone)
        if gate:
            wait_time = env.now - ankomst_min
            flyplass.stats['wait_times'].append(wait_time)
            flyplass.stats['gate_count'] += 1
            yield env.process(parker(env, fly_id, gate, sone, fly_data, flyplass, smp, ankomst_min, pax))
            return
        
        # Hvis vi har ventet 15 min, prøv remote uansett flystørrelse (MEN KUN HVIS VI HAR SJÅFØRER)
        if env.now - ankomst_min >= 15 and flyplass.sjåfører:
            remote = next((s for s, v in flyplass.remote_status.items() if v is None), None)
            if remote:
                wait_time = env.now - ankomst_min
                flyplass.stats['wait_times'].append(wait_time)
                flyplass.stats['remote_count'] += 1
                flyplass.remote_status[remote] = fly_id
                yield env.process(busstransport(env, flyplass, fly_id, pax, config['kjøretid']))
                yield env.timeout(max(0, fly_data['duration_min'] - config['kjøretid']))
                flyplass.remote_status[remote] = None
                if not flyplass.gate_ledig_event.triggered:
                    flyplass.gate_ledig_event.succeed()
                    flyplass.gate_ledig_event = flyplass.env.event()
                return

        yield flyplass.gate_ledig_event | env.timeout(1)

def parker(env, fly_id, gate, sone, fly_data, flyplass, smp, ankomst_min, pax):
    flyplass.gate_status[gate] = fly_id
    flyplass.active_flight_zones[fly_id] = sone
    yield env.timeout(fly_data['duration_min'])
    flyplass.gate_status[gate] = None
    if fly_id in flyplass.active_flight_zones: del flyplass.active_flight_zones[fly_id]
    if not flyplass.gate_ledig_event.triggered:
        flyplass.gate_ledig_event.succeed()
        flyplass.gate_ledig_event = flyplass.env.event()

def run_simulation(config):
    # Laste data
    df = pd.read_csv(DATA_DIR / "simulation_input.csv")
    df = df[df['Date'] == "2026-06-17"].copy()
    seed = config.get('seed', DEFAULT_SEED)
    rng = np.random.default_rng(seed)
    
    def parse_t(s):
        if not isinstance(s, str) or ':' not in s: return 0
        h, m = map(int, s.split(':'))
        return h * 60 + m
    
    df['In_Min'] = df['In_Time'].apply(parse_t)
    
    # Håndtere trafikkvekst i peak
    if config['trafikkvekst'] > 0:
        peak_flights = df[(df['In_Min'] >= 900) & (df['In_Min'] <= 1050)].copy()
        num_extra = int(len(peak_flights) * config['trafikkvekst'])
        if num_extra > 0:
            extra_flights = peak_flights.sample(n=num_extra, replace=True, random_state=seed).copy()
            # Legg til litt forskyvning så de ikke kommer nøyaktig samtidig
            extra_flights['In_Min'] += rng.integers(-5, 6, size=len(extra_flights))
            df = pd.concat([df, extra_flights])
    
    # Legg til stokastiske forsinkelser
    if config['stokastisk']:
        # Bruk en eksponentialfordeling for forsinkelser (alltid positiv eller null)
        # Gjennomsnittlig 5 min forsinkelse, noen mer
        forsinkelser = rng.exponential(scale=5, size=len(df))
        df['In_Min'] += forsinkelser
    
    df = df.sort_values(by=['In_Min', 'Seats'], ascending=[True, False])
    
    env = simpy.Environment()
    flyplass = Flyplass(env, config['antall_sjåfører'], config['buss_kapasitet'])
    smp = df['In_Min'].min()
    
    for _, row in df.iterrows():
        env.process(delayed_start(env, max(0, row['In_Min'] - smp), row, flyplass, smp, config))
    
    env.run(until=1440 + 500) # Kjør litt lenger for å tømme systemet
    
    # Samle resultater
    res = {
        'Scenario': config['name'],
        'Sjåfører': config['antall_sjåfører'],
        'Vekst': f"{config['trafikkvekst']*100:.0f}%",
        'Remote_Strat': 'PÅ' if config['strategisk_remote'] else 'AV',
        'Stokastisk': 'JA' if config['stokastisk'] else 'NEI',
        'Fly_Totalt': len(flyplass.stats['wait_times']),
        'Gate': flyplass.stats['gate_count'],
        'Remote': flyplass.stats['remote_count'],
        'Gj_Ventetid': np.mean(flyplass.stats['wait_times']) if flyplass.stats['wait_times'] else 0,
        'Maks_Ventetid': max(flyplass.stats['wait_times']) if flyplass.stats['wait_times'] else 0,
        'Rejected': flyplass.stats['rejected']
    }
    return res

def delayed_start(env, delay, row, flyplass, smp, config):
    yield env.timeout(delay)
    yield env.process(fly_prosess(env, row, flyplass, smp, config))

if __name__ == "__main__":
    # Standard kjøring hvis man bare kjører fila
    config = {
        'name': 'Baseline',
        'antall_sjåfører': 2,
        'buss_kapasitet': 80,
        'kjøretid': 6,
        'strategisk_remote': True,
        'trafikkvekst': 0,
        'stokastisk': False,
        'seed': DEFAULT_SEED
    }
    res = run_simulation(config)
    print(res)
