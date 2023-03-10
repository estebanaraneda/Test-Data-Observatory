import math


def PatenteaID(Patente):
    Letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    ListaP = list(Patente)
    Numeros = []
    i = 0
    while i < len(ListaP) - 3:
        Numero = 0
        j = 0
        while j < len(Letras):
            if ListaP[i] == Letras[j]:
                Numero = j
            j = j + 1
        Numeros.append(Numero)
        i = i + 1
    i = len(ListaP) - 3
    while i >= len(ListaP) - 3 and i < len(ListaP):
        Numeros.append(ListaP[i])
        i = i + 1
    ID = 1
    i = 0
    while i < len(Numeros) - 4:
        ID = ID + int(Numeros[i]) * (26**(len(Numeros) - i - 1))
        i = i + 1
    while i >= len(Numeros) - 4 and i < len(Numeros):
        ID = ID + int(Numeros[i]) * (10**(len(Numeros) - i - 1))
        i = i + 1

    return ID


def IDaPatente(ID):
    Letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if ID >= 1000:
        ID = ID - 1

    LetrasN = math.trunc(ID / 1000)
    Numeros = str(ID)[-3:]
    if ID < 10:
        Numeros = str(0) + str(0) + Numeros
    elif ID < 100:
        Numeros = str(0) + Numeros

    Lista = []
    i = 1
    while i <= 4:
        Lista.append(LetrasN % 27)
        LetrasN = math.trunc(LetrasN / 27)
        i = i + 1

    j = 0
    while j < len(Lista):
        Lista[j] = Letras[Lista[j]]
        j = j + 1

    Patente = ''.join(reversed(Lista)) + str(Numeros)

    return Patente


print(IDaPatente(1001))
print(PatenteaID('AAAB000'))
print(IDaPatente(26000))
print(PatenteaID('AAAZ999'))
