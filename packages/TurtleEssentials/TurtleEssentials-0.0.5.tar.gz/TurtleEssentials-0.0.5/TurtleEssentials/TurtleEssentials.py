try:
    import turtle as tu
except ImportError:
    print("Imports failed!")

class Shape:
    Last_Shape = []
    Last_Item_Index = 0

    @staticmethod
    def Remove_Shape():
        if Shape.Last_Shape:
            shape = Shape.Last_Shape.pop()
            shape.clear()

    @staticmethod
    def Star(Size=20, DoFill=False, Color="Black", FillColor="Yellow", pos1=100, pos2=100):
        star = tu.Turtle()
        Shape.Last_Shape.append(star)
        Shape.Last_Item_Index = len(Shape.Last_Shape) - 1
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
        elif not DoFill:
            for i in range(5):
                star.forward(Size)
                star.left(54)
                star.forward(Size)
                star.right(126)

    @staticmethod
    def Hexagon(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        hexagon = tu.Turtle()
        Shape.Last_Shape.append(hexagon)
        hexagon.penup()
        hexagon.goto(pos1, pos2)
        hexagon.pencolor(Color)
        hexagon.pendown()
        if DoFill:
            hexagon.begin_fill()
            hexagon.fillcolor(FillColor)
            for _ in range(6):
                hexagon.forward(Size)
                hexagon.left(60)
            hexagon.end_fill()
        elif not DoFill:
            for _ in range(6):
                hexagon.forward(Size)
                hexagon.left(60)

    @staticmethod
    def Square(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        square = tu.Turtle()
        Shape.Last_Shape.append(square)
        square.penup()
        square.goto(pos1, pos2)
        square.pencolor(Color)
        square.pendown()
        if DoFill:
            square.begin_fill()
            square.fillcolor(FillColor)
            for _ in range(4):
                square.forward(Size)
                square.left(90)
            square.end_fill()
        elif not DoFill:
            for _ in range(4):
                square.forward(Size)
                square.left(90)

    @staticmethod
    def Triangle(Size=20, DoFill=False, Color="Black", FillColor="Black", pos1=100, pos2=100):
        triangle = tu.Turtle()
        Shape.Last_Shape.append(triangle)
        triangle.penup()
        triangle.goto(pos1, pos2)
        triangle.pencolor(Color)
        triangle.pendown()
        if DoFill:
            triangle.fillcolor(FillColor)
            triangle.begin_fill()
            for _ in range(3):
                triangle.forward(Size)
                triangle.left(120)
            triangle.end_fill()
        elif not DoFill:
            for _ in range(3):
                triangle.forward(Size)
                triangle.left(120)