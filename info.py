asns = []
with open("static/tier1_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        As = {}
        if len(sp) == 7:
            As["asn"], As["name"], As["country"], As["scale"], As["min_lgt"], As["max_lgt"], As["dms"] = sp
            asns.append(As)

citys = {
    "北京": [116.39723, 39.9075],
    "纽约": [
                -75.29128,
                43.10535
            ],
    "洛杉矶": [
                -118.15,
                34.04
            ],
    "夏威夷": [
                -155.33,
                19.46
            ],
    "伦敦": [
                0.10,
                51.30
            ],
    "莫斯科": [
                37.35,
                55.45
            ],
    "新德里": [
                77.13,
                28.37

            ],
    "东京": [
                139.46,
                35.42
            ],
}


if __name__ == "__main__":
    print(len(asns))
    print(asns)
