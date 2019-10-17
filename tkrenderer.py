#render web to tk canvas
class TkRender:

    def __init__(self, cnv):
        self.Cnv = cnv
    #draw curve with line segments
    def DrawCurve(self, line, c, detail, web):
        #curves are made of 3 points simple line are made of 2
        if (line[2]):#check if line has 3 points
            #create array of points
            points = []
            for i in range(0, detail + 1):
                points.append(web.PointOnCurve(line, i / detail))

            #draw a line segment between each point
            for i in range(0, len(points) - 1):
                c.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="white", width=1)

        else:#draw simple line
            c.create_line(line[0][0], line[0][1], line[1][0], line[1][1], fill="white", width=1)

    #render web
    def Render(self, web, rules, detail):
        c = self.Cnv
        c.delete("all")#clear canvas

        #draw anchor points if enabled
        if(rules["draw_anchor"]):
            for i in web.Anchors:
                c.create_oval(i[0]-3, i[1]-3, i[0]+3, i[1]+3, fill="red")

        #draw center if enabled
        if(rules["draw_center"]):
            i = web.Center
            c.create_oval(i[0] - 3, i[1] - 3, i[0] + 3, i[1] + 3, fill="green")

        #draw lines
        for i in web.Lines:
            self.DrawCurve(i, c, detail, web)