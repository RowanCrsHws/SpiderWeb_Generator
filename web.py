import random
from math import sqrt, fabs, sin, cos, atan2


class Web:
    PI = 3.14

    def __init__(self, size, renderer):
        #setup values
        self.Size = size
        self.Renderer = renderer

    #generate web
    def Generate(self, anchor_count, anchor_deviation, radial_count, ring_count, hang, detail):
        self.Detail = detail
        hang += 0.01 # add to hang to avoid division by 0
        self.Center = ((self.Size / 2) + random.randint(-int(self.Size/8), int((self.Size/8))),
                       (self.Size / 2) + random.randint(-int(self.Size/8), int((self.Size/8))))#get center point

        self.Anchors = self.GenerateAnchors(anchor_count, self.Size, self.Center, anchor_deviation)#generate anchors
        self.GenerateLines(hang, radial_count, ring_count, detail)#generate lines

    #set anchor at given point
    def SetAnchor(self, x, y):
        self.Anchors.append((x, y))

    #clear anchors
    def ClearAnchors(self):
        self.Anchors = []

    #generate lines
    def GenerateLines(self, hang, radial_count, ring_count, detail):
        self.Detail = detail
        self.Lines = []
        self.Anchors = self.OrderAnchors(self.Center, self.Anchors)#order anchors in clockwise direction
        alines = self.GenerateAnchorLines(self.Anchors, self.Center, self.Size, hang)#generate lines from anchors to center
        blines = self.GenerateBorderLines(alines, self.Center, hang)#generate border lines, between anchor lines
        rlines = self.GenerateRadialLines(blines, radial_count, self.Center, self.Size, hang)#generate lines from center to border lines
        clines = self.GenerateRingLines(rlines, ring_count, self.ClosestDistToCenter(blines, self.Center, self.Size, self.Detail), self.Size, hang)#generate radial lines
        self.Lines += alines + blines + rlines + clines#combine lines

    #get closest distance to center on line
    def ClosestDistToCenter(self, lines, center, max, detail):
        cd = max
        for i in lines:
            if(i[2]):
                for j in range(0, detail+1):
                    p = self.PointOnCurve(i, j/detail)
                    d = sqrt(fabs(p[0] - center[0]) ** 2 + fabs(p[1] - center[1]) ** 2)
                    if(d < cd):
                        cd = d

        return cd

    #get point a given distance along simple line
    def PointOnLine(self, line, dist):
        if(line[0] == line[1]):
            return line[0]

        dis = sqrt(fabs(line[0][0] - line[1][0]) ** 2 + fabs(line[0][1] - line[1][1]) ** 2)
        pdis = (dis * dist) / dis
        x = int(pdis * line[1][0] + (1 - pdis) * line[0][0])
        y = int(pdis * line[1][1] + (1 - pdis) * line[0][1])
        return (x, y)
    # same as above but for curve
    def PointOnCurve(self, curve, dist):
        x = (1 - dist) ** 2 * curve[0][0] + 2 * (1 - dist) * dist * curve[2][0] + dist ** 2 * curve[1][0]
        y = (1 - dist) ** 2 * curve[0][1] + 2 * (1 - dist) * dist * curve[2][1] + dist ** 2 * curve[1][1]
        return (x, y)
    #generate anchors, in circle around center with given random deviance
    def GenerateAnchors(self, anchor_count, size, center, dev):
        # generate angles at even points with given deviance
        angles = []
        p = (self.PI*2)/anchor_count
        a = 0
        for i in range(0, anchor_count):
            a += p
            angles.append(a + random.uniform(-dev, dev))

        angles.sort()
        anchors = []
        #angles to points
        for i in angles:
            x = int(cos(i) * (self.Size / 2) + random.randint(-int(self.Size/8), int((self.Size/8)))) + center[0]
            y = int(sin(i) * (self.Size / 2) + random.randint(-int(self.Size/8), int((self.Size/8)))) + center[1]
            if(x > size):
                x = size
            elif(x < 0):
                x = 0
            if(y > size):
                y = size
            elif(y < 0):
                y = 0

            anchors.append((x, y))

        return anchors

    #ordering key
    def SortSec(self, val):
        return val[1]

    #order anchors in circle, to allow for user added ones
    def OrderAnchors(self, center, anchors):
        alist = []
        for i in anchors:
            dx = i[0] - center[0]
            dy = center[1] - i[1]
            rad = atan2(dx, dy)
            alist.append((i, rad))
        alist.sort(key=self.SortSec)
        list = [i[0] for i in alist]
        return list

    #generate lines from anchor to center
    def GenerateAnchorLines(self, anchors, center, size, hang):
        lines = []
        for i in anchors:
            a = center
            p = self.PointOnLine((i, a), 0.5)
            lines.append((i, a, (p[0], p[1] + int(size / (16 / hang)))))


        return lines


    #generate border lines, between anchor lines at randomized distance along lines
    def GenerateBorderLines(self, lines, center, hang):
        points = []
        blines = []
        for i in lines:
            points.append(self.PointOnCurve(i, random.uniform(0.1, 0.3)))

        for i in range(0, len(points)):
            l = (points[i], points[(i + 1) % len(points)])
            erp = self.PointOnLine((self.PointOnLine(l, 0.5), center), hang/3)
            blines.append((l[0], l[1], erp))

        return blines

    #generate radial lines at even intervals along border lines
    def GenerateRadialLines(self, outer, count, center, size, hang):
        lines = []
        for j in outer:

            for i in range(0, count):
                l = (self.PointOnCurve(j, i/count), center)
                p = self.PointOnLine(l, 0.5)

                lines.append((l[0], l[1], (p[0], p[1]+int(size/(16/hang)))))

        return lines
    #generate ring lines between radial lines
    def GenerateRingLines(self, radials, count, d, size, hang):
        lines = []
        for i in range(0, count):
            r = int((i/count)*d)

            points = []
            for j in radials:
                le = sqrt(fabs(j[0][0] - j[1][0]) ** 2 + fabs(j[0][1] - j[1][1]) ** 2)
                points.append(self.PointOnCurve((j[1], j[0], j[2]), (r/le)+random.uniform(-0.01, 0.01)))

            lp = len(points)
            for j in range(0, lp):
                l = (points[j], points[(j + 1) % lp])
                p = self.PointOnLine(l, .5)


                lines.append((l[0], l[1], (p[0], p[1]+int(size/(64/hang)))))


        return lines
    #render web with default renderer
    def Render(self, rules, detail=None):
        if(detail):
            d = detail
        else:
            d = self.Detail
        return self.Renderer.Render(self, rules, d)