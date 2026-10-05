poke_type = input("Type (Fire, Water, Grass, Electric): ").lower()
letter = input("First letter of the name: ").upper()

if poke_type == "water" and letter == "S":
    print("Squirtle")
elif poke_type == "water" and letter == "T":
    print("Tentacool")
elif poke_type == "fire" and letter == "C":
    print("Charmander")
elif poke_type == "fire" and letter == "M":
    print("Moltres")
elif poke_type == "grass" and letter == "B":
    print("Bulbasaur")
elif poke_type == "grass" and letter == "O":
    print("Oddish")
elif poke_type == "electric" and letter == "P":
    print("Pikachu")
elif poke_type == "electric" and letter == "V":
    print("Voltorb")
else:
    print("No suggestions")
