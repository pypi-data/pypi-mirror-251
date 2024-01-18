try:
    import turtle as tu
except ImportError:
    print("Imports failed!")

Last_Shape = None
if Last_Shape == None:
    pass

class Shape:
    def Star(Size=20, DoFill=False, Color="Black", FillColor="Yellow" , pos1=100, pos2=100):
        star = tu.Turtle()
        Last_Shape = star
        star.penup()
        star.goto(pos1, pos2)
        star.pencolor(Color)
        star.pendown()
        if DoFill:
            star.begin_fill()
            star.fillcolor(FillColor)
            for i in range(5):
                star.forward(Size)
                star.left(54)
                star.forward(Size)
                star.right(126)
            star.end_fill()
        elif DoFill == False:
            for i in range(5):
                star.forward(Size)
                star.left(54)
                star.forward(Size)
                star.right(126)


    def Hexagon(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        hex = tu.Turtle()
        Last_Shape = hex
        hex.penup()
        hex.goto(pos1,pos2)
        hex.pencolor(Color)
        hex.pendown()
        if DoFill:
            hex.begin_fill()
            hex.fillcolor(FillColor)
            for i in range(6):
                hex.forward(Size)
                hex.left(60)
            hex.end_fill()
        if DoFill == False:
            for i in range(6):
                hex.forward(Size)
                hex.left(60)

    def Square(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        Last_Shape = sqr
        sqr = tu.Turtle()
        sqr.penup()
        sqr.goto(pos1, pos2)
        sqr.pencolor(Color)
        sqr.pendown()
        if DoFill:
            sqr.begin_fill()
            sqr.fillcolor(FillColor)
            for i in range(4):
                sqr.forward(Size)
                sqr.left(90)
            sqr.end_fill()
        if DoFill == False:
            for i in range():
                sqr.forward(Size)
                sqr.left(90)

    def Triangle(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        Last_Shape = t
        t = tu.Turtle()
        t.penup()
        t.goto(pos1, pos2)
        t.pencolor(Color)
        t.pendown()
        if DoFill:
            t.fillcolor(FillColor)
            t.begin_fill()
            for i in range(3):
                t.forward(Size)
                t.left(120)
            t.end_fill()
        if DoFill == False:
            for i in range(3):
                t.forward(Size)
                t.left(120)
    
    def Template(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        Last_Shape = t
        t = tu.Turtle()
        t.penup()
        t.goto(pos1, pos2)
        t.pencolor(Color)
        t.pendown()
        if DoFill:
            t.begin_fill()
            t.fillcolor(FillColor)
            for i in range():
                t.forward(Size)
                t.left()
            t.end_fill()
        if DoFill == False:
            for i in range():
                t.forward(Size)
                t.left()

class Edit:
    def RemoveShape(shape=Last_Shape):
        tu.clear(shape)



