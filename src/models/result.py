"""
Classe para padronizar resultados de operações.
Facilita o tratamento de sucessos e erros de forma consistente.
"""

from typing import Any, List, Optional


class Result:
    """
    Classe para representar o resultado de uma operação.
    
    Atributos:
        success (bool): Indica se a operação foi bem-sucedida
        data (Any): Dados retornados pela operação
        errors (List[str]): Lista de mensagens de erro
    """
    
    def __init__(self, success: bool, data: Any = None, errors: Optional[List[str]] = None):
        self.success = success
        self.data = data
        self.errors = errors or []
    
    def __str__(self) -> str:
        """Representação em string do resultado."""
        if self.success:
            return f"Success: {self.data}"
        else:
            return f"Errors: {', '.join(self.errors)}"
    
    def __bool__(self) -> bool:
        """Permite usar o objeto em contextos booleanos."""
        return self.success
    
    @classmethod
    def success_result(cls, data: Any = None) -> 'Result':
        """Cria um resultado de sucesso."""
        return cls(success=True, data=data)
    
    @classmethod
    def error_result(cls, error_message: str) -> 'Result':
        """Cria um resultado de erro com uma mensagem."""
        return cls(success=False, errors=[error_message])
    
    @classmethod
    def error_result_multiple(cls, error_messages: List[str]) -> 'Result':
        """Cria um resultado de erro com múltiplas mensagens."""
        return cls(success=False, errors=error_messages)
    
    def add_error(self, error_message: str):
        """Adiciona uma mensagem de erro ao resultado."""
        if self.success:
            self.success = False
        self.errors.append(error_message)
    
    def has_errors(self) -> bool:
        """Verifica se há erros."""
        return len(self.errors) > 0
    
    def get_first_error(self) -> Optional[str]:
        """Retorna o primeiro erro, se houver."""
        return self.errors[0] if self.errors else None
