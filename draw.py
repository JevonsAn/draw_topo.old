import tornado.web
import tornado.ioloop
import os
import random
import math
import json

from info import tier1_asns, citys, tier2_asns, asn_leafs

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
x_scale = [3, 3, 10, 10, 10, 4, 10, 6, 6, 6, 7.5, 3]
x_width = [x / sum(x_scale) * 1200 for x in x_scale]
x_list = [100 + sum(x_width[:i]) for i in range(len(x_width) + 1)]
p_list = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
du_list = ['%d° W' % i for i in range(180, -1, -30)] + ['%d° E' % i for i in range(30, 181, 30)]

# rects = []

lines = []
# tier2_rects = []


def rand_color():
    def hsv2rgb(h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    h = random.randint(0, 360)
    s = random.randint(0, 150) / 256
    v = 200 / 256
    r, g, b = hsv2rgb(h, s, v)
    # print(h,s,v)
    res = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res = res.upper().replace(" ", "0")

    h = random.randint(h - 20, h + 20)
    s = random.randint(int(s * 256 - 20), int(s * 256 + 20)) / 256
    v = 150 / 256

    r, g, b = hsv2rgb(h, s, v)
    # print(h,s,v)
    res2 = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res2 = res2.upper().replace(" ", "0")
    return res, res2


def calc_posi(lgt):
    t = len(p_list) - 2
    for i in range(len(p_list) - 1):
        if p_list[i] <= lgt < p_list[i + 1]:
            t = i
            break
    base = x_list[t]
    width = lgt - p_list[t]
    real_width = width / 30 * x_width[t]
    return base + real_width


def rect_posi():
    rects = []
    lgtss = []
    # lines = []
    dots = []
    tier2_rects = []

    thigh = 100
    # print([t['scale'] for t in asns])
    tier1_asns.sort(key=lambda As: int(As['scale']), reverse=True)
    # print(tier1_asns)
    for asn in tier1_asns:
        t1 = 3
        t2 = 0
        high = math.log(int(asn["scale"])) * t1 + t2
        a = dict()
        a["asn"] = int(asn["asn"])
        a["color"], dark_color = rand_color()
        a["yp"] = thigh + 1
        a["height"] = high
        thigh += high
        a["name"] = f'{asn["asn"]}, {asn["name"]}, {asn["country"]}'
        a["scale"] = asn["scale"]
        min_x = float(asn["min_lgt"])
        max_x = float(asn["max_lgt"])
        if max_x <= 180:
            a["xp"] = calc_posi(min_x)
            a["width"] = calc_posi(max_x) - a["xp"]
            rects.append(a)
        else:
            a["xp"] = calc_posi(min_x)
            a["width"] = calc_posi(180) - a["xp"]
            rects.append(a)
            b = {x: y for x, y in a.items()}
            b["xp"] = calc_posi(-180)
            b["width"] = calc_posi(max_x - 360) - b["xp"]
            # print(min_x, max_x)
            # print(calc_posi(-180), calc_posi(180), a, b)
            rects.append(b)
        lgts = map(int, asn["posis"].split(","))
        for l in lgts:
            lgtss.append({"xp": calc_posi(l), "yp": a["yp"], "width": 2,
                         "color": dark_color, "height": a["height"] - 3, "lgt": l})
        for l in asn_leafs[a["asn"]]:
            if l[0] > 180:
                pl = calc_posi(l[0] - 360)
            else:
                pl = calc_posi(l[0])
            dots.append({"xp": "%.1f" % pl, "yp": thigh - 1.5, "color": dark_color, "other": l[1], "lgt": "%.1f" % l[0]})

    # print(rects, dots)
    thigh += 40
    # print(tier2_asns)
    for asn in tier2_asns:
        high = 12
        a = dict()
        # print(asn["asn"])
        a["asn"] = int(asn["asn"])
        a["color"], dark_color = rand_color()
        a["yp"] = thigh + 1
        a["height"] = high
        thigh += high
        a["name"] = f'{asn["asn"]}, {asn["name"]}, {asn["country"]}'
        a["scale"] = asn["scale"]
        min_x = float(asn["min_lgt"])
        max_x = float(asn["max_lgt"])
        if max_x <= 180:
            a["xp"] = calc_posi(min_x)
            a["width"] = calc_posi(max_x) - a["xp"]
            tier2_rects.append(a)
        else:
            a["xp"] = calc_posi(min_x)
            a["width"] = calc_posi(180) - a["xp"]
            tier2_rects.append(a)
            b = {x: y for x, y in a.items()}
            b["xp"] = calc_posi(-180)
            b["width"] = calc_posi(max_x - 360) - b["xp"]
            # print(min_x, max_x)
            # print(calc_posi(-180), calc_posi(180), a, b)
            tier2_rects.append(b)
        for l in asn_leafs.get(a["asn"], []):
            if l[0] > 180:
                pl = calc_posi(l[0] - 360)
            else:
                pl = calc_posi(l[0])
            dots.append({"xp": "%.1f" % pl, "yp": thigh - 1.5, "color": dark_color, "other": l[1], "lgt": "%.1f" % l[0]})

    return rects, lgtss, tier2_rects, dots


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        pos_to_name = {x_list[0]: "", x_list[-1]: ""}
        for city in citys:
            posi = calc_posi(citys[city][0])
            pos_to_name[posi] = city
            lines.append({"xp": posi})
        x = list(sorted(pos_to_name.keys()))

        du = [pos_to_name[m] for m in x]
        self.render("topo.html", x_list=x_list, x_domain=du_list, x_list2=x, x_domain2=du)


class JsonHandler(tornado.web.RequestHandler):

    def get(self):
        # print(lines)
        rects, lgts, tier2_rects, dots = rect_posi()
        # print(tier2_rects[:20])
        self.write(json.dumps({"rects": rects, "lgts": lgts, "lines": lines, "rect2s": tier2_rects, "dots": dots}))


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    application = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/json", JsonHandler),
            # (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/auto/bgpsim/web"})
        ],
        debug=True,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(application)
    # http_server.bind(65530)
    # http_server.start(0)
    http_server.listen(5678)
    tornado.ioloop.IOLoop.instance().start()
