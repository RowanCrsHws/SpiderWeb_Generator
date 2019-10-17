from PIL import Image, ImageDraw
from random import randint

#render web to pil image, includes aa
class ImageRender:

    #draw curve from line segments
    def DrawCurve(self, line, draw, detail, web, aa):
        # curves are made of 3 points simple line are made of 2
        if (line[2]):  # check if line has 3 points
            # create array of points
            points = []
            for i in range(0, detail+1):
                points.append(web.PointOnCurve(line, i / detail))

            # draw a line segment between each point
            for i in range(0, len(points)-1):
                draw.line(((points[i][0]*aa, points[i][1]*aa), (points[i+1][0]*aa, points[i+1][1]*aa)), (255, 255, 255), int(aa/2))
        else:#draw simple line
            draw.line((line[0], line[1]), (255, 255, 255), int(aa/2))

    #render web
    def Render(self, web, rules, detail):
        aa = rules["aa"]#get aa
        img = Image.new("RGB", (web.Size*aa, web.Size*aa))#create image size of given resolution multiplied by aa

        draw = ImageDraw.Draw(img)
        #draw anchor points if enabled
        if(rules["draw_anchor"]):
            for i in web.Anchors:
                draw.ellipse(((i[0]*aa-3, i[1]*aa-3), (i[0]*aa+3, i[1]*aa+3)), fill=(255, 0, 0))
        #draw center if enabled
        if(rules["draw_center"]):
            c = (web.Center * aa, web.Center * aa)
            draw.ellipse(((c[0] - 3, c[1] - 3), (c[0] + 3, c[1] + 3)), fill=(0, 255, 0))
        #draw lines
        for i in web.Lines:
            self.DrawCurve(i, draw, detail, web, aa)

        del draw
        img = img.resize((int(web.Size), int(web.Size)), resample=Image.LANCZOS)#resample image to given resolution
        img.save("webs/" + rules["name"] + ".png", "PNG")#save iamge
        return img




