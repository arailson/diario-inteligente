"""
Modelo para representar uma avaliação diária.
Contém as notas e comentários sobre diferentes aspectos do dia.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Review:
    """
    Classe que representa uma avaliação diária.
    
    Atributos:
        work (int): Nota para trabalho (0-10)
        training (int): Nota para treino (0-10)
        studies (int): Nota para estudos (0-10)
        mind (int): Nota para estado mental (0-10)
        positive_points (str): Pontos positivos do dia
        negative_points (str): Pontos negativos do dia
        id (Optional[int]): ID único no banco de dados
    """
    work: int
    training: int
    studies: int
    mind: int
    positive_points: str
    negative_points: str
    id: Optional[int] = None
    
    def __post_init__(self):
        """Valida os dados após a inicialização."""
        self._validate()
    
    def _validate(self):
        """Valida se os dados estão corretos."""
        errors = []
        
        # Validação das notas (devem ser números entre 0 e 10)
        for field_name, value in [
            ("work", self.work),
            ("training", self.training),
            ("studies", self.studies),
            ("mind", self.mind)
        ]:
            if not isinstance(value, (int, float)):
                errors.append(f"O campo {field_name} deve ser um número.")
            elif value < 0 or value > 10:
                errors.append(f"O campo {field_name} deve estar entre 0 e 10.")
        
        # Validação dos comentários
        if not isinstance(self.positive_points, str) or not self.positive_points.strip():
            errors.append("O campo 'positive_points' deve ser uma string não vazia.")
        
        if not isinstance(self.negative_points, str) or not self.negative_points.strip():
            errors.append("O campo 'negative_points' deve ser uma string não vazia.")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def get_average_score(self) -> float:
        """Calcula a média das notas."""
        return (self.work + self.training + self.studies + self.mind) / 4
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'work': self.work,
            'training': self.training,
            'studies': self.studies,
            'mind': self.mind,
            'positive_points': self.positive_points,
            'negative_points': self.negative_points
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Review':
        """Cria um objeto Review a partir de um dicionário."""
        return cls(
            id=data.get('id'),
            work=data['work'],
            training=data['training'],
            studies=data['studies'],
            mind=data['mind'],
            positive_points=data['positive_points'],
            negative_points=data['negative_points']
        )
