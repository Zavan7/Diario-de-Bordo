import re

def gerador_tuplas():
    print("Digite valores, um por linha. Para terminar, aperte ENTER em uma linha vazia.")
    valores = []
    while True:
        linha = input()
        if linha == "":
            break
        limpo = re.sub(r'[^a-zA-Z0-9 ]', '', linha)
        limpo = ' '.join(limpo.split())
        valores.append(limpo)
    
    return "(" + ", ".join(f"'{v}'" for v in valores) + ")"

print(gerador_tuplas())
