import pandas as pd
import numpy as np
import random
import math
import copy
random.seed()

#----------FUNKCJA - Obliczanie czasu przejazdu między miastami ----------
#(W obliczeniach został ujęty rowniez czas powrotu do miasta początkowego)
def sum_time(data, order): #data - tabela z której pobieramy odleglosci między miastami, order - uszeregowanie dla którego obliczamy czas przejazdu

  rows = np.shape(data)[0] #zmienna rows reprezentuje liczbę miast

  #Utworzenie tabeli z uszeregowaniem + miasto z pierwszej pozycji
  sum_of_time = copy.deepcopy(order)
  sum_of_time.append(order[0])

  sum_for_cities = 0 #Czas przejazdu między wszystkimi miastami

  for i in range(1,rows+1):
    from_city = sum_of_time[i-1]
    to_city = sum_of_time[i]
    sum_for_cities += data[from_city-1][to_city] #from_city - 1 ponieważ operujemy na indeksach od 0, to_city bez (-1) ponieważ pierwszym indexem jest numer zadania (Numer zadania w pierwszym wierszu nie został zczytany)

  return(sum_for_cities)

#----------WCZYTANIE DANYCH---------

#Problem 1:
#Wczytanie danych z githuba
url_data_I1 = 'https://raw.githubusercontent.com/Aleksandra0/Project_CI/main/Dane_TSP_48.xlsx'
data_I1 = pd.read_excel(url_data_I1)

#Zamiana na tablice dwuwymiarowa z dataframe
data_I1=data_I1.to_numpy()
rows1 = np.shape(data_I1)[0]

#Problem 2:
#Wczytanie danych z githuba
url_data_I2 = 'https://raw.githubusercontent.com/Aleksandra0/Project_CI/main/Dane_TSP_76.xlsx'
data_I2 = pd.read_excel(url_data_I2)

#Zamiana na tablice dwuwymiarowa z dataframe
data_I2=data_I2.to_numpy()
rows2 = np.shape(data_I2)[0]

#Problem 3:
#Wczytanie danych z githuba
url_data_I3 = 'https://raw.githubusercontent.com/Aleksandra0/Project_CI/main/Dane_TSP_127.xlsx'
data_I3 = pd.read_excel(url_data_I3)

#Zamiana na tablice dwuwymiarowa z dataframe
data_I3=data_I3.to_numpy()
rows3 = np.shape(data_I3)[0]

#Uszeregowania początkowe - od 1 do n
order1 = list(range(1, rows1+1))
order2 = list(range(1, rows2+1))
order3 = list(range(1, rows3+1))

sum1 = sum_time(data_I1, order1)
sum2 = sum_time(data_I2, order2)
sum3 = sum_time(data_I3, order3)

print(sum1, sum2, sum3)

#Z uwagi na to, że algorytmy nie radzą sobie z wyjściem z uszeregowania 1 - 76, przetasujemy je w losowy sposób (problem 2)
np.random.shuffle(order2)

#----------FUNKCJA - ALGORYTM NN----------

def NN(data, starting_city): #data_I - instancja problemu, starting_city - numer miasta z którego zaczynamy

  #Podmiana pustych wartości na 0 - jeśli występują
  data = np.nan_to_num(data, nan=0.0)

  order = []
  order.append(starting_city)

  rows = np.shape(data)[0]
  city = starting_city

  while(len(order) < rows):

    current_row = list(data[city-1][1:]) #Wiersz dla danego miasta, bez pierwszej pozycji (pierwsza pozycja to numer miasta)

    #Szukamy elemenyu maximum, aby podmienić 0 (odleglosc z miasta a do miasta a) na liczbe wieksza od maksymalnej odleglosci
    max1 = max(current_row)
    current_row[city-1] = max1+1 #Podmieniamy 0 na wartość wyższą od najwyższej w wierszu (aby nie przeszkadzała w obliczeniach)

    min1 = min(current_row) #Wartość najmniejsza w wierszu (Czyli czas dla najbliższego sąsiada)
    nn_city = current_row.index(min1)+1 #Numer najbliższego miasta - Dodajemy 1 ponieważ miasta zaczynają się od 1 a nie od 0

    #Sprawdzamy czy sąsiad już nie występuje:
    check = 0
    while(check == 0):
      check = 1
      for ind in order:
        if (nn_city == ind):
          check = 0
          current_row[nn_city-1]=max1+1 #Podmieniamy tą wartość na wartość największą, aby nie mogła już zostać wyszukana jako najmniejsza

      if(check == 0): #Szukamy nowego minimum
        min1 = min(current_row) #Wartość najmniejsza w wierszu (Czyli czas dla najbliższego sąsiada)
        nn_city = current_row.index(min1)+1 #Numer najbliższego miasta - Dodajemy 1 ponieważ miasta zaczynają się od 1 a nie od 0

    #Jeżeli sąsiad nie występuje dodajemy go do uszeregowania
    if(check == 1):
      order.append(nn_city)
      city = nn_city #W następnej iteracji szukamy sąsiada najbliższego obecnemu najbliższemu sąsiadowy

  return(order)


#----------ALGORYTM NN----------

#Tablice do przechowywania wyników
results_nn_I1 = []
results_nn_I2 = []
results_nn_I3 = []

#Tablice do przechowywania uszeregowań
results2_nn_I1 = []
results2_nn_I2 = []
results2_nn_I3 = []

print("   ")
print("Wyniki uzyskane dla algorytmu Najbliższego Sąsiada:")

for i in range (1, rows1+1): #Sprawdzamy działanie algorytmu dla każdego miasta po kolei
  order = NN(data_I1, i)
  #print(len(order))
  #print(np.unique(order[:]).size)
  results_nn_I1.append(sum_time(data_I1, order))
  results2_nn_I1.append(order)

print(results_nn_I1)
print("Minimalna ze znalezionych wartości: ", min(results_nn_I1))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_nn_I1[results_nn_I1.index(min(results_nn_I1))])
print("Maksymalna ze znalezionych wartości: ", max(results_nn_I1))
print("Srednia ze znalezionych wartości: ", np.mean(results_nn_I1))

for i in range (1, rows2+1): #Sprawdzamy działanie algorytmu dla każdego miasta po kolei
  order = NN(data_I2, i)
  results_nn_I2.append(sum_time(data_I2, order))
  results2_nn_I2.append(order)

print(results_nn_I2)
print("Minimalna ze znalezionych wartości: ", min(results_nn_I2))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_nn_I2[results_nn_I2.index(min(results_nn_I2))])
print("Maksymalna ze znalezionych wartości: ", max(results_nn_I2))
print("Srednia ze znalezionych wartości: ", np.mean(results_nn_I2))

for i in range (1, rows3+1): #Sprawdzamy działanie algorytmu dla każdego miasta po kolei
  order = NN(data_I3, i)
  results_nn_I3.append(sum_time(data_I3, order))
  results2_nn_I3.append(order)

print(results_nn_I3)
print("Minimalna ze znalezionych wartości: ", min(results_nn_I3))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_nn_I3[results_nn_I3.index(min(results_nn_I3))])
print("Maksymalna ze znalezionych wartości: ", max(results_nn_I3))
print("Srednia ze znalezionych wartości: ", np.mean(results_nn_I3))
