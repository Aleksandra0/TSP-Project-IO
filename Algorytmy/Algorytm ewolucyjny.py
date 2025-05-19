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

#----------FUNKCJE - ALGORYTMY GENETYCZNE----------

def evolutionary(data_I, data, n, pop, method, method_c, p_c, p_m, s): #n - ilość iteracji bez poprawy #pop - wielkość populacji początkowej, method - metoda wyboru rodziców ("ru" - ruletka, "rd" - ranking dopasowania), method_c - metoda krzyżownaia ("pmx", "ox") , p_c - prawdopodobieńśtwo krzyżowania, p_m - prawdopodobieństwo mutacji, s - rodzaj sąsiedztwa (stosowany tylko przy mutacji)

  rows = np.shape(data)[0]
  order = copy.deepcopy(data)

  population = [] #Tablica zawierająca populację początkową

  best_order_now = copy.deepcopy(order)

  #ETAP 1 - Wylosowanie populacji początkowej
  for i in range(0, pop):
    np.random.shuffle(order)
    order2 = copy.deepcopy(order)
    population.append(order2)

  #Pętla zewnętrzna - ilość iteracji bez poprawy

  iterations_without_improvement = 0

  while(iterations_without_improvement < n):

    #ETAP 2 - przygotowanie do wyboru rodziców

    times = [] #Czasy przejazdu dla osobników w populacji
    index = 0;
    for ind in population:
      ind = list(ind)
      times.append([index, sum_time(data_I, ind), 0, 0]) #Dwa zera na końcu to miejsce na prawdopodobieńśtwo i dystrybuantę (Potrzebne do kolejnego kroku - wyboru rodziców)
      index+=1

    mean_te = np.mean(times, axis=0)
    mean_times_earlier = mean_te[1] #Średnia z drugiej kolumny tablicy times - czyli średnia wszystkich obliczonych czasów przejazdu między miastami

    #ETAP 3 - Wybór rodziców (W zależności od wybranego parametru: ranking dopasowania - "rd", ruletka - "ru")

    parents = [] #Tablica rodziców

    #Prawdopodobieńśtwo obliczne na podstawie sumy rang - ponieważ poszukujemy jak najmniejszej wartości musimy odwrócić sortowanie tablicy (Chcemy aby najgorszy osobnik miał rangę 1)
    times_sorted_rev = sorted(times, key=lambda x:x[1], reverse=True)

    #Dodanie kolumny na rangi/wielkosc dopasowania
    rows2 = np.shape(times_sorted_rev)[0]
    ra = np.zeros(shape=(rows2,1))
    ra = ra.astype(int)
    times_sorted_rev = np.hstack((times_sorted_rev,ra))

    if(method == "ru"):

      #Prawdopodobieństwo obliczane nie na podstawie rang, a wielkości dopasownaia (Ze względu na to, że mamy do czynienia z problemem minimalizacji jako wielkość dopasowanaia wezmiemy najgorszy czas + 1 - czas)
      sum_d = (times_sorted_rev[0][1])+1

      #Dodanie wielkosci dopasowania:
      sum_dop = 0;
      for i in range(0,rows2):
        times_sorted_rev[i][2]=(sum_d-times_sorted_rev[i][1])
        sum_dop += (sum_d-times_sorted_rev[i][1])

      #Obliczenie prawdopodobieństwa i dystrybuanty
      times_sorted_rev = times_sorted_rev.astype(float)
      distr=0
      for i in range(0,rows2):
        times_sorted_rev[i][3] = (times_sorted_rev[i][2])/sum_dop
        distr += (times_sorted_rev[i][2])/sum_dop
        times_sorted_rev[i][4] = distr

      #Usunięcie kolumny z dopasowaniami
      times_sorted_rev = np.delete(times_sorted_rev, 2, 1)

    elif(method == "rd"):

      #Dodanie rang:
      sum_r = 0; #Suma rang
      for i in range(1,rows2+1):
        times_sorted_rev[i-1][2]=i
        sum_r += i

      #Obliczenie prawdopodobieństwa i dystrybuanty
      times_sorted_rev = times_sorted_rev.astype(float)
      distr=0
      for i in range(0,rows2):
        times_sorted_rev[i][3] = (times_sorted_rev[i][2])/sum_r
        distr += (times_sorted_rev[i][2])/sum_r
        times_sorted_rev[i][4] = distr

      #Usunięcie kolumny z rangami
      times_sorted_rev = np.delete(times_sorted_rev, 2, 1)

      #Na koniec tego etapu - tablica times_sorted_rev zawiera koljeno: nr uszeregowania, czas, prawdopodobieństwo i dystrybuantę

    else:
      print("Błąd - podano zły parametr")
      return

    which_parents = [] #Docelowo tablica dwuwymiarowa - w 1 kolumnie numer uszeregowania dla rodzica 1 w 2 kolumnie dla rodzica 2
    for i in range(0, pop): #Długość tablicy - długość populacji (Jeżeli populacja jest dl. 8 - wybierzemy 16 rodziców, aby potem na kniec miec 16 dzieci z których polowę odrzucimy na zasadzie selekcji)
      l1 = random.random() #Liczba losowa 1
      #Wybór rodzica na podstawie dystrybuanty
      for j in range(0,pop):
        if(l1 < times_sorted_rev[j][3]):
          which_parents.append([int((times_sorted_rev[j][0])),0])
          break
      l2 = random.random() #Liczba losowa 2
      #Wybór rodzica na podstawie dystrybuanty
      for j in range(0,pop):
        if(l2 < times_sorted_rev[j][3]):
          which_parents[i][1] = int(times_sorted_rev[j][0])
          #Jeżeli rodzic 2 jest taki sam jak rodzic 1 - ponawiamy wybór rodzica
          while(which_parents[i][1] == which_parents[i][0]):
            l2 = random.random() #Liczba losowa 2
            #Wybór rodzica na podstawie dystrybuanty
            for k in range(0,pop):
              if(l2 < times_sorted_rev[k][3]):
                which_parents[i][1] = int(times_sorted_rev[k][0])
                break
          break


    #Dodanie uszeregowań do tablicy parents:
    for i in range(0, pop):
      parents.append([population[which_parents[i][0]],population[which_parents[i][1]]])

    #ETAP 4 - Krzyżowanie (Metoda w zależności od wybranego parametru - "pmx", "ox")

    children = [] #tablica uzyskanych w trakcie krzyżowania potomków

    for i in range(0, pop):

      l_c = random.random() #losujemy liczbę losową z przedziału 0-1, jeżeli będzie ona mniejsza lub równa od prawdopodobieństwa krzyżowania - wykonujemy krzyżowanie, jeśli większa - rodzice przechodzą bez zmian do następnego pokolenia
      if(l_c < p_c):

        #Wykonujemy krzyżowanie

        if(method_c == "pmx"):

          #1) Technika PMX
          parent1 = parents[i][0]
          parent2 = parents[i][1]

          #2) Losujemy dwa punkty między którymi nic się zmieni: (drugi musi byc wiekszy od pierwszego)
          point1 = random.randrange(2, rows-10) #losujemy do rows-10 aby zostawić jakis rozsądny zapas na wylosowanie drugiego punktu
          point2 = random.randrange(point1+1, rows-2)  #Maksymalnie do 2 indexu od końca

          part0_p1 = parent1[point1:point2+1] #Czesc niezmienna z rodzica 1 - wycinamy tabelę do point2+1 aby liczyć również index do którego odzcinamy
          part0_p2 = parent2[point1:point2+1] #Czesc niezmienna z rodzica 2

          #Tworzymy mapę wymiany:
          map_w = []

          for i in range(point1,point2+1):
            map_w.append([parent1[i],parent2[i]])

          #Tworzenie potomków
          child1 = np.zeros(shape=(rows))
          child2 = np.zeros(shape=(rows))
          child1 = child1.astype(int)
          child2 = child2.astype(int)

          #Wymiana sekcji kojarzenia, dziecko 1 od rodzcica 2, dziecko 2 od rodzica 1
          j = 0
          for i in range(point1,point2+1):
            child1[i] = part0_p2[j]
            child2[i] = part0_p1[j]
            j+=1

          #Uzupełnienie reszty genów z rodziców (Dla dziecka 1 z rodzica 1, dla dziecka 2 z rodzica 2) - jeżeli wartość się powtórzy - używamy mapy wymiany

          #Potomek 1:
          for i in range(0,point1): #Uzupelnienie pierwszej pustej czesci
            task_to_check = parent1[i]
            use_map = 0
            for t in child1:
              if(task_to_check == t):
                use_map = 1
            if(use_map == 0):
              child1[i] = parent1[i] #Index sie nie powtarza - przepisujemy miasto z rodzica
            else:
              task_to_use = 0
              for position in map_w:
                if(task_to_check == position[1]):
                  task_to_use = position[0] #Numer miasta, które użyjemy zamiast tego, które się powtarza
                  break

              #Sprawdzamy czy miasto którego chcemy użyć też już nie występuje, jeśli tak - znowu używamy mapy wymiany
              check = 0
              while(check == 0):
                #Używamy mapy wymiany dopóki nie znajdzimey takiego miasta, które da się wstawić do ciągu
                check2 = 0
                for t in child1:
                  if(task_to_use == t):
                    check2 = 1
                if(check2 == 1):
                  task_to_check = task_to_use
                  task_to_use = 0
                  for position in map_w:
                    if(task_to_check == position[1]):
                      task_to_use = position[0]
                else:
                  check = 1

              if(check == 1):
                #Podmieniamy miasto na to z mapy wymiany
                for task2 in parent1:
                  if(task2 == task_to_use):
                    child1[i] = task2
                    break

          for i in range(point2+1,rows): #Uzupelnienie drugiej pustej czesci
            task_to_check = parent1[i]
            use_map = 0
            for t in child1:
              if(task_to_check == t):
                use_map = 1
            if(use_map == 0):
              child1[i] = parent1[i] #Index sie nie powtarza - przepisujemy miasto z rodzica
            else:
              task_to_use = 0
              for position in map_w:
                if(task_to_check == position[1]):
                  task_to_use = position[0] #Numer miasta, które użyjemy zamiast tego, które się powtarza
                  break

              #Sprawdzamy czy miasto którego chcemy użyć też już nie występuje, jeśli tak - znowu używamy mapy wymiany
              check = 0
              while(check == 0):
                #Używamy mapy wymiany dopóki nie znajdzimey takiego miasta, które da się wstawić do ciągu
                check2 = 0
                for t in child1:
                  if(task_to_use == t):
                    check2 = 1
                if(check2 == 1):
                  task_to_check = task_to_use
                  task_to_use = 0
                  for position in map_w:
                    if(task_to_check == position[1]):
                      task_to_use = position[0]
                else:
                  check = 1

              if(check == 1):
                #Podmieniamy miasto na to z mapy wymiany
                for task2 in parent1:
                  if(task2 == task_to_use):
                    child1[i] = task2
                    break

          #Potomek 2:
          for i in range(0,point1): #Uzupelnienie pierwszej pustej czesci
            task_to_check = parent2[i]
            use_map = 0
            for t in child2:
              if(task_to_check == t):
                use_map = 1
            if(use_map == 0):
              child2[i] = parent2[i] #Index sie nie powtarza - przepisujemy miasto z rodzica
            else:
              task_to_use = 0
              for position in map_w:
                if(task_to_check == position[0]):
                  task_to_use = position[1] #Numer miasta, które użyjemy zamiast tego, które się powtarza
                  break

              #Sprawdzamy czy miasto którego chcemy użyć też już nie występuje, jeśli tak - znowu używamy mapy wymiany
              check = 0
              while(check == 0):
                #Używamy mapy wymiany dopóki nie znajdzimey takiego miasta, które da się wstawić do ciągu
                check2 = 0
                for t in child2:
                  if(task_to_use == t):
                    check2 = 1
                if(check2 == 1):
                  task_to_check = task_to_use
                  task_to_use = 0
                  for position in map_w:
                    if(task_to_check == position[0]):
                      task_to_use = position[1]
                else:
                  check = 1

              if(check == 1):
                #Podmieniamy miasto na to z mapy wymiany
                for task2 in parent2:
                  if(task2 == task_to_use):
                    child2[i] = task2
                    break

          for i in range(point2+1,rows): #Uzupelnienie drugiej pustej czesci
            task_to_check = parent2[i]
            use_map = 0
            for t in child2:
              if(task_to_check == t):
                use_map = 1
            if(use_map == 0):
              child2[i] = parent2[i] #Index sie nie powtarza - przepisujemy miasto z rodzica
            else:
              task_to_use = 0
              for position in map_w:
                if(task_to_check == position[0]):
                  task_to_use = position[1] #Numer miasta, które użyjemy zamiast tego, które się powtarza
                  break

              #Sprawdzamy czy miasto którego chcemy użyć też już nie występuje, jeśli tak - znowu używamy mapy wymiany
              check = 0
              while(check == 0):
                #Używamy mapy wymiany dopóki nie znajdzimey takiego miasta, które da się wstawić do ciągu
                check2 = 0
                for t in child2:
                  if(task_to_use == t):
                    check2 = 1
                if(check2 == 1):
                  task_to_check = task_to_use
                  task_to_use = 0
                  for position in map_w:
                    if(task_to_check == position[0]):
                      task_to_use = position[1]
                else:
                  check = 1

              if(check == 1):
                #Podmieniamy miasto na to z mapy wymiany
                for task2 in parent2:
                  if(task2 == task_to_use):
                    child2[i] = task2
                    break

          #Jeżeli z jakiegoś powodu algorytm zadziała niepoprawnie i w utworzonych potomkach wystąpią powtórzenia algorytm przerwie działanie z komunikatem o tym, że wystąpił błąd
          if(np.unique(child1[:]).size != rows or np.unique(child1[:]).size != rows):
            print("Błąd - w zbiorze wystąpiły powtórzenia")
            print(child1, child2)
            print(np.unique(child1[:]).size, np.unique(child1[:]).size != rows)
            return false

          children.append(child1)
          children.append(child2)

        elif(method_c == "ox"):

          #3) Technika OX
          parent1 = parents[i][0]
          parent2 = parents[i][1]

          #2) Losujemy dwa punkty między którymi nic się zmieni: (drugi musi byc wiekszy od pierwszego)
          point1 = random.randrange(2, rows-10) #losujemy do rows-10 aby zostawić jakis rozsądny zapas na wylosowanie drugiego punktu
          point2 = random.randrange(point1+1, rows-2)  #Maksymalnie do 2 indexu od końca

          part0_p1 = parent1[point1:point2+1] #Czesc niezmienna z rodzica 1 - wycinamy tabelę do point2+1 aby liczyć również index do którego odzcinamy
          part0_p2 = parent2[point1:point2+1] #Czesc niezmienna z rodzica 2

          #Tworzenie potomków
          child1 = np.zeros(shape=(rows))
          child2 = np.zeros(shape=(rows))
          child1 = child1.astype(int)
          child2 = child2.astype(int)

          #Przepisujemy czesc niezmienna do potomkow
          j = 0
          for i in range(point1,point2+1):
            child1[i] = part0_p1[j]
            child2[i] = part0_p2[j]
            j+=1

          #Zaczynając od drugiego punktu przecięcia przeciecia przepisujemy miasta z innego rodzica - jesli sie powtorza pomijamy
          j = point2+1
          for i in range(point2+1,rows):
            check = 0
            while(check == 0): #Pętla będzie szukała miasta w rodzicu dopóki nie znajdzie takiego, które się nie powtarza
              if(j >= rows): #Zabezpieczenie aby nie przekroczyć indexu dla rodzica
                j = 0
              task_to_check = parent2[j]
              skip = 0
              for t in child1:
                if(task_to_check == t): #Jezeli dane miasto juz wystepuje - przechodzimy do nastepnego
                  j+=1
                  skip = 1
                  break

              if(skip == 0):
                check = 1

            child1[i] = parent2[j]

          #Przechodzimy do uzupelniania poczatku zachowujac index j dla rodzica
          for i in range(0,point1):
            check = 0
            while(check == 0): #Pętla będzie szukała miasta w rodzicu dopóki nie znajdzie takiego, które się nie powtarza
              if(j >= rows): #Zabezpieczenie aby nie przekroczyć indexu dla rodzica
                j = 0
              task_to_check = parent2[j]
              skip = 0
              for t in child1:
                if(task_to_check == t): #Jezeli dane miasto juz wystepuje - przechodzimy do nastepnego
                  j+=1
                  skip = 1
                  break

              if(skip == 0):
                check = 1

            child1[i] = parent2[j]

          #Powtarzamy procedurę dla dziecka nr 2:
          #Zaczynając od drugiego punktu przecięcia przeciecia przepisujemy miasta z innego rodzica - jesli sie powtorza pomijamy
          j = point2+1
          for i in range(point2+1,rows):
            check = 0
            while(check == 0): #Pętla będzie szukała miasta w rodzicu dopóki nie znajdzie takiego, które się nie powtarza
              if(j >= rows): #Zabezpieczenie aby nie przekroczyć indexu dla rodzica
                j = 0
              task_to_check = parent1[j]
              skip = 0
              for t in child2:
                if(task_to_check == t): #Jezeli dane miasto juz wystepuje - przechodzimy do nastepnego
                  j+=1
                  skip = 1
                  break

              if(skip == 0):
                check = 1

            child2[i] = parent1[j]

          #Przechodzimy do uzupelniania poczatku zachowujac index j dla rodzica
          for i in range(0,point1):
            check = 0
            while(check == 0): #Pętla będzie szukała miasta w rodzicu dopóki nie znajdzie takiego, które się nie powtarza
              if(j >= rows): #Zabezpieczenie aby nie przekroczyć indexu dla rodzica
                j = 0
              task_to_check = parent1[j]
              skip = 0
              for t in child2:
                if(task_to_check == t): #Jezeli dane miasto juz wystepuje - przechodzimy do nastepnego
                  j+=1
                  skip = 1
                  break

              if(skip == 0):
                check = 1

            child2[i] = parent1[j]

          children.append(child1)
          children.append(child2)
          #Jeżeli z jakiegoś powodu algorytm zadziała niepoprawnie i w utworzonych potomkach wystąpią powtórzenia algorytm przerwie działanie z komunikatem o tym, że wystąpił błąd
          if(np.unique(child1[:]).size != rows or np.unique(child1[:]).size != rows):
            print("Błąd - w zbiorze wystąpiły powtórzenia")
            print(child1, child2)
            print(np.unique(child1[:]).size, np.unique(child1[:]).size != rows)
            return false

        else:
          print("Błąd - podano zły parametr")
          return

      else:
        #Rodzice przechodzą do następnego pokolenia w niezmienionej formie
        children.append(parents[i][0])
        children.append(parents[i][1])

    #Po zakończeniu tego etapu mamy (populacja x 2) dzieci - tak abysmy mogli wybrac 50% najlepszych osobnikó do następnego pokolenia

    #ETAP 5 - Mutacje

    for x_mut in range(0,pop*2):
      l_m = random.random() #losujemy liczbę losową z przedziału 0-1, jeżeli będzie ona mniejsza lub równa od prawdopodobieństwa mutacji - wykonujemy losową mutację (zamianę dwóch zadań miejscami), jeśli większa - nie wykonujemy żadnej akcji
      if(l_m < p_m):

      #Następuje mutacja
        muted_child = np.copy(children[x_mut])
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
          #Zamiana miast miejscami
          task1 = np.copy(muted_child[ii1])
          muted_child[ii1] = np.copy(muted_child[ii2])
          muted_child[ii2] = task1
        else:
          #Wstawienie miast na indeks
          task1 = np.copy(muted_child[ii1])
          muted_child = list(muted_child)
          muted_child.pop(ii1)
          muted_child.insert(ii2, task1)

        children[x_mut] = muted_child

    #ETAP 6 - Selekcja pokolenia

    #Wybieramy połowę najlepszych osobników
    times = [] #Czasy realizacji zadań dla potomków
    index = 0
    for ind in children:
      ind = list(ind)
      times.append([index, sum_time(data_I, ind)])
      index+=1

    times_sorted = sorted(times, key=lambda x:x[1]) #Posortowanie według czasów od najmniejszego do największego
    times_new = times_sorted[0:pop]

    #średni czas dla nowo powstałej populacji:
    mean_te = np.mean(times_new, axis=0)
    mean_times_now= mean_te[1] #Średnia z drugiej kolumny tablicy times_new

    #Utworzenie nowej tablicy dla populacji
    population = []
    for index in times_new:
      population.append(children[index[0]]) #Do nowej populacji dodajemy te dzieci, ktore mialy najmniejszy czas realizacji zadań (Do konkretnego czasu przypisawono wczesniej index w tablicy children)

    #Sprawdzamy czy nastąpiła poprawa - Sprawdzamy to porównując średni czas uzyskany dla populacji wczesniejszej i nowej
    if(mean_times_now < mean_times_earlier):
       iterations_without_improvement = 0

    iterations_without_improvement+=1

  #Po wyjściu z pętli - podajemny najlepszy czas dla otrzymanej na koniec populacji
  times = [] #Czasy realizacji zadań dla osobników w populacji
  index = 0
  for ind in population:
    ind = list(ind)
    times.append([index, sum_time(data_I, ind)])
    index+=1

  times_sorted = sorted(times, key=lambda x:x[1]) #Posortowanie według czasów od najmniejszego do największego
  best_order_now = np.copy(population[times_sorted[0][0]]) #Najlepszy osobnik w obecnej populacji

  return best_order_now

