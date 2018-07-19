asns = []
with open("static/tier1_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        As = {}
        if len(sp) == 6:
            As["asn"], As["name"], As["country"], As["scale"], As["min_lgt"], As["max_lgt"] = sp
            asns.append(As)
asns.sort(key=lambda As: As['scale'])

if __name__ == "__main__":
    print(len(asns))
    print(asns)
