from src.invalid_shape_parameter_error import InvalidShapeParameterError
from src.shape import Shape
from src.rectangle import Rectangle


class Square(Rectangle):
    def __init__(self, x, y, base=None, fill_color='', edge_color='red', dash_style=None, dx=None,
                 dy=None, ):
        super().__init__(x, y, base, base, fill_color, edge_color, dash_style, dx, dy)

        # If base is not given, but dx and dy are (dx and dy are the mouse's 
        # distance from the center in terms of x and y, respectively), make base
        # the max between dx and dy.
        if base is None and dx is not None and dy is not None:
            base = max(dy, dx) * 2

        if base is None:
            raise InvalidShapeParameterError("Square: height and width are not defined!!")

        self.x_axis = base / 2
        self.y_axis = base / 2
        self.base = base

    def __str__(self):
        """
        Return special string for square
        :return:
        """
        return f"{Shape.__str__(self)} b={self.base}"

    # Square inherits draw and update methods from Rectangle.

