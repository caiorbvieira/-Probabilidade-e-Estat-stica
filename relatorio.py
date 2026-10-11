import statistics
import math
import csv

print("=" * 55)
print("ANALISADOR ESTATÍSTICO - ENGENHARIA DE SOFTWARE")
print("=" * 55)

print("[1] Digitar os dados")
print("[2] Carregar arquivo CSV")

opcao = input("Escolha uma opção: ")

dados = []

if opcao == "1":
    entrada = input("Digite os valores separados por vírgula: ")

    try:
        dados = [float(x.strip()) for x in entrada.split(",")]
    except:
        print("Algum valor foi digitado errado.")
        exit()

elif opcao == "2":
    nome = input("Digite o nome/caminho do arquivo CSV: ")

    try:
        with open(nome, "r", encoding="utf-8-sig") as arquivo:
            leitor = csv.reader(arquivo)

            for linha in leitor:
                for valor in linha:
                    try:
                        dados.append(float(valor))
                    except:
                        pass

        print(f"Arquivo carregado com sucesso! ({len(dados)} valores)")

    except:
        print("Não foi possível abrir o arquivo.")
        exit()

else:
    print("Opção inválida.")
    exit()


if len(dados) == 0:
    print("Nenhum dado encontrado.")
    exit()


# PARTE 1

print("\n" + "-" * 55)
print("PARTE 1 - DADOS NÃO AGRUPADOS")
print("-" * 55)

media = statistics.mean(dados)
mediana = statistics.median(dados)
moda = statistics.mode(dados)

print(f"Média: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda:.2f}")


# PARTE 2

print("\n" + "-" * 55)
print("PARTE 2 - DADOS AGRUPADOS SEM INTERVALO")
print("-" * 55)

frequencias = {}

for numero in dados:
    if numero in frequencias:
        frequencias[numero] += 1
    else:
        frequencias[numero] = 1

valores = sorted(frequencias)

print("Valor (xi) | fi | Fi")

acumulada = 0
soma = 0

for valor in valores:
    fi = frequencias[valor]
    acumulada += fi

    print(f"{valor:.2f}      | {fi}  | {acumulada}")

    soma += valor * fi

media2 = soma / len(dados)

maior_freq = max(frequencias.values())

modas = []

for valor in valores:
    if frequencias[valor] == maior_freq:
        modas.append(valor)


# mediana usando a tabela

n = len(dados)

def achar_valor(posicao):
    acumulada = 0

    for valor in valores:
        acumulada += frequencias[valor]

        if acumulada >= posicao:
            return valor


if n % 2 == 0:
    valor1 = achar_valor(n / 2)
    valor2 = achar_valor((n / 2) + 1)

    mediana2 = (valor1 + valor2) / 2

else:
    mediana2 = achar_valor((n + 1) / 2)


print("\nResultados pela tabela:")
print(f"Média: {media2:.2f}")
print(f"Mediana: {mediana2:.2f}")

if len(modas) == 1:
    print(f"Moda: {modas[0]:.2f}")
else:
    print("Modas:", modas)


# PARTE 3

print("\n" + "-" * 55)
print("PARTE 3 - DADOS AGRUPADOS COM INTERVALO")
print("-" * 55)

n = len(dados)

menor = min(dados)
maior = max(dados)

# fórmula de Sturges
k = math.ceil(1 + 3.322 * math.log10(n))

amplitude_total = maior - menor
h = amplitude_total / k

print(f"Número de classes: {k}")
print(f"Amplitude de cada classe: {h:.2f}\n")

classes = []

inicio = menor

for i in range(k):

    fim = inicio + h

    classe = {
        "inicio": inicio,
        "fim": fim,
        "fi": 0,
        "Fi": 0
    }

    classes.append(classe)

    inicio = fim


# frequência das classes

for numero in dados:

    for i in range(len(classes)):

        inicio = classes[i]["inicio"]
        fim = classes[i]["fim"]

        if i == len(classes) - 1:

            if numero >= inicio and numero <= fim:
                classes[i]["fi"] += 1
                break

        else:

            if numero >= inicio and numero < fim:
                classes[i]["fi"] += 1
                break


acumulada = 0

print("Classe                 | fi | Fi")

for classe in classes:

    acumulada += classe["fi"]
    classe["Fi"] = acumulada

    print(
        f"[{classe['inicio']:.2f} - {classe['fim']:.2f})"
        f" | {classe['fi']} | {classe['Fi']}"
    )


# média agrupada

soma = 0

for classe in classes:

    ponto_medio = (classe["inicio"] + classe["fim"]) / 2

    soma += ponto_medio * classe["fi"]

media3 = soma / n


# mediana agrupada

posicao_mediana = n / 2

freq_anterior = 0
mediana3 = 0

for classe in classes:

    if classe["Fi"] >= posicao_mediana:

        li = classe["inicio"]
        fi = classe["fi"]

        mediana3 = li + ((posicao_mediana - freq_anterior) / fi) * h

        break

    freq_anterior = classe["Fi"]


# moda pelo método de Czuber

maior_frequencia = 0
indice_modal = 0

for i in range(len(classes)):

    if classes[i]["fi"] > maior_frequencia:

        maior_frequencia = classes[i]["fi"]
        indice_modal = i


fm = classes[indice_modal]["fi"]

if indice_modal == 0:
    anterior = 0
else:
    anterior = classes[indice_modal - 1]["fi"]

if indice_modal == len(classes) - 1:
    proxima = 0
else:
    proxima = classes[indice_modal + 1]["fi"]


d1 = fm - anterior
d2 = fm - proxima

li = classes[indice_modal]["inicio"]

moda3 = li + (d1 / (d1 + d2)) * h


# função para quartil, decil e percentil

def separatriz(porcentagem):

    posicao = porcentagem * n

    anterior = 0

    for classe in classes:

        if classe["Fi"] >= posicao:

            li = classe["inicio"]
            fi = classe["fi"]

            resultado = li + ((posicao - anterior) / fi) * h

            return resultado

        anterior = classe["Fi"]


q1 = separatriz(0.25)
q3 = separatriz(0.75)

d2 = separatriz(0.20)
d7 = separatriz(0.70)

p15 = separatriz(0.15)
p22 = separatriz(0.22)
p63 = separatriz(0.63)
p70 = separatriz(0.70)


print("\nResultados com intervalo de classe:")

print(
    f"Média: {media3:.2f} | "
    f"Mediana: {mediana3:.2f} | "
    f"Moda: {moda3:.2f}"
)

print(
    f"Q1: {q1:.2f} | "
    f"Q3: {q3:.2f}"
)

print(
    f"D2: {d2:.2f} | "
    f"D7: {d7:.2f}"
)

print(
    f"P15: {p15:.2f} | "
    f"P22: {p22:.2f} | "
    f"P63: {p63:.2f} | "
    f"P70: {p70:.2f}"
)