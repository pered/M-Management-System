from typing import Optional

class Sample:
    def __init__(self,
                 petal_width : float,
                 petal_length : float,
                 sepal_width : float,
                 sepal_length : float,
                 species : Optional[str] = None) -> None:
        self.petal_width = petal_width
        self.petal_length = petal_length
        self.sepal_width = sepal_width
        self.sepal_length = sepal_length
        self.species = species
        self.classification : Optional[str] = None
        
    def __repr__(self) -> str:
        if self.species is None:
            known_unknown = "UnknownSepcies"
        else:
            known_unknown = "KnownSpecies"
        if self.classification is None:
            classification = ""
        else:
            classification = f", {self.classification}"
            
        return (f"{known_unknown}("
        f"{self.petal_width},"
        f"{self.petal_length},"
        f"{self.sepal_width},"
        f"{self.sepal_length},"
        f"{self.species},"
        f"{classification}"
        f")")
    
    def classify(self, classification : str) -> None:
        self.classification = classification
    
    def matches(self) -> bool:
        return self.classification == self.species
    
def main() -> None:
    petal = Sample(2.5,2.1,3.4,3.6,"Iris")
    

if __name__ == "__main__":
    main()