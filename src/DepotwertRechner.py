#!/usr/bin/env python
# coding: utf-8

# # Benutzung des Tools
# 
# 1. Unter dem Namen der Datei auf Runtime/Laufzeit drücken.
# 2. Run all auswählen.
# 3. Auf Eingabenabfrage warten und diese tätigen.

# In[1]:


import numpy as np
import pandas as pd
import pandas_datareader.data as reader
import datetime as dt
import math


# ## Eingabeaufforderung
# 
# Hier die angeforderten Eingaben ausfüllen.
# 
# - Die Anzahl der enthaltenen Positionen im Portfolio
# - Die Position und die monatliche Sparrate dieser Position
# - Das Startdatum des Portfolios
# 
# Es lassen sich mit diesem Tool nicht nur ETFs und Aktien, sondern auch Rohstoffe und alle Daten, die über Yahoo Finance zu finden sind analysieren.

# In[2]:


## Erstellen des Portfolios und Zeitraumes

# Portfolio zusammensetzen
try:
    num_assets = int(input("Wieviele Assets sind in Ihrem Musterportfolio? "))
except:
    print("Die Anzahl der Assets konnte nicht gelesen werden.\nVersuchen Sie es erneut.")
    exit()

asset_list = []
rates_list = []

for i in range(num_assets):
  asset_list.append(input("Welches Asset würden Sie gerne Ihrem Portfolio hinzufügen? "))
  rates_list.append(float(input("Wieviel zahlen monatlich in dieses Asset? ")))
portfolio = dict(zip(asset_list, rates_list))

# Zeitraum bestimmen
start_eingabe = input("Bitte geben Sie den Beginn des Portfolios ein (Format: 2015,12,7): ").split(",")
formation = dt.datetime(int(start_eingabe[0]), int(start_eingabe[1]), int(start_eingabe[2]))


# In[ ]:


## Referenzdaten bestimmen

# Gesamte monatliche Einzahlungen bestimmen
monatliche_einz = 0
for i in rates_list:
  monatliche_einz += i

referenz_depot = {'URTH': monatliche_einz, '^GSPC': monatliche_einz, '^GDAXI': monatliche_einz}


# In[ ]:


## Funktion zur Erstellung von Depots mit gebenen Einzahlungen
## Wird für eigenes und Referenzdepot verwendet
def rendite_berechnen(depot):
    
    # Kurse der Ticker einholen und monatliche Rendite berechnen
    df = reader.get_data_yahoo(list(depot.keys()),formation,interval='m')['Adj Close'].reset_index(drop=True)
    mtl_ret = df.pct_change() + 1
    
    # Depotwert nach angegebener Zeit berechnen
    depot_werte = pd.DataFrame(0,columns=depot.keys(), index=[0])
    for i in range(1, mtl_ret.shape[0]):
        for key in depot.keys():
            if (not math.isnan(df.loc[i,key])) and (not math.isnan(mtl_ret.loc[i,key])):
                depot_werte.loc[0,key] += depot[key]
                depot_werte[key] *= mtl_ret.loc[i, key]
                
    return depot_werte


# In[ ]:


## Berechnen der Depotwerte (Portfolio und Referenzdepot)

portfolio_werte = rendite_berechnen(portfolio)
referenz_werte = rendite_berechnen(referenz_depot)


# In[ ]:


## Zusammenrechnung der Einzelwerte des Porfolios

# Berechnung des Wertes des gesamten Portfolios
gesamt_depotwert = 0
for column in portfolio_werte:
  gesamt_depotwert += round(portfolio_werte[column][0],2)
  print(f"Ihr {column} wäre auf einen Wert von {round(portfolio_werte[column][0],2)}€ gewachsen.")

print(f"Ihr gesamtes Portfolio wäre somit auf einen Wert von {round(gesamt_depotwert,2)}€ gewachsen.")
print("")


# In[ ]:


## Ausgabe der Referenzwerte

print("Zum Vergleich ein paar Indizes:")
for x in referenz_werte:
  print(f"Ein {x} wäre bei gleicher Sparrate einen Wert von {round(referenz_werte[x][0],2)}€ gewachsen.")

