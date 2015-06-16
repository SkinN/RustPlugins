class antiwounded:

    def __init__(self):

        self.Title='Anti-Wounded'
        self.Author='SkinN'
        self.ResourceId=1045
        self.Version=V(1,0,1)

    def CanBeWounded(self, player, hitinfo):

        return False