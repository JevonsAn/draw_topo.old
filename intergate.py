from sql_operation import *
# from asn_to_cnum_dict import asn_to_cnum_dict
# from pymysql import IntegrityError
# from prefix_to_asn_dict import ip_to_asn_dict
# from handle.prefix_info import prefix_info
import json
"""
    从文件中提取自治域号和前缀信息
"""

# pre_asn_file = open("prefix_to_asn.txt", "w")

# with open("originas") as f:
#     fl = 0
#     length_dict = {}
#     for line in f.readlines():
#         fl += 1
#         # if fl > 10:
#         #     break
#         if fl % 2 == 0:
#             continue
#         sp = line.strip().split("\t")
#         # print(sp)
#         last = sp[-1].split(" ")

#         asn, prefix, length = (str(x[1: -1]) for x in last)

#         # prefix24 = ".".join(sp[0].split(".")[::-1] + ["0"])
#         # print(prefix24)

#         pre_asn_file.write("%s %s %s\n" % (asn, prefix, length))


# pre_asn_file.close()


def ip_dec_to_bin(address):
    bin_list = ["%08d" % int(bin(int(x))[2:]) for x in address.split(".")]
    bins = ".".join(bin_list)
    return bins


def ip_bin_to_dec(address):
    dec_list = [str(int(x, 2)) for x in address.split(".")]
    return ".".join(dec_list)


def max_min_ip_in_prefix(prefix, length):
    length = int(length)
    bin_ip = ip_dec_to_bin(prefix)
    mx = [x for x in bin_ip]
    mn = [x for x in bin_ip]
    real_l = 0
    for i, w in enumerate(bin_ip):
        if w != ".":
            real_l += 1
            if real_l > length:
                mx[i] = "1"
                mn[i] = "0"
    mx[-1] = "0"
    mn[-2] = "1"
    return ip_bin_to_dec("".join(mn)), ip_bin_to_dec("".join(mx))


"""
    计算用于获取地理信息的ip列表
"""

# ip_to_asn_dict = {}
# # ip_file = open("ip_list.txt", "w")

# with open("prefix_to_asn.txt") as f:
#     for line in f.readlines():
#         asn, prefix, length = line.strip().split(" ")
#         mx, mn = max_min_ip_in_prefix(prefix, length)
#         if mx in ip_to_asn_dict:
#             ip_to_asn_dict[mx].append((prefix, length, asn))
#         else:
#             ip_to_asn_dict[mx] = [(prefix, length, asn)]
#         if mn in ip_to_asn_dict:
#             ip_to_asn_dict[mn].append((prefix, length, asn))
#         else:
#             ip_to_asn_dict[mn] = [(prefix, length, asn)]
#         # ip_file.write("%s\n%s\n" % (mx, mn))
#     print("ip_to_asn_dict = ", ip_to_asn_dict, file=open("prefix_to_asn_dict.py", "w"))


# ip_file.close()


"""
    计算各自治域的custom数量并把关系写入数据库
"""
asn_to_custom_num_dict = {}
links = get_links()
exe_list = []
for link in links:
    as1 = link[0]
    as2 = link[1]
    relationship = link[2]
    if relationship == "P2C":
        if as1 in asn_to_custom_num_dict:
            asn_to_custom_num_dict[as1] += 1
        else:
            asn_to_custom_num_dict[as1] = 1
        exe_list.append((as1, as2))
    elif relationship == "C2P":
        if as2 in asn_to_custom_num_dict:
            asn_to_custom_num_dict[as2] += 1
        else:
            asn_to_custom_num_dict[as2] = 1
        exe_list.append((as2, as1))
    else:
        if as1 not in asn_to_custom_num_dict:
            asn_to_custom_num_dict[as1] = 0
        if as2 not in asn_to_custom_num_dict:
            asn_to_custom_num_dict[as2] = 0
print(len(exe_list))
insert_relation_many(exe_list)
print(asn_to_custom_num_dict, file=open("asn_to_cnum_dict.py", "w"))


"""
    插入AS信息
"""
# as_list = get_asns()
# now_asns = get_now_asns()
# asn_set = set()
# for ass in as_list:
#     asn = ass[0]
#     asn_set.add(asn)
# print(len(asn_set))

# exe_list = []
# for i, asn in enumerate(now_asns):
#     an = asn[0]
#     if an not in asn_set:

#         # custom_num = 0
#         # if str(an) in asn_to_cnum_dict:
#         #     custom_num = asn_to_cnum_dict[str(an)]
#         # n = (*asn, custom_num)
#         # exe_list.append(n)

# res = insert_asinfo_many(exe_list)
# if not res[0]:
#     print(res[1])

