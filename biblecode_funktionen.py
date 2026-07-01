import pandas
import numpy
import matplotlib.pyplot
import random

hebraeisch_liste = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "ך", "כ", "ל", "ם", "מ", "ן", "נ", "ס", "ע", "ף", "פ", "ץ", "צ", "ק", "ר", "ש", "ת"]
mappung = {char: i for i, char in enumerate(hebraeisch_liste)}

def kodieren(text):
    """Verschlüsselt den gegebenen Text basierend auf der bereitgestellten Mappung."""
    return [mappung.get(char, char) for char in text]

def dekodieren(verschluesselt):
    """Entschlüsselt den verschlüsselten Text basierend auf der bereitgestellten Zeichenliste."""
    text = []
    for zahl in verschluesselt:
        if isinstance(zahl, int):
            text.append(hebraeisch_liste[zahl])
    return text

def bibeltext_besorgen(dateipfad):
    tabelle = pandas.read_csv(dateipfad)
    spaltenlänge = len(tabelle["Text"])
    
    bibelverse = []
    for i in range(spaltenlänge):
        vers_name = tabelle.at[i, "Bibelvers"]
        bibelverse = bibelverse + [vers_name]
    
    genesis_verse = []
    for i in range(spaltenlänge):
        vers = tabelle.at[i, "Text"]
        genesis_verse = genesis_verse + [vers]
    
    buchstabenliste = []
    position_liste = []
    for a in range(len(bibelverse)):
        for b in range(len(genesis_verse[a])):
            if genesis_verse[a][b] != " ":
                buchstabenliste.append(genesis_verse[a][b])
                position_liste.append(bibelverse[a])
    return buchstabenliste, position_liste

def suche_els(buchstabenliste, suchwort, skips):
    suchbereich = len(buchstabenliste) #buchstaben

    els_liste = []
    for start in range(suchbereich): 
        for skip in skips:
            current_word = "" 
            for letter in range(len(suchwort)):
                bereinigte_position = (start + skip * letter) % suchbereich #Der Index darf nicht zu groß werden. Wenn ein Wort am Ende des Textes noch nicht fertig ist, sucht man am Anfang danach weiter
                current_letter = buchstabenliste[bereinigte_position]
                current_word = current_word + current_letter #Das Wort wird Buchstabe für Buchstabe zusammengesetzt
            if current_word == suchwort: #Wenn das konstruierte Wort das Suchwort ist, wird es zur Sequences Liste hinzugefügt
                els = [start, len(suchwort), skip]
                els_liste.append(els)
    return els_liste

def lese_els(els, buchstabenliste, position_liste):
    #els = [start, length, skip]
    start = els[0]
    length = els[1]
    skip = els[2]
    vers = position_liste[start]

    wort = ""
    for letter in range(length):
        position = start+letter*skip
        wort += buchstabenliste[position]
    return [vers, wort]
    
def plot_text(focused_text, marked, rows, lines, position):
    matplotlib.pyplot.figure(figsize=(15,10))
    for y in range(lines):
        for x in range(rows):
            matplotlib.pyplot.text(rows-x, lines-y , focused_text[rows*y+x],fontsize=12, fontweight="bold")
            c = 1
            for marker in marked:
                if marker[position+(rows*y)+x] == 1:
                    matplotlib.pyplot.gca().add_artist(matplotlib.pyplot.Circle((rows-x+0.2, lines-y+0.2), radius=0.5, linewidth= 2.5, fill=False, color = matplotlib.cm.get_cmap("tab20")(1/20*c-0.01)))
                if marker[position+(rows*y)+x] == 2:
                    matplotlib.pyplot.gca().add_artist(matplotlib.pyplot.Circle((rows-x+0.2, lines-y+0.2), radius=0.5, linewidth= 2.5, fill=False, color = "r"))
                c += 1
    
    matplotlib.pyplot.xticks(range(rows + 2),range(rows + 2))
    matplotlib.pyplot.yticks(range(lines + 2),range(lines + 2))
    matplotlib.pyplot.show()

def display_matrix(text, position_liste, anchor_els, andere_els, shift, top_space, right_space):
    kodierter_text=kodieren("".join(text))
    max_rows = 40
    lines = 30
    miss_out = 0
    rows = (numpy.abs(anchor_els[2])-shift)
    if rows > max_rows: #anzahl der spalten begrenzen
        rows = max_rows
    elss = [anchor_els] + andere_els
    markers = []
    #print(elss)
    for els in elss:
        #els = [start, length, skip]
        start = els[0]
        length = els[1]
        skip = els[2]
        
        marked = [0]*len(text) #umkreisen der gefundenen buchstaben
        for letter in range(length):
            marked[start+letter*skip] = 1
        marked[0] = 2
        markers = markers + [marked]
            
    focused_text = [] #die angezeigten buchstaben filtern
    start_index = anchor_els[0] - (right_space + rows*top_space)
    end_index = start_index + (rows * (lines + 1)) 
    focused_text = kodierter_text[start_index:end_index] if start_index >= 0 else kodierter_text[start_index:]+kodierter_text[:end_index]
    
    if shift >= numpy.abs(anchor_els[2]):
        print("Achtung: Der Shift darf nicht größer/gleich dem Skip des ELS sein!!!")

    plot_text(dekodieren(focused_text), markers, rows, lines, start_index)
    print("Anzeige von Buchstabe " + str(start_index) + " bis " + str(end_index))
    print(lese_els(anchor_els, text, position_liste))

