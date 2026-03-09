import simpy
import pandas as pd
import random

# Konfigurasjon (Disse tallene justerer du når du vet mer)
ANTALL_GATER = 14          # Antall vanlige gater (med bro)
ANTALL_REMOTE_STANDS = 5  # Antall remote stands
ANTALL_BUSSER = 2         # Antall busser tilgjengelig
BUSS_KAPASITET = 70       # Hvor mange passasjerer en buss tar
BUSS_TUR_RETUR_TID = 10   # Minutter en buss bruker på å kjøre tur/retur terminal

SIMULERINGSTID = 60      # Vi simulerer 2 timer (i minutter)

class Flyplass:
    def __init__(self, env):
        self.env = env
        # Ressurser
        self.gater = simpy.Resource(env, capacity=ANTALL_GATER)
        self.remote_stands = simpy.Resource(env, capacity=ANTALL_REMOTE_STANDS)
        self.busser = simpy.Resource(env, capacity=ANTALL_BUSSER)

    def kjør_buss(self, fly_id, antall_passasjerer):
        """Simulerer busstransport for et fly på remote stand"""
        antall_turer = (antall_passasjerer + BUSS_KAPASITET - 1) // BUSS_KAPASITET
        print(f"  {self.env.now}: 🚌 Fly {fly_id} trenger {antall_turer} bussturer for {antall_passasjerer} pax.")
        
        for tur in range(antall_turer):
            with self.busser.request() as request:
                yield request # Vent på ledig buss
                print(f"  {self.env.now}: 🚌 Buss starter tur {tur+1} for {fly_id}")
                yield self.env.timeout(BUSS_TUR_RETUR_TID) # Kjøretid
                print(f"  {self.env.now}: 🚌 Buss ferdig med tur {tur+1} for {fly_id}")

def fly_prosess(env, fly_data, flyplass):
    """Selve livssyklusen til et fly i systemet"""
    fly_id = fly_data['flight_id']
    print(f"{env.now}: ✈️  Fly {fly_id} har landet.")

    # 1. Prøv å få gate først (Prioritert)
    # Her kan du legge inn logikk: "Hvis Schengen, prøv Schengen-gate først"
    # For nå gjør vi det enkelt: Prøv gate, hvis full -> remote stand.
    
    if flyplass.gater.count < flyplass.gater.capacity:
        with flyplass.gater.request() as gate_request:
            yield gate_request
            print(f"{env.now}: 🟢 Fly {fly_id} parkerte ved GATE.")
            yield env.timeout(fly_data['turnaround_time_min'])
            print(f"{env.now}: 🛫 Fly {fly_id} drar fra gate.")
            
    else:
        # 2. Hvis ingen gate, bruk remote stand
        print(f"{env.now}: ⚠️  Ingen gate ledig for {fly_id}, prøver REMOTE stand.")
        
        with flyplass.remote_stands.request() as remote_request:
            yield remote_request
            print(f"{env.now}: 🟡 Fly {fly_id} parkerte ved REMOTE stand.")
            
            # Start bussprosess parallelt med turnaround
            # (I virkeligheten venter man kanskje litt før bussene kommer, men vi kjører det nå)
            yield env.process(flyplass.kjør_buss(fly_id, fly_data['passengers']))
            
            # Vi antar flyet må stå der minst like lenge som turnaround-tiden
            yield env.timeout(fly_data['turnaround_time_min'])
            print(f"{env.now}: 🛫 Fly {fly_id} drar fra remote stand.")

import os

def start_simulering():
    # Finn stien til denne filen og gå opp ett nivå til prosjektmappen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "004 data", "dummy_flight_data.csv")

    # Last inn data
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Fant ikke datafilen på: {data_path}")
        return

    # Konverter tidspunkt '08:00' til minutter fra start (f.eks. start kl 08:00 = 0)
    # For enkelhets skyld sier vi at simuleringen starter 08:00.
    start_time_str = "08:00"
    base_time = pd.to_datetime(start_time_str, format='%H:%M')

    env = simpy.Environment()
    flyplass = Flyplass(env)

    print(f"--- Starter simulering (Starttid: {start_time_str}) ---")
    print(f"Ressurser: {ANTALL_GATER} gater, {ANTALL_REMOTE_STANDS} remote stands, {ANTALL_BUSSER} busser.")

    # Planlegg alle flyene
    for index, row in df.iterrows():
        flight_time = pd.to_datetime(row['arrival_time'], format='%H:%M')
        delay_minutes = (flight_time - base_time).total_seconds() / 60
        
        if delay_minutes < 0: continue # Hopp over fly før starttid
        
        env.process(delayed_start(env, delay_minutes, row, flyplass))

    env.run(until=SIMULERINGSTID)
    print("--- Simulering ferdig ---")

def delayed_start(env, delay, fly_data, flyplass):
    """Hjelpefunksjon for å starte flyet på riktig tidspunkt"""
    yield env.timeout(delay)
    env.process(fly_prosess(env, fly_data, flyplass))

if __name__ == "__main__":
    start_simulering()
