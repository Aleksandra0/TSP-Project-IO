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

#----------FUNKCJA - METODA WSPINACZKI----------

def Hill_climbing(data_I, data, n, m, warunek, s): #data_I - istancja problemu, #data - uszeregowanie początkowe, m - multistart, n - ilość iteracji, warunek - parametr odpowiadający za warunek zatrzymania - "bez" - ilość iteracji bez poprawy (n), "il" - ilość iteracji ogólnie (n), s - sąsiedztwo (przyjmuje 3 wartości: "z" - zamiana zadań miejscami, "w" - wstawienie zadania na odpowiedni index, "l" - losowy mix obu sposobów)

  rows = np.shape(data)[0]
  order = copy.deepcopy(data)

  iterations_without_improvement = 0
  iterations = 0

  np.random.shuffle(order) #Pierwsze potasowanie na potrzeby przechowywania losowego wyniku
  best_order_now = copy.deepcopy(order) #Zmienna w której bedzie przechowywane najlepsze jak dotąd znalezione uszeregowanie - na poczatek jest to losowe uszeregowanie

  for i in range(0, m): #Pętla dla multistartu - m razy zaczynamy z różnych losowych miejsc startowych, aby ulepszyć algorytm w kontekście występowania ekstremów lokalnych

    #ETAP 1: Losowe uszeregowanie zadań
    np.random.shuffle(order)

    #ETAP 2: Wylosowanie 2 zadań, zamiana miejscami, sprawdzenie, któe rozwiązanie jest lepsze

    if(warunek == "bez"): #Warunek zatrzymania - ilość iteracji bez poprawy

      while iterations_without_improvement < n: #Powtarzamy operację dopóki przez n iteracji nie zanjdziemy lepszego rozwiązania niż obecne

        result1 = sum_time(data_I, order) #czas przejazdu przed zamianą

        if(s == "l"):
          #Losujemy metodę sąsiedztwa
          which_s = random.randint(0,1)
          if(which_s == 0):
            ss = "z"
          else:
            ss = "w"
        elif(s == "w"):
          ss = "w"
        elif(s == "z"):
          ss = "z"
        else:
          print("Błąd - podano zły parametr")
          return

        #Wylosowanie dwóch różnych losowych indeksów
        ii1 = random.randint(0,rows-1)
        ii2 = random.randint(0,rows-1)
        while ii1 == ii2:
          ii2 = random.randint(0,rows-1)

        if(ss == "z"):
          #Zamiana zadań miejscami
          data_to_check = copy.deepcopy(order)
          task1 = data_to_check[ii1]
          data_to_check[ii1] = data_to_check[ii2]
          data_to_check[ii2] = task1

        elif(ss == "w"):
          #Wstawienie zadania o wybranym indeksie na wylosowany indeks
          data_to_check = copy.deepcopy(order)
          task1 = data_to_check[ii1]
          data_to_check.pop(ii1) #Usunięcie miasta o wybranym indeksie z listy
          data_to_check.insert(ii2, task1) #Dodanie miasta na wybrany index

        result2 = sum_time(data_I, data_to_check) #czas przejazdu po zamianie

        if(result2 < result1): #Przyjmujemy rozwiązanie jako bazowe jeżeli wynik 2 jest mniejszy od wyniku 1
          order = copy.deepcopy(data_to_check)
          iterations_without_improvement = 0 #Zresteowanie zmienniej przechowującej ilosc iteracji bez poprawy

        iterations_without_improvement+=1

    elif(warunek == "il"): #Warunek zatrzymania - ilość iteracji ogólnie

        while iterations < n: #Powtarzamy operację n razy

          result1 = sum_time(data_I, order) #czas przejazdu przed zamianą

          if(s == "l"):
            #Losujemy metodę sąsiedztwa
            which_s = random.randint(0,1)
            if(which_s == 0):
              ss = "z"
            else:
              ss = "w"
          elif(s == "w"):
            ss = "w"
          elif(s == "z"):
            ss = "z"
          else:
            print("Błąd - podano zły parametr")
            return

          #Wylosowanie dwóch różnych losowych indeksów
          ii1 = random.randint(0,rows-1)
          ii2 = random.randint(0,rows-1)
          while ii1 == ii2:
            ii2 = random.randint(0,rows-1)

          if(ss == "z"):
            #Zamiana zadań miejscami
            data_to_check = copy.deepcopy(order)
            task1 = data_to_check[ii1]
            data_to_check[ii1] = data_to_check[ii2]
            data_to_check[ii2] = task1

          elif(ss == "w"):
            #Wstawienie zadania o wybranym indeksie na wylosowany indeks
            data_to_check = copy.deepcopy(order)
            task1 = data_to_check[ii1]
            data_to_check.pop(ii1) #Usunięcie miasta o wybranym indeksie z listy
            data_to_check.insert(ii2, task1) #Dodanie miasta na wybrany index

          result2 = sum_time(data_I, data_to_check) #czas przejazdu po zamianie
          if(result2 < result1): #Przyjmujemy rozwiązanie jako bazowe jeżeli wynik 2 jest mniejszy od wyniku 1
            order = copy.deepcopy(data_to_check)

          iterations+=1

    else:
      print("Błąd - podano zły parametr")
      return

    #Sprawdzenie czy rozwiązanie znalezione dla tego uszeregowania początkowego jest lepsze niż poprzednie:
    if(sum_time(data_I, order) < sum_time(data_I, best_order_now)):
      best_order_now = copy.deepcopy(order) #Jeżeli uzyskane rozwiązanie jest lepsze niż poprzednie, zapisujemy je do zmiennej tak aby potem zwrócić najlepsze możliwe rozwiązanie jakie zostało znalezione

  return best_order_now

  #----------METODA WSPINACZKI----------

