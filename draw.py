import tornado.web
import tornado.ioloop
import os
import random
import math
import json

from info import asns

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
x_scale = [10, 15, 10, 10, 10, 10, 10, 20, 10, 10, 10, 10]
x_width = [x / sum(x_scale) * 1200 for x in x_scale]
x_list = [100 + sum(x_width[:i]) for i in range(len(x_width) + 1)]
p_list = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
du_list = ['%d° W' % i for i in range(180, -1, -30)] + ['%d° E' % i for i in range(30, 181, 30)]


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
    s = random.randint(0, 256) / 256
    v = random.randint(100, 200) / 256
    r, g, b = hsv2rgb(h, s, v)
    res = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res = res.upper().replace(" ", "0")
    return res


def calc_posi(lgt):
    t = len(p_list) - 2
    for i in range(len(p_list) - 1):
        if p_list[i] <= lgt < p_list[i + 1]:
            t = i
            break
    base = x_list[t]
    width = lgt - p_list[t]
    real_width = width / 30 * x_width[t]
    return base + real_width + 1


def rect_posi():
    n = -1
    rects = []
    for asn in asns:
        n += 1
        a = {}
        a["asn"] = int(asn["asn"])
        a["color"] = rand_color()
        a["yp"] = 50 + n * 20 + 1
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
            b = {}
            b["asn"] = a["asn"]
            b["color"] = a["color"]
            b["yp"] = a["yp"]
            b["xp"] = calc_posi(-180)
            b["width"] = calc_posi(max_x - 360) - b["xp"]
            print(min_x, max_x)
            print(calc_posi(-180), calc_posi(180), a, b)
            rects.append(b)
    return rects


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("topo.html", x_list=x_list, x_domain=du_list)


class JsonHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(json.dumps(rect_posi()))


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
    http_server.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
