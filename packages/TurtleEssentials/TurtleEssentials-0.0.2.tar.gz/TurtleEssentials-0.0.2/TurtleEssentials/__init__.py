try:
    import turtle as t
except ImportError:
    print("Imports failed!")

class Shape:
    def Star(Size=20, DoFill=False, Color="Black", FillColor="Yellow" , pos1=100, pos2=100):
        t.penup()
        t.goto(pos1, pos2)
        t.pencolor(Color)
        t.pendown()
        if DoFill:
            t.begin_fill()
            t.fillcolor(FillColor)
            for i in range(5):
                t.forward(Size)
                t.left(54)
                t.forward(Size)
                t.right(126)
            t.end_fill()
        elif DoFill == False:
            for i in range(5):
                t.forward(Size)
                t.left(54)
                t.forward(Size)
                t.right(126)

    def Hexagon(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        t.penup()
        t.goto(pos1,pos2)
        t.pencolor(Color)
        t.pendown()
        if DoFill:
            t.begin_fill()
            t.fillcolor(FillColor)
            for i in range(6):
                t.forward(Size)
                t.left(60)
            t.end_fill()
        if DoFill == False:
            for i in range(6):
                t.forward(Size)
                t.left(60)

    def Square(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        t.penup()
        t.goto(pos1, pos2)
        t.pencolor(Color)
        t.pendown()
        if DoFill:
            t.begin_fill()
            t.fillcolor(FillColor)
            for i in range(4):
                t.forward(Size)
                t.left(90)
            t.end_fill()
        if DoFill == False:
            for i in range():
                t.forward(Size)
                t.left(90)

    def Triangle(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
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



