"""
Sistema de processamento de respostas por email.
NOTA: Este serviço não é mais utilizado pois mudamos para formulário web.
Mantido apenas para referência/histórico.
"""

import re
from datetime import datetime
from typing import Dict, Optional
from ..models.result import Result
from ..models.review import Review
from .database_service import DatabaseService
from .confirmation_service import ConfirmationService


class EmailProcessorService:
    """Serviço para processar respostas de email com avaliações."""
    
    def __init__(self):
        """Inicializa o serviço de processamento de email."""
        self.db_service = DatabaseService()
        self.confirmation_service = ConfirmationService()
    
    def process_email_response(self, email_content: str) -> Result:
        """
        Processa uma resposta de email com avaliação diária.
        
        Args:
            email_content: Conteúdo do email de resposta
            
        Returns:
            Result: Resultado do processamento
        """
        try:
            # Extrai os dados do email
            extracted_data = self._extract_data_from_email(email_content)
            
            if not extracted_data:
                return Result.error_result("Não foi possível extrair dados válidos do email")
            
            # Valida os dados extraídos
            validation_result = self._validate_extracted_data(extracted_data)
            if not validation_result.success:
                return validation_result
            
            # Cria o objeto Review
            review = Review(
                work=extracted_data['work'],
                training=extracted_data['training'],
                studies=extracted_data['studies'],
                mind=extracted_data['mind'],
                positive_points=extracted_data['positive_points'],
                negative_points=extracted_data['negative_points']
            )
            
            # Salva no banco de dados
            save_result = self.db_service.insert_review(review)
            
            if save_result.success:
                print(f"✅ Avaliação processada e salva: ID {review.id}")
                print(f"📊 Média: {review.get_average_score():.1f}/10")
                
                # Envia confirmação para o usuário
                confirmation_result = self.confirmation_service.send_evaluation_confirmation(
                    review, "usuario@exemplo.com"  # Aqui você pode extrair do email
                )
                
                if confirmation_result.success:
                    print("✅ Confirmação enviada para o usuário")
                else:
                    print(f"⚠️  Erro ao enviar confirmação: {confirmation_result.get_first_error()}")
                
                # Envia notificação para admin
                admin_result = self.confirmation_service.send_admin_notification(
                    review, "usuario@exemplo.com"
                )
                
                if admin_result.success:
                    print("📧 Notificação enviada para admin")
                else:
                    print(f"⚠️  Erro ao enviar notificação: {admin_result.get_first_error()}")
                
                return Result.success_result(review)
            else:
                return save_result
                
        except Exception as e:
            return Result.error_result(f"Erro ao processar email: {str(e)}")
    
    def _extract_data_from_email(self, email_content: str) -> Optional[Dict]:
        """
        Extrai dados da avaliação do conteúdo do email.
        
        Args:
            email_content: Conteúdo bruto do email
            
        Returns:
            Dict com os dados extraídos ou None se não conseguir
        """
        try:
            # Padrões para extrair os dados
            patterns = {
                'work': r'work[:\s]*(\d+)',
                'training': r'training[:\s]*(\d+)',
                'studies': r'studies[:\s]*(\d+)',
                'mind': r'mind[:\s]*(\d+)',
                'positive_points': r'positive_points[:\s]*(.*?)(?=negative_points|$)',
                'negative_points': r'negative_points[:\s]*(.*?)$'
            }
            
            extracted = {}
            
            # Extrai notas numéricas
            for field, pattern in patterns.items():
                if field in ['work', 'training', 'studies', 'mind']:
                    match = re.search(pattern, email_content, re.IGNORECASE)
                    if match:
                        try:
                            extracted[field] = int(match.group(1))
                        except ValueError:
                            return None
                    else:
                        return None
                else:
                    # Extrai texto
                    match = re.search(pattern, email_content, re.IGNORECASE | re.DOTALL)
                    if match:
                        extracted[field] = match.group(1).strip()
                    else:
                        return None
            
            return extracted
            
        except Exception as e:
            print(f"Erro ao extrair dados: {str(e)}")
            return None
    
    def _validate_extracted_data(self, data: Dict) -> Result:
        """
        Valida os dados extraídos do email.
        
        Args:
            data: Dados extraídos
            
        Returns:
            Result: Resultado da validação
        """
        errors = []
        
        # Valida notas (0-10)
        for field in ['work', 'training', 'studies', 'mind']:
            if field not in data:
                errors.append(f"Campo {field} não encontrado")
            elif not isinstance(data[field], int) or data[field] < 0 or data[field] > 10:
                errors.append(f"Campo {field} deve ser um número entre 0 e 10")
        
        # Valida textos
        for field in ['positive_points', 'negative_points']:
            if field not in data:
                errors.append(f"Campo {field} não encontrado")
            elif not isinstance(data[field], str) or not data[field].strip():
                errors.append(f"Campo {field} não pode estar vazio")
        
        if errors:
            return Result.error_result_multiple(errors)
        
        return Result.success_result()
    
    def simulate_email_processing(self, work: int, training: int, studies: int, 
                                mind: int, positive_points: str, negative_points: str) -> Result:
        """
        Simula o processamento de um email (para testes).
        
        Args:
            work, training, studies, mind: Notas (0-10)
            positive_points, negative_points: Comentários
            
        Returns:
            Result: Resultado do processamento
        """
        # Simula o formato de email
        email_content = f"""
        work: {work}
        training: {training}
        studies: {studies}
        mind: {mind}
        positive_points: {positive_points}
        negative_points: {negative_points}
        """
        
        return self.process_email_response(email_content)
    
    def get_processing_stats(self) -> Result:
        """
        Retorna estatísticas do processamento de emails.
        
        Returns:
            Result: Estatísticas do processamento
        """
        try:
            # Busca todas as avaliações
            reviews_result = self.db_service.get_all_reviews()
            
            if not reviews_result.success:
                return reviews_result
            
            reviews = reviews_result.data
            total_reviews = len(reviews)
            
            if total_reviews == 0:
                return Result.success_result({
                    'total_processed': 0,
                    'last_processing': None,
                    'success_rate': 0
                })
            
            # Calcula estatísticas
            stats = {
                'total_processed': total_reviews,
                'last_processing': reviews[0].id if reviews else None,
                'success_rate': 100,  # Assumindo que todas foram processadas com sucesso
                'average_score': sum(r.get_average_score() for r in reviews) / total_reviews
            }
            
            return Result.success_result(stats)
            
        except Exception as e:
            return Result.error_result(f"Erro ao obter estatísticas: {str(e)}")
