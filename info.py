tier1_asns = []
with open("static/tier1_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        As = {}
        if len(sp) == 8:
            As["asn"], As["name"], As["country"], As["scale"], As["min_lgt"], As["max_lgt"], As["dms"], As["posis"] = sp
            tier1_asns.append(As)

tier2_asns = []
with open("static/tier2_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        As = {}
        if len(sp) == 8:
            As["asn"], As["name"], As["country"], As["scale"], As["min_lgt"], As["max_lgt"], As["dms"], As["posis"] = sp
            tier2_asns.append(As)

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
    "旧金山": [
                -122.25,
                37.46
            ],
    "西雅图": [
                -122.19,
                47.36
            ],
    "圣保罗": [
                -46.38,
                -23.33
    ],
    "新加坡": [
                103.45,
                1.22
    ],
    "上海": [
                121.27,
                31.14
    ],
    "悉尼": [
                151.17,
                -33.55
    ],
    "丹佛": [
                -104.59,
                39.43
    ],
    "芝加哥": [
                -87,
                41.51
    ],
    "阿姆斯特丹": [
                4.52,
                52.21
    ],
    "华沙": [
                21,
                52.15
    ],
    "柏林": [
                13.2,
                52.31
    ],
    "香港": [
                114,
                22.17
    ],
    "休斯顿": [
                -95.23,
                29.6
    ],
    "多伦多": [
                -79.33,
                43.6
    ],
    "波士顿": [
                -71,
                42.29
    ],
    "盐湖城": [
                -111.89,
                40.7
    ],
    "孟买": [
                72.8,
                18.95
    ],


}


if __name__ == "__main__":
    print(len(tier1_asns))
    print(tier1_asns)
