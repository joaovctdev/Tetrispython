class Colors:    
    dark_grey = (0,0,0)
    Cor1 = (119, 9, 230)
    Cor2 = (9, 230, 82)
    Cor3 = (255,255,255)
    Cor4 = (22, 31, 234)
    Cor5 = (243, 255, 11)
    Cor6 = (254, 92, 254)
    Cor7 = (230, 141, 10)
    white= (255,255,255)
    dark_blue = (44,44,127)
    light_blue = (59,85,162)
    black = (0,0,0)
    
    @classmethod
    def get_cell_colors(cls):
        return(cls.dark_grey, cls.Cor1, cls.Cor2, cls.Cor3, cls.Cor4, cls.Cor5, cls.Cor6, cls.Cor7)