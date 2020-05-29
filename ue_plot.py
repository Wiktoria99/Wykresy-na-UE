#!/usr/bin/env python

'''
Argumentem jest dowlona ilość plików .csv
Skrypt rysuje wykresy z podancyh w pliku danych. 
Mozliwe jest rozpoznanie przez skrypt dwóch typów wylresów:
    - charakterystyki amplitudowo-częstotliwościowej k[dB] f[Hz] - skala logarytmiczna
    - zmiany napięcia w czasie U[V] t[s] 
Jeśli żadne z powyższyn należy podać typ skali oraz nazwy osi.
Możliwe jest nadanie nazw wykresom
'''
import pandas as pd
import plotly.graph_objects as go
from sys import argv
import numpy as np
import plotly.express as px
from scipy import stats
from datetime import datetime

# kolory:
#       | granatowy | czerwony | zielony | błękit   | fioletowy | żółty   |  pomarańcz |fukcja    |mieta    | szary  |
colors = ['#170ce8', '#eb1515', '#0b9c1c', '#35dbd0', '#ed840c', '#7a35db', '#d9db35', '#db35db', '#4ede8f', '#73656a' ]

try:
    files = argv[1:]
except IndexError:
    print('Podaj argument!')
else:
    if len(files)==1:
        # wersja dla jednego pliku
        try:
            data = pd.read_csv(files[0])
        except FileNotFoundError:
            print('Nie ma takiego pliku!')
        else:
            x = data.columns[0]
            y_vals = {name: 0 for name in data.columns[1:]}
            print("Nazwy kolumn:", *([x] + list(y_vals.keys())), sep=' | ')

            if x=='# acfrequency':
                x_type = 'log'
                x_title = 'f [Hz]'
                y_title = 'k [dB]'
            elif x =='# time':
                x_type = 'linear'
                x_title = 't [s]'
                y_title = 'U [V]'
            else:
                ver = input('Skala logarytmiczna? [t/n]: ')
                x_type  =  'linear' if ver=='n' else 'log'
                x_title = input('Nazwa osi x z jednostką: ')
                y_title = input('Nazwa osi y z jednostką: ')

            grid_color = 'rgba(100, 100, 100, 0.3)'
            zero_color = 'rgba(100, 100, 100, 0.7)'

            fig = go.Figure(go.Scatter())

            i = 0
            for val in y_vals:
                y_vals[val] = input(f'Podaj tytuł {i + 1} wykresu: ')
                i += 1
            i = 0
            for real_name, given_name in y_vals.items():
                fig.add_trace(go.Scatter(x=data[x], y=data[real_name], name=given_name, line=dict(color=colors[i%10])))
                i+=1

            fig.update_layout(plot_bgcolor='white', font=dict(family="Cambria", size=12))
            fig.update_xaxes(type=x_type, title=x_title, zerolinecolor=zero_color, gridcolor=grid_color)
            fig.update_yaxes(title=y_title, zerolinecolor=zero_color, gridcolor=grid_color)

            fig.show()
    else:
        # wersja dla kilku plików
        try:
            data = [pd.read_csv(file) for file in files]
        except FileNotFoundError:
            print('Nie znaleziono pliku!')
        else:
            x = [d.columns[0] for d in data]
            y = [d.columns[1] for d in data]

            print("Nazwy kolumn:", x[0], *y, '', sep=' | ')

            if x[0]=='# acfrequency':
                x_type = 'log'
                x_title = 'f [Hz]'
                y_title = 'k [dB]'
            elif x =='# time':
                x_type = 'linear'
                x_title = 't [s]'
                y_title = 'U [V]'
            else:
                ver = input('Skala logarytmiczna? [t/n]: ')
                x_type  =  'linear' if ver=='n' else 'log'
                x_title = input('Nazwa osi x z jednostką: ')
                y_title = input('Nazwa osi y z jednostką: ')

            grid_color = 'rgba(100, 100, 100, 0.3)'
            zero_color = 'rgba(100, 100, 100, 0.7)'

            fig = go.Figure(go.Scatter())

            for i in range(0, len(files)):
                fname = input(f'Podaj tytuł {i+1} wykresu: ')
                fig.add_trace(go.Scatter(x=data[i][x[i]], y=data[i][y[i]], name=fname, line=dict(color=colors[i%10])))

            fig.update_layout(plot_bgcolor='white', font=dict(family="Cambria", size=12))
            fig.update_xaxes(type=x_type, title=x_title, zerolinecolor=zero_color, gridcolor=grid_color)
            fig.update_yaxes(title=y_title, zerolinecolor=zero_color, gridcolor=grid_color)

            fig.show()
