import math
import matplotlib.pyplot as plt

from src.error_handling.interpreter_error import (
    BaseForInvalidNumberOfArgumentsError,
    BaseForInvalidFunCallArgumentsError
)


class Symbol:
    def __init__(self, value=None) -> None:
        self.value = value

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value


class Point:
    def __init__(self, arguments) -> None:
        self.attributes = {
            'x': Symbol(arguments[0]),
            'y': Symbol(arguments[1])
        }
        self.methods = {
            'get_x': self.get_x,
            'get_y': self.get_y,
            'set_x': self.set_x,
            'set_y': self.set_y,
        }

    def get_x(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['x']

    def get_y(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['y']

    def set_x(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(
                1,
                len(arguments)
            )
        if isinstance(arguments[0], (int, float)) is False:
            raise BaseForInvalidFunCallArgumentsError('set_x')
        self.attributes['x'].set_value(arguments[0])

    def set_y(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(
                1,
                len(arguments)
            )
        if isinstance(arguments[0], (int, float)) is False:
            raise BaseForInvalidFunCallArgumentsError('set_y')
        self.attributes['y'].set_value(arguments[0])

    def get_properties(self, method_name):
        x = self.attributes['x'].get_value()
        y = self.attributes['y'].get_value()
        if (
            isinstance(x, (int, float)) is False or
            isinstance(y, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return x, y


class Figure:
    def __init__(self, arguments) -> None:
        self.attributes = {
            'position': Symbol(arguments[0]),
            'color': Symbol('grey'),
            'border_color': Symbol('black'),
            'border_width': Symbol(1),
            'border_style': Symbol('solid'),
            'fill': Symbol(True),
            'opacity': Symbol(1),
        }
        self.methods = {
            'get_color': self.get_color,
            'get_border_color': self.get_border_color,
            'get_border_width': self.get_border_width,
            'get_border_style': self.get_border_style,
            'get_fill': self.get_fill,
            'get_opacity': self.get_opacity,
            'set_color': self.set_color,
            'set_border_color': self.set_border_color,
            'set_border_width': self.set_border_width,
            'set_border_style': self.set_border_style,
            'set_fill': self.set_fill,
            'set_opacity': self.set_opacity,
            'area': self.area,
            'perimeter': self.perimeter,
            'move_to': self.move_to,
            'render': self.render
        }

    def get_color(self):
        return self.attributes['color']

    def get_border_color(self):
        return self.attributes['border_color']

    def get_border_width(self):
        return self.attributes['border_width']

    def get_border_style(self):
        return self.attributes['border_style']

    def get_fill(self):
        return self.attributes['fill']

    def get_opacity(self):
        return self.attributes['opacity']

    def set_color(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if isinstance(arguments[0], (int, float, str)) is False:
            raise BaseForInvalidFunCallArgumentsError('set_color')
        self.attributes['color'].set_value(arguments[0])

    def set_border_color(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if isinstance(arguments[0], (int, float, str)) is False:
            raise BaseForInvalidFunCallArgumentsError('set_border_color')
        self.attributes['border_color'].set_value(arguments[0])

    def set_border_width(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if isinstance(arguments[0], (int, float)) is False:
            raise BaseForInvalidFunCallArgumentsError('set_border_width')
        self.attributes['border_width'].set_value(arguments[0])

    def set_border_style(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if arguments[0] not in [
            '-', 'solid',
            '--', 'dashed',
            '-.', 'dashdot',
            ':', 'dotted'
        ]:
            raise BaseForInvalidFunCallArgumentsError('set_border_style')
        self.attributes['border_style'].set_value(arguments[0])

    def set_fill(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if isinstance(arguments[0], bool) is False:
            raise BaseForInvalidFunCallArgumentsError('set_fill')
        self.attributes['fill'].set_value(arguments[0])

    def set_opacity(self, arguments):
        if len(arguments) != 1:
            raise ValueError('Invalid number of arguments')
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] < 0 or arguments[0] > 1
        ):
            raise BaseForInvalidFunCallArgumentsError('set_opacity')
        self.attributes['opacity'].set_value(arguments[0])

    def area(self, arguments):
        pass

    def perimeter(self, arguments):
        pass

    def move_to(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if isinstance(arguments[0], Point) is False:
            raise BaseForInvalidFunCallArgumentsError('move_to')
        self.attributes['position'].set_value(arguments[0])

    def render(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        figure = self.patch()
        plt.axes()
        plt.gca().add_patch(figure)
        plt.axis('scaled')
        plt.show()


class Square(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['side'] = Symbol(arguments[1])
        self.methods['get_side'] = self.get_side
        self.methods['set_side'] = self.set_side
        self.methods['diagonal'] = self.diagonal

    def get_side(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['side']

    def set_side(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_side')
        self.attributes['side'].set_value(arguments[0])

    def get_properties(self, method_name):
        side = self.attributes['side'].get_value()
        if isinstance(side, (int, float)) is False:
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return side

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side = self.get_properties('area')
        return Symbol(side * side)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side = self.get_properties('circumference')
        return Symbol(4 * side)

    def diagonal(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side = self.get_properties('diagonal')
        return Symbol(side * math.sqrt(2))

    def patch(self):
        x, y = self.attributes['position'].get_value().get_properties('patch')
        position = (x, y)
        side = self.get_properties('patch')
        square = plt.Rectangle(
            position,
            side,
            side,
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return square


class Rectangle(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['width'] = Symbol(arguments[1])
        self.attributes['height'] = Symbol(arguments[2])
        self.methods['get_width'] = self.get_width
        self.methods['get_height'] = self.get_height
        self.methods['set_width'] = self.set_width
        self.methods['set_height'] = self.set_height
        self.methods['diagonal'] = self.diagonal

    def get_width(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['width']

    def get_height(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['height']

    def set_width(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_width')
        self.attributes['width'].set_value(arguments[0])

    def set_height(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False
            or arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_height')
        self.attributes['height'].set_value(arguments[0])

    def get_properties(self, method_name):
        width = self.attributes['width'].get_value()
        height = self.attributes['height'].get_value()
        if (
            isinstance(width, (int, float)) is False or
            isinstance(height, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return width, height

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        width, height = self.get_properties('area')
        return Symbol(width * height)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        width, height = self.get_properties('circumference')
        return Symbol(2 * (width + height))

    def diagonal(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        width, height = self.get_properties('diagonal')
        return Symbol(math.sqrt(width ** 2 + height ** 2))

    def patch(self):
        x = self.attributes['position'].get_value().attributes['x'].get_value()
        y = self.attributes['position'].get_value().attributes['y'].get_value()
        position = (x, y)
        rectangle = plt.Rectangle(
            position,
            self.attributes['width'].get_value(),
            self.attributes['height'].get_value(),
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return rectangle


class Circle(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['radius'] = Symbol(arguments[1])
        self.methods['get_radius'] = self.get_radius
        self.methods['set_radius'] = self.set_radius
        self.methods['diameter'] = self.diameter

    def get_radius(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['radius']

    def set_radius(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False
            or arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_radius')
        self.attributes['radius'].set_value(arguments[0])

    def get_properties(self, method_name):
        radius = self.attributes['radius'].get_value()
        if isinstance(radius, (int, float)) is False:
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return radius

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        r = self.get_properties('area')
        return Symbol(3.14 * r * r)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        r = self.get_properties('circumference')
        return Symbol(2 * 3.14 * r)

    def diameter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        r = self.get_properties('diameter')
        return Symbol(2 * r)

    def patch(self):
        x = self.attributes['position'].get_value().attributes['x'].get_value()
        y = self.attributes['position'].get_value().attributes['y'].get_value()
        position = (x, y)
        circle = plt.Circle(
            position,
            self.attributes['radius'].get_value(),
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return circle


class Triangle(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['point1'] = self.attributes['position']
        self.attributes['point2'] = Symbol(arguments[1])
        self.attributes['point3'] = Symbol(arguments[2])
        self.methods['get_point1'] = self.get_point1
        self.methods['get_point2'] = self.get_point2
        self.methods['get_point3'] = self.get_point3
        self.methods['set_point1'] = self.set_point1
        self.methods['set_point2'] = self.set_point2
        self.methods['set_point3'] = self.set_point3
        self.methods['sides'] = self.sides
        self.methods['heights'] = self.heights
        self.methods['move_to'] = self.move_to

    def get_point1(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['point1']

    def get_point2(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['point2']

    def get_point3(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['point3']

    def set_point1(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(2, len(arguments))
        if (isinstance(arguments[0], Point) is False):
            raise BaseForInvalidFunCallArgumentsError('set_point1')
        self.attributes['point1'].set_value(arguments[0])

    def set_point2(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(2, len(arguments))
        if (isinstance(arguments[0], Point) is False):
            raise BaseForInvalidFunCallArgumentsError('set_point2')
        self.attributes['point2'].set_value(arguments[0])

    def set_point3(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(2, len(arguments))
        if (isinstance(arguments[0], Point) is False):
            raise BaseForInvalidFunCallArgumentsError('set_point3')
        self.attributes['point3'].set_value(arguments[0])

    def get_properties(self, method_name):
        point1 = self.attributes['point1'].get_value()
        point2 = self.attributes['point2'].get_value()
        point3 = self.attributes['point3'].get_value()
        if (
            isinstance(point1, Point) is False or
            isinstance(point2, Point) is False or
            isinstance(point3, Point) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return point1, point2, point3

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        point1, point2, point3 = self.get_properties('area')
        x1 = point1.get_x([]).get_value()
        y1 = point1.get_y([]).get_value()
        x2 = point2.get_x([]).get_value()
        y2 = point2.get_y([]).get_value()
        x3 = point3.get_x([]).get_value()
        y3 = point3.get_y([]).get_value()
        area = 0.5 * (
            x1 * (y2 - y3) +
            x2 * (y3 - y1) +
            x3 * (y1 - y2)
        )
        return Symbol(area)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        point1, point2, point3 = self.get_properties('circumference')
        side1 = self.side_length(point1, point2)
        side2 = self.side_length(point2, point3)
        side3 = self.side_length(point3, point1)
        return Symbol(side1 + side2 + side3)

    def side_length(self, point1, point2):
        x1 = point1.get_x([]).get_value()
        y1 = point1.get_y([]).get_value()
        x2 = point2.get_x([]).get_value()
        y2 = point2.get_y([]).get_value()
        return math.sqrt(
            (x2 - x1) ** 2 + (y2 - y1) ** 2
        )

    def sides(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        point1, point2, point3 = self.get_properties('sides')
        side1 = self.side_length(point1, point2)
        side2 = self.side_length(point2, point3)
        side3 = self.side_length(point3, point1)
        return Symbol([Symbol(side1), Symbol(side2), Symbol(side3)])

    def heights(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        point1, point2, point3 = self.get_properties('heights')
        side1 = self.side_length(point1, point2)
        side2 = self.side_length(point2, point3)
        side3 = self.side_length(point3, point1)
        area = self.area([]).get_value()
        h1 = 2 * area / side1
        h2 = 2 * area / side2
        h3 = 2 * area / side3
        return Symbol([Symbol(h1), Symbol(h2), Symbol(h3)])

    def move_to(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if isinstance(arguments[0], Point) is False:
            raise BaseForInvalidFunCallArgumentsError('move_to')
        current_x = self.attributes['point1'].get_value().get_x([]).get_value()
        current_y = self.attributes['point1'].get_value().get_y([]).get_value()
        x = current_x - arguments[0].get_x([]).get_value()
        y = current_y - arguments[0].get_y([]).get_value()
        self.attributes['point1'].set_value(arguments[0])
        self.attributes['point2'].get_value().set_x(
            [self.attributes['point2'].get_value().get_x([]).get_value() - x]
        )
        self.attributes['point2'].get_value().set_y(
            [self.attributes['point2'].get_value().get_y([]).get_value() - y]
        )
        self.attributes['point3'].get_value().set_x(
            [self.attributes['point3'].get_value().get_x([]).get_value() - x]
        )
        self.attributes['point3'].get_value().set_y(
            [self.attributes['point3'].get_value().get_y([]).get_value() - y]
        )

    def patch(self):
        point1 = self.attributes['point1'].get_value()
        point2 = self.attributes['point2'].get_value()
        point3 = self.attributes['point3'].get_value()
        if (
            isinstance(point1, Point) is False or
            isinstance(point2, Point) is False or
            isinstance(point3, Point) is False
        ):
            raise BaseForInvalidFunCallArgumentsError('patch')
        x1 = point1.get_x([]).get_value()
        y1 = point1.get_y([]).get_value()
        x2 = point2.get_x([]).get_value()
        y2 = point2.get_y([]).get_value()
        x3 = point3.get_x([]).get_value()
        y3 = point3.get_y([]).get_value()
        triangle = plt.Polygon(
            [
                (x1, y1),
                (x2, y2),
                (x3, y3)
            ],
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return triangle


class Rhomb(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['side'] = Symbol(arguments[1])
        self.attributes['angle'] = Symbol(arguments[2])
        self.methods['get_side'] = self.get_side
        self.methods['get_angle'] = self.get_angle
        self.methods['set_side'] = self.set_side
        self.methods['set_angle'] = self.set_angle
        self.methods['diagonals'] = self.diagonals

    def get_side(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['side']

    def get_angle(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['angle']

    def set_side(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_side')
        self.attributes['side'].set_value(arguments[0])

    def set_angle(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0 or arguments[0] >= 180
        ):
            raise BaseForInvalidFunCallArgumentsError('set_angle')
        self.attributes['angle'].set_value(arguments[0])

    def get_properties(self, method_name):
        side = self.attributes['side'].get_value()
        angle = self.attributes['angle'].get_value()
        if (
            isinstance(side, (int, float)) is False or
            isinstance(angle, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return side, angle

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side, angle = self.get_properties('area')
        return Symbol(side * side * math.sin(math.radians(angle)))

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side, _ = self.get_properties('circumference')
        return Symbol(4 * side)

    def diagonals(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        side, angle = self.get_properties('diagonals')
        diagonal1 = side * math.sqrt(2 * (1 + math.cos(math.radians(angle))))
        diagonal2 = side * math.sqrt(2 * (1 - math.cos(math.radians(angle))))
        return Symbol([Symbol(diagonal1), Symbol(diagonal2)])

    def patch(self):
        x = self.attributes['position'].get_value().attributes['x'].get_value()
        y = self.attributes['position'].get_value().attributes['y'].get_value()
        if (
            isinstance(x, (int, float)) is False or
            isinstance(y, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError('patch')
        position = (x, y)
        side, angle = self.get_properties('patch')
        b = (
            x + side * math.cos(math.radians(angle)),
            y + side * math.sin(math.radians(angle))
        )
        c = (
            b[0] + side,
            b[1]
        )
        d = (
            x + side,
            y
        )
        rhomb = plt.Polygon(
            [position, b, c, d],
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return rhomb


class Parallelogram(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['base'] = Symbol(arguments[1])
        self.attributes['height'] = Symbol(arguments[2])
        self.attributes['angle'] = Symbol(arguments[3])
        self.methods['get_base'] = self.get_base
        self.methods['get_height'] = self.get_height
        self.methods['get_angle'] = self.get_angle
        self.methods['set_base'] = self.set_base
        self.methods['set_height'] = self.set_height
        self.methods['set_angle'] = self.set_angle
        self.methods['sides'] = self.sides
        self.methods['diagonals'] = self.diagonals

    def get_base(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['base']

    def get_height(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['height']

    def get_angle(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['angle']

    def set_base(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_base')
        self.attributes['base'].set_value(arguments[0])

    def set_height(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_height')
        self.attributes['height'].set_value(arguments[0])

    def set_angle(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0 or arguments[0] >= 180
        ):
            raise BaseForInvalidFunCallArgumentsError('set_angle')
        self.attributes['angle'].set_value(arguments[0])

    def get_properties(self, method_name):
        base = self.attributes['base'].get_value()
        height = self.attributes['height'].get_value()
        angle = self.attributes['angle'].get_value()
        if (
            isinstance(base, (int, float)) is False or
            isinstance(height, (int, float)) is False or
            isinstance(angle, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return base, height, angle

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base, height, _ = self.get_properties('area')
        return Symbol(base * height)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base, height, angle = self.get_properties('circumference')
        return Symbol(2 * (base + height / math.sin(math.radians(angle))))

    def sides(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base, height, angle = self.get_properties('sides')
        side1 = base
        side2 = height / math.sin(math.radians(angle))
        return Symbol([Symbol(side1), Symbol(side2)])

    def diagonals(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base, height, angle = self.get_properties('diagonals')
        side = height / math.sin(math.radians(angle))
        diagonal1 = math.sqrt(
            base ** 2 + side ** 2 +
            2 * base * side * math.cos(math.radians(angle))
        )
        diagonal2 = math.sqrt(
            base ** 2 + side ** 2 -
            2 * base * side * math.cos(math.radians(angle))
        )
        return Symbol([Symbol(diagonal1), Symbol(diagonal2)])

    def patch(self):
        x = self.attributes['position'].get_value().attributes['x'].get_value()
        y = self.attributes['position'].get_value().attributes['y'].get_value()
        position = (x, y)
        base = self.attributes['base'].get_value()
        height = self.attributes['height'].get_value()
        angle = self.attributes['angle'].get_value()
        b = (
            x + height / math.tan(math.radians(angle)),
            y + height
        )
        c = (
            b[0] + base,
            b[1]
        )
        d = (
            x + base,
            y
        )
        parallelogram = plt.Polygon(
            [position, b, c, d],
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return parallelogram


class Trapeze(Figure):
    def __init__(self, arguments) -> None:
        super().__init__(arguments)
        self.attributes['base1'] = Symbol(arguments[1])
        self.attributes['base2'] = Symbol(arguments[2])
        self.attributes['height'] = Symbol(arguments[3])
        self.methods['get_base1'] = self.get_base1
        self.methods['get_base2'] = self.get_base2
        self.methods['get_height'] = self.get_height
        self.methods['set_base1'] = self.set_base1
        self.methods['set_base2'] = self.set_base2
        self.methods['set_height'] = self.set_height

    def get_base1(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['base1']

    def get_base2(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['base2']

    def get_height(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        return self.attributes['height']

    def set_base1(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_base1')
        self.attributes['base1'].set_value(arguments[0])

    def set_base2(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False
            or arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_base2')
        self.attributes['base2'].set_value(arguments[0])

    def set_height(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        if (
            isinstance(arguments[0], (int, float)) is False or
            arguments[0] <= 0
        ):
            raise BaseForInvalidFunCallArgumentsError('set_height')
        self.attributes['height'].set_value(arguments[0])

    def get_properties(self, method_name):
        base1 = self.attributes['base1'].get_value()
        base2 = self.attributes['base2'].get_value()
        height = self.attributes['height'].get_value()
        if (
            isinstance(base1, (int, float)) is False or
            isinstance(base2, (int, float)) is False or
            isinstance(height, (int, float)) is False
        ):
            raise BaseForInvalidFunCallArgumentsError(method_name)
        return base1, base2, height

    def area(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base1, base2, height = self.get_properties('area')
        return Symbol(0.5 * (base1 + base2) * height)

    def perimeter(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        base1, base2, height = self.get_properties('circumference')
        side1 = math.sqrt((0.5 * (base2 - base1)) ** 2 + height ** 2)
        side2 = math.sqrt((0.5 * (base2 + base1)) ** 2 + height ** 2)
        return Symbol(base1 + base2 + side1 + side2)

    def patch(self):
        x = self.attributes['position'].get_value().attributes['x'].get_value()
        y = self.attributes['position'].get_value().attributes['y'].get_value()
        position = (x, y)
        base1 = self.attributes['base1'].get_value()
        base2 = self.attributes['base2'].get_value()
        height = self.attributes['height'].get_value()
        b = (
            x + 0.5 * (base1 - base2),
            y + height
        )
        c = (
            b[0] + base2,
            b[1]
        )
        d = (
            x + base1,
            y
        )
        trapezoid = plt.Polygon(
            [position, b, c, d],
            fc=self.attributes['color'].get_value(),
            ec=self.attributes['border_color'].get_value(),
            lw=self.attributes['border_width'].get_value(),
            ls=self.attributes['border_style'].get_value(),
            fill=self.attributes['fill'].get_value(),
            alpha=self.attributes['opacity'].get_value()
        )
        return trapezoid


class Scene:
    def __init__(self, arguments) -> None:
        self.attributes = {
            'figures': Symbol(arguments[0]),
        }
        self.methods = {
            'add': self.add_figure,
            'remove': self.remove_figure,
            'clear': self.clear,
            'render': self.render
        }

    def add_figure(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        self.attributes['figures'].get_value().append(Symbol(arguments[0]))

    def remove_figure(self, arguments):
        if len(arguments) != 1:
            raise BaseForInvalidNumberOfArgumentsError(1, len(arguments))
        self.attributes['figures'].get_value().pop(arguments[0])

    def clear(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        self.attributes['figures'].get_value().clear()

    def render(self, arguments):
        if len(arguments) != 0:
            raise BaseForInvalidNumberOfArgumentsError(0, len(arguments))
        plt.axes()
        for figure in self.attributes['figures'].get_value():
            try:
                plt.gca().add_patch(figure.get_value().patch())
            except BaseForInvalidFunCallArgumentsError:
                raise BaseForInvalidFunCallArgumentsError('render')
        plt.axis('scaled')
        plt.show()
