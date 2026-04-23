import simpy
import pandas as pd
import numpy as np
import os

# --- KONFIGURASJON ---
ANTALL_SJÅFØRER = 2 
BUSS_KAPASITET = 80
KJØRETID = 6 

INNLAND_FASTE = [15, 16, 17, 18, 19, 20] 
NON_SCHENGEN_BASE = [23]
FLEX_NS_S = [24, 25, 26, 27]     
FLEX_S_D = [28, 29, 30, 31, 32] 

REMOTE_STANDS = [3, 4, 5, 6, 7, 41, 43, 9, 11]

class Flyplass:
    def __init__(self, env):
        self.env = env
        self.busser = simpy.Resource(env, capacity=4)
        self.sjåfører = simpy.Resource(env, capacity=ANTALL_SJÅFØRER)
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

def busstransport(env, flyplass, fly_id, pax):
    flyplass.aktive_buss_oppdrag += 1
    turer = int(np.ceil(pax / BUSS_KAPASITET))
    def tur():
        with flyplass.busser.request() as rb, flyplass.sjåfører.request() as rs:
            yield rb & rs
            yield env.timeout(KJØRETID)
    yield simpy.AllOf(env, [env.process(tur()) for _ in range(turer)])
    flyplass.aktive_buss_oppdrag -= 1

def fly_prosess(env, fly_data, flyplass, smp):
    fly_id = fly_data['In_Flight'] if fly_data['In_Flight'] != 'NIGHTSTOP' else fly_data['Out_Flight']
    sone = fly_data['D/I/S']
    pax = fly_data['Seats'] if not np.isnan(fly_data['Seats']) else 150
    ankomst_min = env.now
    er_peak = (900 <= (smp + env.now) <= 1050)
    er_lite_fly = (pax < 120)

    # LOGIKK: Strategisk Remote i Peak
    if er_lite_fly and er_peak:
        if flyplass.aktive_buss_oppdrag < ANTALL_SJÅFØRER:
            remote = next((s for s, v in flyplass.remote_status.items() if v is None), None)
            if remote:
                flyplass.remote_status[remote] = fly_id
                flyplass.stats['remote_count'] += 1
                flyplass.stats['wait_times'].append(0) 
                yield env.process(busstransport(env, flyplass, fly_id, pax))
                yield env.timeout(max(0, fly_data['duration_min'] - 6))
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
        
        # Hvis vi har ventet 15 min, prøv remote uansett flystørrelse
        if env.now - ankomst_min >= 15:
            remote = next((s for s, v in flyplass.remote_status.items() if v is None), None)
            if remote:
                wait_time = env.now - ankomst_min
                flyplass.stats['wait_times'].append(wait_time)
                flyplass.stats['remote_count'] += 1
                flyplass.remote_status[remote] = fly_id
                yield env.process(busstransport(env, flyplass, fly_id, pax))
                yield env.timeout(max(0, fly_data['duration_min'] - 6))
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

def start_simulering():
    df = pd.read_csv("G03-bergens-beste/004 data/simulation_input.csv")
    df = df[df['Date'] == "2026-06-17"].copy()
    def parse_t(s):
        if not isinstance(s, str) or ':' not in s: return 0
        h, m = map(int, s.split(':'))
        return h * 60 + m
    df['In_Min'] = df['In_Time'].apply(parse_t)
    df = df.sort_values(by=['In_Min', 'Seats'], ascending=[True, False])
    
    env = simpy.Environment()
    flyplass = Flyplass(env)
    smp = df['In_Min'].min()
    
    for _, row in df.iterrows():
        env.process(delayed_start(env, max(0, row['In_Min'] - smp), row, flyplass, smp))
    
    env.run(until=1440)
    
    # Rapport
    print(f"\n--- SIMULERINGSRESULTATER ---")
    print(f"Strategi: Små fly (<120) til remote i peak (15:00-17:30)")
    print(f"Totalt antall fly håndtert: {len(flyplass.stats['wait_times'])}")
    print(f"Fly til Gate: {flyplass.stats['gate_count']}")
    print(f"Fly til Remote: {flyplass.stats['remote_count']}")
    
    if flyplass.stats['wait_times']:
        avg_wait = sum(flyplass.stats['wait_times']) / len(flyplass.stats['wait_times'])
        max_wait = max(flyplass.stats['wait_times'])
        print(f"Gjennomsnittlig ventetid: {avg_wait:.1f} min")
        print(f"Maksimal ventetid: {max_wait} min")
    
    print(f"Antall fly som ikke fikk plass: {flyplass.stats['rejected']}")
    print(f"-----------------------------\n")

def delayed_start(env, delay, row, flyplass, smp):
    yield env.timeout(delay)
    yield env.process(fly_prosess(env, row, flyplass, smp))

if __name__ == "__main__":
    start_simulering()
