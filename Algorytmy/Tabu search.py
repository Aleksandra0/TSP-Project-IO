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

#----------FUNKCJA - TABU SEARCH----------
def tabu_search(data_I, data, n, len_tabu, warunek, s): #n - liczba iteracji bez poprawy, len_tabu - długość listy tabu, warunek - warunek zatrzymania ("bez" - ilosc iteracji bez poprawy, "il" - ogolna liczba wykonań)

  rows = np.shape(data)[0]
  order = copy.deepcopy(data)

  iterations_without_improvement = 0
  iterations = 0
  tabu_list = []

  np.random.shuffle(order) #Losowe rozwiązanie
  best_order_now = copy.deepcopy(order) #Zmienna w której bedzie przechowywane najlepsze jak dotąd znalezione uszeregowanie - na poczatek jest to losowe uszeregowanie

  if(warunek == "bez"): #Warunek zatrzymania - ilość iteracji bez poprawy

    while iterations_without_improvement < n:

      results_list = [] #Lista rozwiązań

      #ETAP 1 - sprawdzenie całego sąsiedztwa (Każdy z każdym)

      if(s == "z"):
        #Sprawdzenie całego sąsiedztwa poprzez zamianę
        for i in range(0,rows):
          for j in range(i+1, rows):

            data_to_check = copy.deepcopy(order)
            task1 = data_to_check[i]
            data_to_check[i] = data_to_check[j]
            data_to_check[j] = task1
            result1 = sum_time(data_I, data_to_check)
            results_list.append([result1, i, j])

        index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
        #Wynik jest zwracany w postaci tablicy dwuelementowej - interesuje nas tylko pierwsza część czyli numer wiersza (Z tego również bierzemy inedx 0 - wartości minimalnych w zbiorze może być wiele więc bierzemy pierwszą napotkaną)

        index1 = results_list[index[0][0]][1] #index pierwszego miasta
        index2 = results_list[index[0][0]][2] #index drugiego miasta


      elif(s == "w"):
        #Sprawdzenie całego sąsiedztwa poprzez wstawianie
        #Dalsze działania związane z listą tabu są takie same, z tym, że index1 oznacza index miasta któe wstawiamy, index2 index na któe wstawiamy wybrane miasto

        #najpierw wstawiamy rozwiązanie początkowe
        result1 = sum_time(data_I, order)
        results_list.append([result1, 0, 0])
        for i in range(0,rows):
          for j in range(0,rows):
            if(i != j): #Ten przypadek pokrywa początkowe uszeregowanie
              data_to_check = copy.deepcopy(order)
              task1 = data_to_check[i]
              data_to_check.pop(i) #Usunięcie miasta o wybranym indeksie z listy
              data_to_check.insert(j, task1) #Dodanie miasta na wybrany index
              result1 = sum_time(data_I, data_to_check)
              results_list.append([result1, i, j])

        index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
        #Wynik jest zwracany w postaci tablicy dwuelementowej - interesuje nas tylko pierwsza część czyli numer wiersza (Z tego również bierzemy inedx 0 - wartości minimalnych w zbiorze może być wiele więc bierzemy pierwszą napotkaną)

        index1 = results_list[index[0][0]][1] #index pierwszego miasta
        index2 = results_list[index[0][0]][2] #index drugiego miasta

      else:
        print("Błąd - podano zły parametr")
        return


      #ETAP 2 - Operacje związane z listą Tabu
      if(len(tabu_list) != 0):
        indexes_to_check = [index1, index2]
        on_the_list = 0
        for indexes in tabu_list:
          if(indexes == indexes_to_check):
            #Operacja jest niedozowolona - zamiana znajduje się na liście tabu
            on_the_list = 1
            break

        #W pierwszej kolejności sprawdzimy czy pojawiły się inne rozwiązania, które mają taką samą wartośc (też najmniejszą) (czy dlugossc zmiennej index - obliczanej wczesniej jest większa od 1)
        if(on_the_list == 1):
          if(len(index[0]) > 1):
            on_the_list = 0
            for i in range(1, len(index[0])-1):
              index1 = results_list[index[0][i]][1] #index pierwszego miasta
              index2 = results_list[index[0][i]][2] #index drugiego miasta
              indexes_to_check = [index1, index2]
              for indexes in tabu_list:
                if(indexes == indexes_to_check):
                  on_the_list=1
              if(on_the_list == 0):
                break
                #Wychodzimy z pętli - możemy zastosować obecne index1 i index2, ponieważ znalezlismy indexy których nie ma na liscie tabu

        #Jeżeli poprzedni krok się nie powiódł szukamy kolejnego najlepszego rozwiązania
        if(on_the_list == 1):
          results_list = sorted(results_list, key=lambda x:x[0], reverse=False) #Posortowanie listy z wynikami wedlug czasow
          while(len(results_list) > 0):
            on_the_list = 0
            #Usunięcie najmniejszej wartości (Jeśli jest kilka takich samych najmniejszych wartości to wszystkie zostaną usunięte)
            for i in range(0,len(index[0])):
              results_list.pop(0)

            index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
            index1 = results_list[index[0][0]][1] #index pierwszego miasta
            index2 = results_list[index[0][0]][2] #index drugiego miasta

            #Powtarzamy wszystkie wcześniejsze kroki
            indexes_to_check = [index1, index2]

            for indexes in tabu_list:
              if(indexes == indexes_to_check):
                #Operacja jest niedozowolona - zamiana znajduje się na liście tabu
                on_the_list = 1
                break

            #W pierwszej kolejności sprawdzimy czy pojawiły się inne rozwiązania, które mają taką samą wartośc (też najmniejszą) (czy dlugossc zmiennej index - obliczanej wczesniej jest większa od 1)
            if(on_the_list == 1):
              if(len(index[0]) > 1):
                on_the_list = 0
                for i in range(1, len(index[0])-1):
                  index1 = results_list[index[0][i]][1] #index pierwszego miasta
                  index2 = results_list[index[0][i]][2] #index drugiego miasta
                  indexes_to_check = [index1, index2]
                  for indexes in tabu_list:
                    if(indexes == indexes_to_check):
                      on_the_list=1
                  if(on_the_list == 0):
                    break
                    #Wychodzimy z pętli - możemy zastosować obecne index1 i index2, ponieważ znalezlismy indexy których nie ma na liscie tabu

            if(on_the_list == 0):
              #Wychodzimy z pętli - znaleźliśmy indeksy, któe możemy zastosować
              results_list = []
              break

      #ETAP 3 - zamiana/wymiana, która ostatecznie została dozowlona
      if(s == "z"):
        task1 = order[index1]
        order[index1] = order[index2]
        order[index2] = task1
      else:
        task1 = order[index1]
        order.pop(index1) #Usunięcie miasta o wybranym indeksie z listy
        order.insert(index2, task1) #Dodanie miasta na wybrany index

      #ETAP 4 - Zaktualizowanie listy tabu (jeśli jest za długa usuwamy pierwszy wiersz)
      tabu_list.append([index1,index2])
      if(len(tabu_list) > len_tabu):
        tabu_list.pop(0) #usuniecie pierwszego elementu z tablicy

      if(sum_time(data_I, order) < sum_time(data_I, best_order_now)):
        best_order_now = copy.deepcopy(order) #Jeżeli uzyskane rozwiązanie jest lepsze niż poprzednie, zapisujemy je do zmiennej tak aby potem zwrócić najlepsze możliwe rozwiązanie jakie zostało znalezione
        iterations_without_improvement = 0

      iterations_without_improvement+=1

  elif(warunek == "il"): #Warunek zatrzymania - ilość iteracji ogólnie

    while iterations < n:

      results_list = [] #Lista rozwiązań

      #ETAP 1 - sprawdzenie całego sąsiedztwa (Każdy z każdym)

      if(s == "z"):
        #Sprawdzenie całego sąsiedztwa poprzez zamianę
        for i in range(0,rows):
          for j in range(i+1, rows):

            data_to_check = copy.deepcopy(order)
            task1 = data_to_check[i]
            data_to_check[i] = data_to_check[j]
            data_to_check[j] = task1
            result1 = sum_time(data_I, data_to_check)
            results_list.append([result1, i, j])

        index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
        #Wynik jest zwracany w postaci tablicy dwuelementowej - interesuje nas tylko pierwsza część czyli numer wiersza (Z tego również bierzemy inedx 0 - wartości minimalnych w zbiorze może być wiele więc bierzemy pierwszą napotkaną)

        index1 = results_list[index[0][0]][1] #index pierwszego miasta
        index2 = results_list[index[0][0]][2] #index drugiego miasta


      elif(s == "w"):
        #Sprawdzenie całego sąsiedztwa poprzez wstawianie
        #Dalsze działania związane z listą tabu są takie same, z tym, że index1 oznacza index miasta któe wstawiamy, index2 index na któe wstawiamy wybrane miasto

        #najpierw wstawiamy rozwiązanie początkowe
        result1 = sum_time(data_I, order)
        results_list.append([result1, 0, 0])
        for i in range(0,rows):
          for j in range(0,rows):
            if(i != j): #Ten przypadek pokrywa początkowe uszeregowanie
              data_to_check = copy.deepcopy(order)
              task1 = data_to_check[i]
              data_to_check.pop(i) #Usunięcie miasta o wybranym indeksie z listy
              data_to_check.insert(j, task1) #Dodanie miasta na wybrany index
              result1 = sum_time(data_I, data_to_check)
              results_list.append([result1, i, j])

        index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
        #Wynik jest zwracany w postaci tablicy dwuelementowej - interesuje nas tylko pierwsza część czyli numer wiersza (Z tego również bierzemy inedx 0 - wartości minimalnych w zbiorze może być wiele więc bierzemy pierwszą napotkaną)

        index1 = results_list[index[0][0]][1] #index pierwszego miasta
        index2 = results_list[index[0][0]][2] #index drugiego miasta

      else:
        print("Błąd - podano zły parametr")
        return


      #ETAP 2 - Operacje związane z listą Tabu
      if(len(tabu_list) != 0):
        indexes_to_check = [index1, index2]
        on_the_list = 0
        for indexes in tabu_list:
          if(indexes == indexes_to_check):
            #Operacja jest niedozowolona - zamiana znajduje się na liście tabu
            on_the_list = 1
            break

        #W pierwszej kolejności sprawdzimy czy pojawiły się inne rozwiązania, które mają taką samą wartośc (też najmniejszą) (czy dlugossc zmiennej index - obliczanej wczesniej jest większa od 1)
        if(on_the_list == 1):
          if(len(index[0]) > 1):
            on_the_list = 0
            for i in range(1, len(index[0])-1):
              index1 = results_list[index[0][i]][1] #index pierwszego miasta
              index2 = results_list[index[0][i]][2] #index drugiego miasta
              indexes_to_check = [index1, index2]
              for indexes in tabu_list:
                if(indexes == indexes_to_check):
                  on_the_list=1
              if(on_the_list == 0):
                break
                #Wychodzimy z pętli - możemy zastosować obecne index1 i index2, ponieważ znalezlismy indexy których nie ma na liscie tabu

        #Jeżeli poprzedni krok się nie powiódł szukamy kolejnego najlepszego rozwiązania
        if(on_the_list == 1):
          results_list = sorted(results_list, key=lambda x:x[0], reverse=False) #Posortowanie listy z wynikami wedlug czasow
          while(len(results_list) > 0):
            on_the_list = 0
            #Usunięcie najmniejszej wartości (Jeśli jest kilka takich samych najmniejszych wartości to wszystkie zostaną usunięte)
            for i in range(0,len(index[0])):
              results_list.pop(0)


            index = np.where(results_list == np.amin(results_list, axis=0)[0]) #index minimalnej wartości z kolumny zerowej (czyli index minimalnej wartości spośród wyników z całego sąsiedztwa)
            index1 = results_list[index[0][0]][1] #index pierwszego miasta
            index2 = results_list[index[0][0]][2] #index drugiego miasta


            #Powtarzamy wszystkie wcześniejsze kroki
            indexes_to_check = [index1, index2]

            for indexes in tabu_list:
              if(indexes == indexes_to_check):
                #Operacja jest niedozowolona - zamiana znajduje się na liście tabu
                on_the_list = 1
                break

            #W pierwszej kolejności sprawdzimy czy pojawiły się inne rozwiązania, które mają taką samą wartośc (też najmniejszą) (czy dlugossc zmiennej index - obliczanej wczesniej jest większa od 1)
            if(on_the_list == 1):
              if(len(index[0]) > 1):
                on_the_list = 0
                for i in range(1, len(index[0])-1):
                  index1 = results_list[index[0][i]][1] #index pierwszego miasta
                  index2 = results_list[index[0][i]][2] #index drugiego miasta
                  indexes_to_check = [index1, index2]
                  for indexes in tabu_list:
                    if(indexes == indexes_to_check):
                      on_the_list=1
                  if(on_the_list == 0):
                    break
                    #Wychodzimy z pętli - możemy zastosować obecne index1 i index2, ponieważ znalezlismy indexy których nie ma na liscie tabu

            if(on_the_list == 0):
              #Wychodzimy z pętli - znaleźliśmy indeksy, któe możemy zastosować
              results_list = []
              break

      #ETAP 3 - zamiana/wymiana, która ostatecznie została dozowlona
      if(s == "z"):
        task1 = order[index1]
        order[index1] = order[index2]
        order[index2] = task1
      else:
        task1 = order[index1]
        order.pop(index1) #Usunięcie miasta o wybranym indeksie z listy
        order.insert(index2, task1) #Dodanie miasta na wybrany index


      #ETAP 4 - Zaktualizowanie listy tabu (jeśli jest za długa usuwamy pierwszy wiersz)
      tabu_list.append([index1,index2])
      if(len(tabu_list) > len_tabu):
        tabu_list.pop(0) #usuniecie pierwszego elementu z tablicy

      if(sum_time(data_I, order) < sum_time(data_I, best_order_now)):
        best_order_now = copy.deepcopy(order) #Jeżeli uzyskane rozwiązanie jest lepsze niż poprzednie, zapisujemy je do zmiennej tak aby potem zwrócić najlepsze możliwe rozwiązanie jakie zostało znalezione

      iterations+=1

  else:
    print("Błąd - podano zły parametr")
    return

  return best_order_now


