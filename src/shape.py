class Shape:
    def __init__(self, x, y, fill_color='', edge_color='red', dash_style=None, dx=None, dy=None):
        self.x = x
        self.y = y
        self.x_axis = None
        self.y_axis = None
        self.fill_color = fill_color
        self.edge_color = edge_color
        self.dash_style = dash_style
        self.tk_id = None

    def __str__(self):
        """
        Return special string shapes
        :return:
        """

        return self.__class__.__name__ + \
               "{} ({}, {}) ({},{},dash={}  ".format(self.tk_id,
                                                     self.x, self.y,
                                                     self.fill_color,
                                                     self.edge_color,
                                                     self.dash_style)
