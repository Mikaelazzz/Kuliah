pola = []

x = input("Node ke 1 :")
y = input("Node ke 2 :")

pola.append([x,y])
for x,y in pola:
    print(f"Edge dari {x} ke {y}")
    print(str(x) + " -> " + str(y))