#Tablice do przechowywania wyników
#results_climbing_E = []
results_climbing_I1 = []
results_climbing_I2 = []
results_climbing_I3 = []

#Tablice do przechowywania uszeregowań
#results2_climbing_E = []
results2_climbing_I1 = []
results2_climbing_I2 = []
results2_climbing_I3 = []

print("   ")
print("Wyniki uzyskane dla metody wspinaczki:")

for i in range(0, 30):
  best_order = Hill_climbing(data_I1, order1, 500, 3, "il", "z")
  results_climbing_I1.append(sum_time(data_I1, best_order))
  results2_climbing_I1.append(best_order)

print(results_climbing_I1) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla pierwszej instancji problemu)
print("Minimalna ze znalezionych wartości: ", min(results_climbing_I1))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_climbing_I1[results_climbing_I1.index(min(results_climbing_I1))])
print("Maksymalna ze znalezionych wartości: ", max(results_climbing_I1))
print("Srednia ze znalezionych wartości: ", np.mean(results_climbing_I1))

for i in range(0, 30):
  best_order = Hill_climbing(data_I2, order2, 500, 3, "il", "z")
  results_climbing_I2.append(sum_time(data_I2, best_order))
  results2_climbing_I2.append(best_order)

print(results_climbing_I1) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla drugiej instancji problemu)
print("Minimalna ze znalezionych wartości: ", min(results_climbing_I2))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_climbing_I2[results_climbing_I2.index(min(results_climbing_I2))])
print("Maksymalna ze znalezionych wartości: ", max(results_climbing_I2))
print("Srednia ze znalezionych wartości: ", np.mean(results_climbing_I2))

for i in range(0, 30):
  best_order = Hill_climbing(data_I3, order3, 500, 3, "il", "z")
  results_climbing_I3.append(sum_time(data_I3, best_order))
  results2_climbing_I3.append(best_order)

print(results_climbing_I3) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla trzeciej instancji problemu)
print("Minimalna ze znalezionych wartości: ", min(results_climbing_I3))
print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_climbing_I3[results_climbing_I3.index(min(results_climbing_I3))])
print("Maksymalna ze znalezionych wartości: ", max(results_climbing_I3))
print("Srednia ze znalezionych wartości: ", np.mean(results_climbing_I3))