#----------TABU SEARCH----------

#Tablice do przechowywania wyników
results_ts_I1 = []
results_ts_I2 = []
results_ts_I3 = []

#Tablice do przechowywania uszeregowań
results2_ts_I1 = []
results2_ts_I2 = []
results2_ts_I3 = []

print("   ")
print("Wyniki uzyskane dla algorytmu tabu search: ")

#Algorytm Tabu search również puszczamy 30 razy ponieważ za każdym razem losujemy inne rozwiązanie pozątkowe

for i in range(0, 30):
  best_order = tabu_search(data_I1, order1, 5000, 50, "il", "z")
  results_ts_I1.append(sum_time(data_I1, best_order))
  results2_ts_I1.append(best_order)

  print(i)
  print(results_ts_I1)
  print("Minimalna ze znalezionych wartości: ", min(results_ts_I1))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ts_I1[results_ts_I1.index(min(results_ts_I1))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ts_I1))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ts_I1))

for i in range(0, 30):
  best_order = tabu_search(data_I2, order2, 5000, 50, "il", "z")
  results_ts_I2.append(sum_time(data_I2, best_order))
  results2_ts_I2.append(best_order)

  print(i)
  print(results_ts_I2)
  print("Minimalna ze znalezionych wartości: ", min(results_ts_I2))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ts_I2[results_ts_I2.index(min(results_ts_I2))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ts_I2))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ts_I2))

for i in range(0, 30):
  best_order = tabu_search(data_I3, order3, 5000, 50, "il", "z")
  results_ts_I3.append(sum_time(data_I3, best_order))
  results2_ts_I3.append(best_order)

  print(i)
  print(results_ts_I3)
  print("Minimalna ze znalezionych wartości: ", min(results_ts_I3))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ts_I3[results_ts_I3.index(min(results_ts_I3))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ts_I3))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ts_I3))