# lendict = {'18': 677298, '19': 668636, '22': 320092, '20': 559063, '21': 336901, '23': 128611, '32': 2259, '16': 13545, '17': 786196, '13': 3561, '15': 3126, '14': 3465, '12': 3472, '11': 2110, '28': 11192, '27': 23078, '26': 54912, '25': 118309, '29': 14935, '8': 13, '9': 1108, '30': 7376, '31': 796, '10': 1491}
# print(sum([x for x in lendict.values()]))

"""
    整合地理信息
"""
# geo_json = ""
# with open("数据/QueryResult.json") as f:
#     geo_json = f.read()
# geo_json = json.loads(geo_json)

# position_json = ""
# with open("数据/cityPosition.txt") as f:
#     position_json = f.read()
# position_json = json.loads(position_json)

# n = 0
# prefix_dict = {}
# for item in geo_json:
#     ip = item['IP_addr']
#     country, province, city = (item['location']['country'], item['location']['province'], item['location']['city'])
#     longitude, dimension = 0, 0
#     if (country, province, city) == ('null', 'null', 'null'):
#         continue
#     try:
#         longitude, dimension = position_json[country][province][city]
#     except Exception as e:
#         print(ip, country, province, city, file=open("no_geo.txt", "a"))
#         continue

#     if ip in ip_to_asn_dict:
#         for info in ip_to_asn_dict[ip]:
#             prefix, length, asn = info
#             if '{' in asn:
#                 continue
#             if (prefix, int(length)) not in prefix_dict:
#                 prefix_dict[(prefix, int(length))] = {"asn": int(asn), "position": [(longitude, dimension)]}
#             else:
#                 prefix_dict[(prefix, int(length))]["position"].append((longitude, dimension))
#     else:
#         print(ip)

# print("prefix_info =", prefix_dict, file=open("prefix_info.py", "w"))

# unormal_prefix_info = {}
# normal_prefix_info = []
# # prefix_info = {}
# # with open("prefix_info.txt") as f:
# #     prefix_info = json.loads(f.read())
#
# for pre in prefix_info:
#     if len(prefix_info[pre]["position"]) != 2:
#         unormal_prefix_info[pre] = prefix_info[pre]
#     else:
#         prefix, length = pre
#         asn = prefix_info[pre]["asn"]
#         pos1, pos2 = prefix_info[pre]["position"]
#         dimension = (pos1[1] + pos2[1]) / 2
#         width = abs(pos1[0] - pos2[0])
#         longitude = min(pos1[0], pos2[0])
#         if width > 180:
#             width = 360 - width
#             longitude = max(pos1[0], pos2[0])
#         normal_prefix_info.append((prefix, length, asn, longitude, width))
# # print(len(normal_prefix_info), normal_prefix_info[:10])
# print(unormal_prefix_info, file=open("unormal_prefix_info.txt", "w"))
# insert_prefix_info_many(normal_prefix_info)

# asn_positions = {}
# for pre in prefix_info:
#     if len(prefix_info[pre]["position"]) == 2:
#         prefix, length = pre
#         asn = prefix_info[pre]["asn"]
#         pos1, pos2 = prefix_info[pre]["position"]
#         dimension = (pos1[1] + pos2[1]) / 2
#         if asn in asn_positions:
#             asn_positions[asn]["lgt"].extend([pos1[0], pos2[0]])
#             asn_positions[asn]["dms"].append(dimension)
#         else:
#             asn_positions[asn] = {"lgt": [pos1[0], pos2[0]], "dms": [dimension]}


def calc_width(l, jiange):
    max_wid = 0
    max_index = 0
    for i in range(len(l) - 1):
        this = l[i]
        next = l[i + 1]
        wid = next - this
        if wid > max_wid:
            max_wid = wid
            max_index = i + 1
    this = l[len(l) - 1]
    next = l[0]
    if this * next < 0:
        wid = 180 - this + next + 180
        if wid > max_wid:
            max_wid = wid
            max_index = 0
    indexs = []
    indexs.append(max_index)
    for i in range(0, len(l) - 1):
        ai = (max_index + i) % len(l)
        bi = (max_index + i + 1) % len(l)
        this = l[ai]
        next = l[bi]
        if bi == 0:
            wid = 180 - this + next + 180
        else:
            wid = next - this
        if wid > jiange:
            indexs.append(bi)

    rects = [(l[x], l[(indexs[i + 1]) % len(l) - 1]) for i, x in enumerate(indexs[:-1])] + [(l[indexs[-1]], l[indexs[0] - 1],)]
    new_rects = []
    for i, r in enumerate(rects):
        if r[0] == r[1]:
            new_rects.append((r[0] - 3, r[0] + 3))
        elif r[0] > 0 and r[1] < 0:
            new_rects.append((r[0], 180))
            new_rects.append((-180, r[1]))
        else:
            new_rects.append(r)
    return new_rects


print(calc_width([-170, -90, 2, 3, 4, 160], 50))

# asn_posi = {}
# for asn in asn_positions:
#     lgt_list = asn_positions[asn]["lgt"]
#     lgt_list.sort()
#     max_wid = 0
