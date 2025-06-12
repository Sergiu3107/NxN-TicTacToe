
# Tic-Tac-Toe

## Descrierea generală a proiectului

Acest proiect implementează un joc Tic-Tac-Toe interactiv cu un algoritm AI performant folosind Python și Pygame. AI-ul folosește o combinație de tehnici avansate de căutare pentru a lua cele mai bune decizii, inclusiv **Alpha-Beta Pruning**, **Iterative Deepening**, și **Heuristica Istoricului**. Proiectul permite jucătorului să joace împotriva AI-ului pe o tablă de dimensiuni personalizabile și cu o condiție de câștig variabilă.

**Algoritmul AI** încearcă să joace optim, evaluând fiecare stare posibilă a jocului folosind un **funcție de evaluare** care atribuie un scor fiecărei configurații de pe tablă. Pe lângă asta, AI-ul implementează tehnici de optimizare precum **Transposition Table** pentru a economisi resursele de calcul și a evita evaluarea repetată a aceleași stări.

## Explicarea algoritmilor folosiți și motivația alegerii acestora

### 1. **Alpha-Beta Pruning**

**Alpha-Beta Pruning** este o optimizare a algoritmului **Minimax** care reduce semnificativ numărul de noduri evaluate în arborii de decizie. Prin evaluarea în adâncime a posibilităților, Alpha-Beta pruning permite „tăierea” unor ramuri ale arborelui de decizie care nu vor afecta rezultatul final, economisind astfel timp și resurse de calcul. Aceasta este tehnica principală folosită pentru a determina cea mai bună mișcare a AI-ului și pentru a reduce complexitatea căutării.

În jocuri cu mai multe opțiuni și mai multe stări, minimizarea numărului de noduri evaluate este esențială pentru a asigura performanța AI-ului într-un interval de timp rezonabil.


### 2. **Iterative Deepening**

**Iterative Deepening** este o tehnică combinată între **Depth-First Search (DFS)** și **Breadth-First Search (BFS)** care îmbină avantajele ambelor metode, adâncind căutarea pe măsură ce trece timpul disponibil. Ideea este că AI-ul va căuta mai întâi la o adâncire foarte mică (de exemplu, adâncirea 1), și, dacă timpul permite, va crește adâncimea treptat până când ajunge la limita maximă stabilită pentru căutare.

În implementarea noastră, **Iterative Deepening** este utilizată pentru a ajuta AI-ul să ia decizii într-un timp limitat. În loc ca AI-ul să caute profund într-un arbore de decizie foarte adânc și să rămână blocat în căutarea unei mutări perfecte, aceasta se bazează pe evaluarea succesivă a posibilelor mișcări pe fiecare nivel de adâncire.

1.  **Inițierea căutării la adâncire mică**: Algoritmul începe printr-o căutare pe adâncimea 1 (evaluând doar mutările directe ale AI-ului și ale jucătorului).
    
2.  **Creșterea adâncimii**: După fiecare iterație, adâncimea căutării este mărită cu 1 (adâncire 2, adâncire 3 și așa mai departe).
    
3.  **Decizie bazată pe cele mai bune mutări găsite până acum**: Dacă AI-ul se află într-o situație de timp limitat, el va lua cea mai bună mutare găsită până la acel moment.
    

Implementarea în cod presupune că în cadrul funcției `iterative_deepening`, se efectuează mai multe iterații de căutare folosind funcția `alpha_beta`. În fiecare iterație, se mărește adâncimea maximă de căutare până când timpul impus de `TIME_LIMIT` este depășit. Astfel, chiar dacă timpul este limitat, AI-ul poate alege cea mai bună mutare disponibilă pe baza căutărilor anterioare.



```py 
def iterative_deepening(self, depth_limit):
    best_move = None
    start_time = time.time()

    for depth in range(1, depth_limit + 1):
        self.node_count = 0
        score, move = self.alpha_beta(self.game.board, depth, -float('inf'), float('inf'), True, start_time)
        
        # If the time limit is exceeded, break the loop
        if time.time() - start_time > TIME_LIMIT:
            break
        best_move = move
    return best_move
   ```

### 3. **Heuristica Istoricului**