def letter_position(place, columns):
    x = place%columns
    y = divmod(place, columns)[0]
    return [x, y]

def els_position(els, columns):
    position = []
    start = els[0]
    length = els[1]
    skip = els[2]
    for letter in range(length):
        place = start + letter*skip
        position.append(letter_position(place, columns))
    return position

def letter_distance(pos_letter1, pos_letter2, columns):
    d_x1 = numpy.abs(pos_letter1[0]-pos_letter2[0])
    d_x2 = columns - d_x1
    d_y = numpy.abs(pos_letter1[1]-pos_letter2[1])
    a = numpy.sqrt(numpy.square(d_x1)+numpy.square(d_y))
    b = numpy.sqrt(numpy.square(d_x2)+numpy.square(d_y))
    d = min(a, b)
    return d
    
def els_distance(els1, els2, columns):
    #poisionen der buchstaben berechnen
    pos_els1 = els_position(els1, columns)
    pos_els2 = els_position(els2, columns)
    #entfernungen berechnen
    #minimale distanz von zwei buchstaben der verschiedenen wörter
    letter_distances = numpy.empty((len(pos_els1),len(pos_els2)))
    for letter1 in range(len(pos_els1)):
        for letter2 in range(len(pos_els2)):
            letter_distances[letter1, letter2] = letter_distance(pos_els1[letter1], pos_els2[letter2], columns) #die abstände zwischen allen buchstaben werden in einem array dargestellt
    l = numpy.min(letter_distances) #der kleinste abstand wird ausgewählt
    #distancen der einzelnen buchstaben im wort
    f = letter_distance(pos_els1[0], pos_els1[1], columns)
    f_strich = letter_distance(pos_els2[0], pos_els2[1], columns)
    return numpy.square(f) + numpy.square(f_strich) + numpy.square(l)

def maximum_compactness(els1, els2):
    skip1 = els1[2]
    skip2 = els2[2]
    compactness = 0
    
    for i in range(1, 10):
        h_i = numpy.round(numpy.abs(skip1)/i)
        if h_i < 1:
            h_i = 1
        mü_hi = 1/els_distance(els1, els2, h_i)
        compactness += mü_hi

    for i in range(1, 10):
        h_strich_i = numpy.round(numpy.abs(skip2)/i)
        if h_strich_i < 1:
            h_strich_i = 1
        mü_hstrichi = 1/els_distance(els1, els2, h_strich_i)
        compactness += mü_hstrichi

    return compactness

def berechne_nähe(els1, els2):
    compactnesses = numpy.empty((len(els1),len(els2)))
    for word1 in range(len(els1)):
        for word2 in range(len(els2)):
            compactnesses[word1, word2] = maximum_compactness(els1[word1], els2[word2])
    return compactnesses

def kompakteste_funde(els1, els2, compactnesses, n):
    max_pairs = []
    for max in range(n):
        maximum = numpy.argmax(compactnesses)
        max_position = [divmod(maximum, len(els2))[0], maximum%len(els2)]
        max_pairs.append([els1[max_position[0]], els2[max_position[1]], compactnesses[max_position[0], max_position[1]]])
        compactnesses[max_position[0],max_position[1]] = 0
    return max_pairs

def random_text(length):
    kodiert = []
    positionen = []
    for letter in range(length):
        zahl = random.randint(0, 26)
        kodiert.append(zahl)
        positionen.append(letter)
    text = dekodieren(kodiert)
    return text, positionen

def lese_txt(dateiname):
    buchstaben_liste = []
    positionen = []
    
    # Bereinigte Datei lesen
    with open(dateiname, 'r', encoding='utf-8') as file:
        bereinigter_inhalt = file.read()
    
    # Buchstaben in die Liste hinzufügen
    for letter in range(len(bereinigter_inhalt)):
        buchstaben_liste.append(bereinigter_inhalt[letter]) 
        positionen.append(letter)
          
    # Ausgabe der Buchstabenliste (optional)
    return buchstaben_liste, positionen

