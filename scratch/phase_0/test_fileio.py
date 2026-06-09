import csv

personasCampet = []

with open("csvfile.csv") as file: 
    reader = csv.DictReader(file) #importante el modo dictReader, en la que la priemra linea son las keys y las siguientes las values. 
    for row in reader: 
        #name, home = row
        #personaCampet = {"name": name, "home": home}
        personasCampet.append(row) #ó (personaCampet)

for personaCampet in sorted(personasCampet, key=lambda personaCampet: personaCampet["name"]): 
    print(f"{personaCampet["name"]} is in {personaCampet["home"]}")