#----------ALGORYTMY EWOLUCYJNE----------

#Tablice do przechowywania wyników
results_ea_I1 = []
results_ea_I2 = []
results_ea_I3 = []

#Tablice do przechowywania uszeregowań
results2_ea_I1 = []
results2_ea_I2 = []
results2_ea_I3 = []

print("   ")
print("Wyniki uzyskane dla algorytmu ewolucyjnego: ")

for i in range(0, 30):
  best_order = evolutionary(data_I1, order1, 500, 128, "ru", "ox", 0.9, 0.2, "l")
  best_order = list(best_order)
  results_ea_I1.append(sum_time(data_I1, best_order))
  results2_ea_I1.append(best_order)

  print(i)
  print(results_ea_I1)
  print("Minimalna ze znalezionych wartości: ", min(results_ea_I1))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ea_I1[results_ea_I1.index(min(results_ea_I1))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ea_I1))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ea_I1))

for i in range(0, 30):
  best_order = evolutionary(data_I2, order2, 500, 128, "ru", "ox", 0.9, 0.2, "l")
  best_order = list(best_order)
  results_ea_I2.append(sum_time(data_I2, best_order))
  results2_ea_I2.append(best_order)

  print(i)
  print(results_ea_I2)
  print("Minimalna ze znalezionych wartości: ", min(results_ea_I2))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ea_I2[results_ea_I2.index(min(results_ea_I2))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ea_I2))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ea_I2))

for i in range(0, 30):
  best_order = evolutionary(data_I3, order3, 500, 128, "rd", "ox", 0.9, 0.2, "l")
  best_order = list(best_order)
  results_ea_I3.append(sum_time(data_I3, best_order))
  results2_ea_I3.append(best_order)

  print(i)
  print(results_ea_I3)
  print("Minimalna ze znalezionych wartości: ", min(results_ea_I3))
  print("Uszeregowanie dla najmniejszej ze znalezionych wartości: ", results2_ea_I3[results_ea_I3.index(min(results_ea_I3))])
  print("Maksymalna ze znalezionych wartości: ", max(results_ea_I3))
  print("Srednia ze znalezionych wartości: ", np.mean(results_ea_I3))
