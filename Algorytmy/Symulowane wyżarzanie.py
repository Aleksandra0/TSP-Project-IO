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

#----------FUNKCJA - SYMULOWANE WYRZAŻANIE----------

def Simulated_annealing(data_I, data, n, temp, temp_reduction, dl, red_type, s): #Ilość iteracji bez poprawy, temperatura początkowa, parametr do redukcji temperatury, dl - dlugosc epoki - ile razy sprawdzimy sąsiedztwo w wewnętrznej pętli, red_type - sposób redukcji temp ("g" - geometrycznie, "a" - arytmetycznie), s - sposób wyboru sąsiedztwa

  rows = np.shape(data)[0]
  order = copy.deepcopy(data)

  iterations_without_improvement = 0

  best_order_now = copy.deepcopy(order) #Zmienna w której bedzie przechowywane najlepsze jak dotąd znalezione uszeregowanie

  t = temp #Temperatura początkowa

  #ETAP 1: Losowe uszeregowanie zadań
  np.random.shuffle(order)

  #ETAP 2: Pętla zewnętrzna - wykonywana dopóki nie jest spełnienoy warunek zatrzymania (n operacji bez poprawy)

  while iterations_without_improvement < n:

    #ETAP 3: Pętla wenętrzna - tyle razy sprawdzamy sąsiedztwo przyjętego rozwiązania w poszukiwaniu lepszego

    for i in range (0, dl):
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

      if(result2 <= result1): #Przyjmujemy rozwiązanie jako bazowe jeżeli wynik 2 jest mniejszy od wyniku 1
        order = copy.deepcopy(data_to_check)
        if(sum_time(data_I, order) < sum_time(data_I, best_order_now)):
          best_order_now = copy.deepcopy(order) #W tym miejscu również sprawdzam czy nie jest to najlepsze do tej pory znalezione rozwiązanie, jeśli tak to zapisuję je do zmiennej
      else: #Jeżeli wylosowane rozwiązanie jest gorsze, sprawdzamy na podstawie temperatury czy powinniśmy przyjąć je jako bazowe
        x = random.uniform(0, 1) #Losowa liczba z zakresu 0-1 - jeżeli będzie ona mniejsza od naszej funkcji, to przyjmiemy rozwiązanie gorsze jako bazowe
        ee = float(np.exp(-(result2-result1)/t)) #Wzór na e^[(gorsze rozw - lepsze rozw)/aktualna temperatura]
        if(x < ee): #Jeżeli wylosowany x jest mniejszy od obliczonej funkcji (zależnej od temperatury i różnicy wyników) to przyjmujemy gorsze rozwiązanie jako bazowe
          order = copy.deepcopy(data_to_check)

      if(red_type == "g"):
        #Obniżanie temperatury w sposób geometryczny
        t = t*temp_reduction
      elif(red_type == "a"):
        #Obniżanie temperatury w sposób arytmetyczny
        t = t-temp_reduction
      else:
        print("Błąd - podano zły parametr")
        return

    #Sprawdzenie czy rozwiązanie znalezione dla tego uszeregowania początkowego jest lepsze niż poprzednie:
    if(sum_time(data_I, order) < sum_time(data_I, best_order_now)):
      best_order_now = copy.deepcopy(order) #Jeżeli uzyskane rozwiązanie jest lepsze niż poprzednie, zapisujemy je do zmiennej tak aby potem zwrócić najlepsze możliwe rozwiązanie jakie zostało znalezione
      iterations_without_improvement = 0

    iterations_without_improvement+=1

  return best_order_now

#----------SYMULOWANE WYŻARZANIE----------

#Tablice do przechowywania wyników
results_sa_I1 = []
results_sa_I2 = []
results_sa_I3 = []

#Tablice do przechowywania uszeregowań
results2_sa_I1 = []
results2_sa_I2 = []
results2_sa_I3 = []


print("   ")
print("Wyniki uzyskane dla symulowanego wyżarzania:")

best_order = Simulated_annealing(data_I1, order1, 200, 100, 0.99, 10, "g", "w")
print(sum_time(data_I1, best_order))

for i in range(0, 30):
  best_order = Simulated_annealing(data_I1, order1, 100, 100, 0.99, 10, "g", "l") #parametr do redukcji temperatury musi być mniejszy od jeden (zazwyczaj między 0.8 - 0.99) - do geometrycznego, do arytmetycznego nie musi
  results_sa_I1.append(sum_time(data_I1, best_order))
  results2_sa_I1.append(best_order)

  print(i)
  print(results_sa_I1) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla pierwszej instancji problemu)
  print("Minimalna ze znalezionych wartości: ", min(results_sa_I1))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_sa_I1[results_sa_I1.index(min(results_sa_I1))])
  print("Maksymalna ze znalezionych wartości: ", max(results_sa_I1))
  print("Srednia ze znalezionych wartości: ", np.mean(results_sa_I1))

for i in range(0, 30):
  best_order = Simulated_annealing(data_I2, order2, 200, 100, 0.99, 10, "g", "l")
  results_sa_I2.append(sum_time(data_I2, best_order))
  results2_sa_I2.append(best_order)

  print(i)
  print(results_sa_I2) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla drugiej instancji problemu)
  print("Minimalna ze znalezionych wartości: ", min(results_sa_I2))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_sa_I2[results_sa_I2.index(min(results_sa_I2))])
  print("Maksymalna ze znalezionych wartości: ", max(results_sa_I2))
  print("Srednia ze znalezionych wartości: ", np.mean(results_sa_I2))

for i in range(0, 30):
  best_order = Simulated_annealing(data_I3, order3, 200, 100, 0.99, 10, "g", "l")
  results_sa_I3.append(sum_time(data_I3, best_order))
  results2_sa_I3.append(best_order)

  print(i)
  print(results_sa_I3) #Tablica przechowująca najmniejsze znalezione czasy realizacji zadań w 30tu iteracjach (dla trzeciej instancji problemu)
  print("Minimalna ze znalezionych wartości: ", min(results_sa_I3))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_sa_I3[results_sa_I3.index(min(results_sa_I3))])
  print("Maksymalna ze znalezionych wartości: ", max(results_sa_I3))
  print("Srednia ze znalezionych wartości: ", np.mean(results_sa_I3))
