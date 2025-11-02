
fich = open("fichier.txt", "w")
fich.write("Le soleil se couchait lentement derrière les montagnes, teintant le ciel de nuances rouges et dorées. "
           "Dans le village endormi, les lumières des maisons s’allumaient une à une, comme des étoiles terrestres. "
           "Amir marchait sans hâte le long du sentier, écoutant le murmure du vent et le chant lointain d’un ruisseau. "
           "Chaque pas soulevait un peu de poussière, chaque souffle lui rappelait qu’il était vivant. "
           "Il ne savait pas vraiment où il allait, mais il avançait, guidé par ce calme étrange qui naît quand le cœur trouve enfin le silence. "
           "Parfois, la plus belle destination est celle qu’on découvre sans la chercher.")
fich.close()


fich = open("fichier.txt", "r")
text = fich.read()


dic = {}
for mot in text.split():
    mot = mot.strip(",.?!;:(){}[]<>\"")
    if mot.isalpha():
        if mot in dic:
            dic[mot] += 1
        else:
            dic[mot] = 1

print(dic)


moy = 0
L = []
D = []
P = []
MAx = max(dic.values())
Min = min(dic.values())

for word, count in dic.items():
    if word == word[::-1]:
        P.append(word)
    if count == MAx:
        L.append(word)
    if count == Min:
        D.append(word)
    moy += count * len(word)

print("La longueur moyenne des mots est", moy / sum(dic.values()))
print("Les mots les plus utilisés sont", L)
print("Les mots les moins utilisés sont", D)
print("Les mots palindromes sont", P)

phrases = text.split(",")
print(f"Il y a {len(phrases)} phrases")


text2 = " ".join(text)
pon = []
for lettre in text2:
    if not lettre.isalpha() and lettre not in pon and lettre != " ":
        pon.append(lettre)
print("Les ponctuations utilisées sont", pon)


t = [i for i in dic.values()]
l = []
for i in t:
    if i not in l:
        l.append(i)
l.sort(reverse=True)

L = []
M = []
for i in l[0:10]:
    for key, value in dic.items():
        if i == value:
            M.append(key)
    L.append(M)
    M = []

print("Top 10 words in frequency:")
c = 1
for i in L:
    print("-", c, i)
    c += 1


swapped = 1
while swapped:
    swapped = 0
    for i in range(len(phrases) - 1):
        if len(phrases[i]) < len(phrases[i + 1]):
            phrases[i], phrases[i + 1] = phrases[i + 1], phrases[i]
            swapped = 1

print(phrases)
