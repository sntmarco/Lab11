from dataclasses import dataclass

@dataclass
class Connessioni:
    id : int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : float
    difficolta : str
    durata : str
    anno : int

    def __eq__(self, other):
        return isinstance(other, Connessioni) and self.id == other.id

    def __str__(self):
        return f"{self.id_rifugio1, self.id_rifugio2, self.distanza, self.difficolta, self.durata, self.anno}"

    def __repr__(self):
        return f"{self.id_rifugio1, self.id_rifugio2, self.distanza, self.difficolta, self.durata, self.anno}"