**Heuristica Istoricului** este o tehnică utilizată pentru a îmbunătăți performanța căutării, ordonând mutările în funcție de frecvența lor în iterațiile anterioare. Aceasta ajută la accelerarea procesului de căutare, prioritizând mutările care au fost deja explorate și care au avut un impact semnificativ asupra deciziilor anterioare.

În fiecare iterație a funcției `alpha_beta`, mutările posibile sunt ordonate pe baza unui tabel de istoric, care stochează informații despre frecvența cu care anumite mutări au fost explorate. Algoritmul `alpha_beta` va căuta mutările cele mai frecvente întâi, ceea ce poate reduce semnificativ timpul de căutare, mai ales în cazurile în care există un număr mare de mutări posibile.

Aceasta se implementează printr-o funcție de sortare a mutărilor pe baza valorii stocate în tabelul `history_table`. Acest tabel este actualizat pe parcursul jocului, iar mutările cele mai relevante sunt prioritizate pentru a le evalua mai întâi.

```py
moves.sort(key=lambda move: self.history_table.get(move, 0), reverse=True)
``` 

Prin această abordare, algoritmul învață și devine mai eficient pe măsură ce jocul progresează, pentru că mutările care au fost evaluate anterior ca fiind promițătoare vor fi verificate mai întâi în următoarele iterații.

### 4. **Transposition Table**

Un **Transposition Table** este o structură de date folosită pentru a salva stările de joc care au fost deja evaluate. Un transpoziție este o stare de joc care poate fi atinsă printr-o secvență diferită de mutări. De exemplu, aceeași configurație de pe tablă poate apărea în joc printr-o serie diferită de mutări, iar utilizarea unui transpozițion table ajută la evitarea recalculării aceleași stări de mai multe ori.

În cadrul funcției `alpha_beta`, înainte de a evalua o stare, algoritmul verifică mai întâi dacă acea stare a fost deja evaluată folosind `transposition_table`. Dacă da, folosește rezultatul stocat în loc să refacă evaluarea. Aceasta economisește o cantitate semnificativă de resurse de calcul.

Transposition Table este un dicționar unde cheia este o reprezentare unică a stării curente a jocului și valoarea este rezultatul evaluării pentru acea stare.

```py
if state_str in self.transposition_table:
    return self.transposition_table[state_str]
   ``` 

După evaluarea stării curente, această valoare este stocată în tabel pentru a fi reutilizată mai târziu.

### 5. **Funcția de Evaluare**

Funcția de evaluare este responsabilă pentru atribuirea unui scor fiecărei stări de joc, ajutând AI-ul să decidă dacă o anumită stare este favorabilă sau nu. Scorul poate fi pozitiv (avantaj AI), negativ (avantaj jucătorului) sau 0 (egalitate). Funcția de evaluare analizează liniile de pe tablă (rânduri, coloane și diagonale) și atribuie un scor în funcție de câte simboluri consecutive ale jucătorului sau ale AI-ului sunt prezente.

În implementarea noastră, funcția de evaluare analizează toate liniile de pe tablă, incluzând rândurile, coloanele și diagonalele. Fiecare linie este evaluată în funcție de numărul de simboluri consecutive ale fiecărui jucător. De exemplu, o linie cu două simboluri consecutive ale AI-ului și un spațiu liber va avea un scor pozitiv, în timp ce o linie cu două simboluri consecutive ale jucătorului va avea un scor negativ.

Funcția de evaluare utilizează aceste scoruri pentru a ajuta la determinarea celei mai bune mutări. În cazul în care AI-ul poate forma o linie câștigătoare, scorul va fi maxim (pozitiv), iar în cazul în care jucătorul riscă să câștige, scorul va fi minim (negativ).