def text_laden(name):
    if name == "G":
        buchstabenliste, position_liste = bibeltext_besorgen("Genesis.csv")
    elif name == "E":
        buchstabenliste, position_liste = bibeltext_besorgen("Exodus.csv")
    elif name == "R":
        buchstabenliste, position_liste = random_text(78177) #länge von Genesis
    elif name == "B":
        buchstabenliste, position_liste = lese_txt("Ben_Sira_Bereinigt.txt")
    elif name == "T":
        buchstabenliste, position_liste = lese_txt("Talmund_Shabbat_Bereinigt.txt")
    else:
        buchstabenliste, position_liste = [],[]
    return buchstabenliste, position_liste

wortpaare = [
    ["כוכבים", "שמים"],
    ["ירח", "שמש"],
    ["אדמה", "מים"],
    ["חושך", "אור"],
    ["אשה", "אדם"],
    ["ילדה", "ילד"],
    ["צמח", "פרי"],
    ["ברק", "גזר"],
    ["כפרה", "תקווה"],
    ["עיר", "כפר"],
    ["תפוח", "בננה"],
    ["מגדל", "קיר"],
    ["שדה", "מזרע"],
    ["גבעה", "פסגה"],
    ["פרח", "עלה"],
    ["שולחן", "כסא"],
    ["מטבח", "חדר"],
    ["תיק", "מכנסיים"]
]
wortpaare_de = [
    ["Sterne", "Himmel"],
    ["Mond", "Sonne"],
    ["Erde", "Wasser"],
    ["Dunkelheit", "Licht"],
    ["Frau", "Mann"],
    ["Mädchen", "Junge"],
    ["Pflanze", "Frucht"],
    ["Blitz", "Karotte"],
    ["Versöhnung", "Hoffnung"],
    ["Stadt", "Dorf"],
    ["Apfel", "Banane"],
    ["Turm", "Wand"],
    ["Feld", "Samen"],
    ["Hügel", "Gipfel"],
    ["Blume", "Blatt"],
    ["Tisch", "Stuhl"],
    ["Küche", "Raum"],
    ["Tasche", "Hose"]
]

nicht_passende_wortpaare = [
    ["כוכבים", "מכנסיים"],
    ["ירח", "מזרע"],
    ["אדמה", "כסא"],
    ["חושך", "בננה"],
    ["אשה", "שולחן"],
    ["ילדה", "תיק"],
    ["צמח", "תקווה"],
    ["ברק", "פסגה"],
    ["כפרה", "עלה"],
    ["עיר", "קיר"],
    ["תפוח", "חדר"],
    ["מגדל", "שדה"],
    ["שדה", "כוכבים"],
    ["גבעה", "שולחן"],
    ["פרח", "מכנסיים"],
    ["שולחן", "פרי"],
    ["מטבח", "כפר"],
    ["תיק", "מגדל"]
]

nicht_passende_wortpaare_de = [
    ["Sterne", "Hose"],          
    ["Mond", "Samen"],          
    ["Erde", "Stuhl"],            
    ["Dunkelheit", "Banane"],     
    ["Frau", "Tisch"],            
    ["Mädchen", "Tasche"],       
    ["Pflanze", "Hoffnung"],      
    ["Blitz", "Gipfel"],        
    ["Versöhnung", "Blatt"],   
    ["Stadt", "Tisch"],         
    ["Apfel", "Raum"],        
    ["Turm", "Himmel"],          
    ["Feld", "Sterne"],         
    ["Hügel", "Tisch"],          
    ["Blume", "Hose"],          
    ["Tisch", "Frucht"],         
    ["Küche", "Stuhl"],        
    ["Tasche", "Feld"]           
]

def werte_wortpaare_aus(text, wortpaare, skips):
    buchstabenliste, position_liste = text_laden(text) #G, E, R, B, T
    nähe_karten = []
    jeweilige_funde = []
    for paar in range(len(wortpaare)):
        print("Werte Paar " + str(paar+1) + " von " + str(len(wortpaare)) + " aus.")
        suchwort1 = wortpaare[paar][0]
        suchwort2 = wortpaare[paar][1]
        els1 = suche_els(buchstabenliste, suchwort1, skips)
        print("Wort 1 hat " + str(len(els1))+ " Funde")
        els2 = suche_els(buchstabenliste, suchwort2, skips)
        print("Wort 2 hat " + str(len(els2))+ " Funde")

        if len(els1)*len(els2) >= 10:
            print("Berechne Nähe der Wörter...")
            nähe = berechne_nähe(els1,els2)
            nähe_karten.append(nähe)
            signifikante_funde = kompakteste_funde(els1, els2, nähe, 10)
            jeweilige_funde.append(signifikante_funde)
        else:
            nähe_karten.append([])
            jeweilige_funde.append([])

    return nähe_karten, jeweilige_funde