```py
`def evaluate_line(self, line):
    player_count = np.sum(line == 1)
    ai_count = np.sum(line == -1)
    if player_count > 0 and ai_count > 0:
        return 0  # Mixed line (no advantage)
    elif player_count > 0:
        return -10 ** player_count  # Player advantage
    elif ai_count > 0:
        return 10 ** ai_count  # AI advantage
    return 0
   ``` 

Funcția de evaluare este esențială pentru luarea deciziilor corecte și pentru optimizarea performanței AI-ului, deoarece aceasta determină importanța fiecărei mutări și ajută la orientarea căutării spre cele mai promițătoare opțiuni.


## Rezultate testelor (performanța algoritmului)

Am efectuat teste cu diverse dimensiuni de tablă și condiții de câștig pentru a evalua performanța AI-ului:

- **Pentru tabele de 3x3** cu condiție de câștig 3, algoritmul AI folosește eficient Alpha-Beta Pruning și Iterative Deepening pentru a lua decizii rapid (în aproximativ 0.01 secunde pe mutare, în funcție de complexitatea jocului).
- **Pentru tabele de 5x5** cu condiție de câștig 4, performanța scade ușor, dar AI-ul poate găsi mutări bune în aproximativ 0.1-0.2 secunde, datorită optimizărilor realizate prin Transposition Table și Heuristica Istoricului.

În general, algoritmul funcționează eficient chiar și pentru tabele de dimensiuni mai mari, precum **15x15** cu condiție de câștig 5, dar în acest caz încep să apară întârzieri semnificative în alegerea unei mișcări. Cu cât tabla este mai mare, cu atât mai mult crește timpul necesar pentru evaluarea și selectarea mutărilor optime, datorită complexității crescute a arborelui de decizie. Totuși, algoritmul rămâne competitiv și poate fi utilizat pentru jocuri la o scară mare, chiar dacă performanța scade ușor pe tabele mai mari.



## Instrucțiuni pentru rularea codului

### Prerechizite:
1. Asigurați-vă că aveți **Python 3.x** instalat pe sistemul dumneavoastră.
2. Instalați biblioteca **Pygame** utilizând pip:
 - Deschideți terminalul sau linia de comandă și rulați comanda:
 ```bash
     pip install pygame
     pip install numpy
```
### Rularea jocului:
1. Descărcați sau clonați repository-ul pe mașina dumneavoastră locală.
2. Deschideți terminalul sau linia de comandă și navigați în directorul proiectului.
3. Rulați scriptul principal al jocului cu comanda:
   ```bash
   python main.py 
   ```

4.  La începutul jocului, vi se va cere să alegeți următoarele:
    
    -   **Dimensiunea tablei** (de exemplu 3 pentru o tablă de 3x3, 4 pentru 4x4, etc.)
    -   **Condiția de câștig** (numărul de simboluri consecutive necesare pentru a câștiga, de obicei 3).
5.  După ce ați ales aceste opțiuni, jocul va începe automat. Jucătorul va controla jocul utilizând mouse-ul, iar AI-ul va face mutările sale în funcție de algoritmul implementat.
    
6.  Jocul continuă până când un jucător câștigă sau tabla este completă. În cazul unei victorii, AI-ul sau jucătorul va fi declarat câștigător și jocul se va încheia.
    

### Control:

-   **Jucătorul** interacționează cu jocul prin **mouse** pentru a plasa simbolurile pe tablă.
-   **AI-ul** va lua decizii automat, folosind algoritmii implementați pentru a evalua cele mai bune mutări.

## Bibliografie

1. **Minimax și Alpha-Beta Pruning**  
   - "Minimax Algorithm", [Wikipedia](https://en.wikipedia.org/wiki/Minimax)  
   - "Alpha-Beta Pruning", [Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)  
   

2. **Tic-Tac-Toe**  
   - "How to build a Tic-Tac-Toe AI in Python", [Real Python](https://realpython.com/python-tic-tac-toe/)  
   - "How to Play Tic-Tac-Toe on a 5x5 grid", [StackExchange](https://boardgames.stackexchange.com/questions/41410/how-to-play-tic-tac-toe-on-a-5x5-grid)

3. **Pygame**  
   - "Pygame Documentation", [Pygame](https://www.pygame.org/docs/)  

4. **Algoritmi pentru AI în Tic-Tac-Toe (5x5)**  
   - "Best algorithm for 5x5 Tic-Tac-Toe AI using 4 in a row", [StackOverflow](https://stackoverflow.com/questions/41135751/best-algorithm-for-5x5-tictactoe-ai-using-4-in-a-row)
