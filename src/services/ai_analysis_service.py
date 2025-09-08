"""
Serviço de IA para análise das avaliações semanais.
Gera insights e recomendações baseadas nas notas e comentários.
"""

from typing import Dict, List, Any
from ..models.result import Result
from ..models.review import Review


class AIAnalysisService:
    """Serviço para análise inteligente das avaliações."""
    
    def __init__(self):
        """Inicializa o serviço de análise."""
        self.analysis_templates = {
            'excellent': {
                'threshold': 8.5,
                'messages': [
                    "🎉 Parabéns! Sua semana foi excepcional!",
                    "✨ Você está no caminho certo, continue assim!",
                    "🏆 Excelente desempenho em todas as áreas!"
                ]
            },
            'good': {
                'threshold': 7.0,
                'messages': [
                    "👍 Boa semana! Você está progredindo bem!",
                    "📈 Continue mantendo esse ritmo positivo!",
                    "💪 Você está evoluindo constantemente!"
                ]
            },
            'average': {
                'threshold': 5.5,
                'messages': [
                    "🔄 Semana equilibrada! Há espaço para melhorias.",
                    "🎯 Foque nas áreas que precisam de mais atenção.",
                    "💡 Pequenos ajustes podem fazer grande diferença!"
                ]
            },
            'needs_improvement': {
                'threshold': 0,
                'messages': [
                    "🌱 Esta semana foi desafiadora, mas você pode melhorar!",
                    "💪 Cada dia é uma nova oportunidade de crescimento.",
                    "🎯 Vamos focar em pequenas melhorias diárias!"
                ]
            }
        }
    
    def analyze_weekly_data(self, weekly_data: Dict[str, Any], reviews: List[Review]) -> Result:
        """
        Analisa os dados semanais e gera insights personalizados.
        
        Args:
            weekly_data: Dados estatísticos da semana
            reviews: Lista de avaliações da semana
            
        Returns:
            Result: Análise completa com insights e recomendações
        """
        try:
            overall_average = weekly_data['overall_average']
            
            # Determina o nível de performance
            performance_level = self._get_performance_level(overall_average)
            
            # Analisa padrões nas avaliações
            patterns = self._analyze_patterns(reviews)
            
            # Gera insights específicos
            insights = self._generate_insights(weekly_data, patterns)
            
            # Cria recomendações personalizadas
            recommendations = self._generate_recommendations(weekly_data, patterns)
            
            # Monta a análise completa
            analysis = {
                'performance_level': performance_level,
                'overall_average': overall_average,
                'patterns': patterns,
                'insights': insights,
                'recommendations': recommendations,
                'motivational_message': self._get_motivational_message(performance_level),
                'weekly_summary': self._create_weekly_summary(weekly_data, patterns)
            }
            
            return Result.success_result(analysis)
            
        except Exception as e:
            return Result.error_result(f"Erro na análise: {str(e)}")
    
    def _get_performance_level(self, average: float) -> str:
        """Determina o nível de performance baseado na média."""
        if average >= self.analysis_templates['excellent']['threshold']:
            return 'excellent'
        elif average >= self.analysis_templates['good']['threshold']:
            return 'good'
        elif average >= self.analysis_templates['average']['threshold']:
            return 'average'
        else:
            return 'needs_improvement'
    
    def _analyze_patterns(self, reviews: List[Review]) -> Dict[str, Any]:
        """Analisa padrões nas avaliações."""
        if not reviews:
            return {}
        
        patterns = {
            'strongest_area': '',
            'weakest_area': '',
            'most_mentioned_positive': '',
            'most_mentioned_negative': '',
            'consistency_score': 0
        }
        
        # Calcula médias por área
        work_scores = [r.work for r in reviews]
        training_scores = [r.training for r in reviews]
        studies_scores = [r.studies for r in reviews]
        mind_scores = [r.mind for r in reviews]
        
        area_averages = {
            'Trabalho': sum(work_scores) / len(work_scores),
            'Treino': sum(training_scores) / len(training_scores),
            'Estudos': sum(studies_scores) / len(studies_scores),
            'Mente': sum(mind_scores) / len(mind_scores)
        }
        
        patterns['strongest_area'] = max(area_averages, key=area_averages.get)
        patterns['weakest_area'] = min(area_averages, key=area_averages.get)
        
        # Analisa consistência (quanto menor o desvio padrão, mais consistente)
        all_scores = work_scores + training_scores + studies_scores + mind_scores
        if all_scores:
            mean_score = sum(all_scores) / len(all_scores)
            variance = sum((score - mean_score) ** 2 for score in all_scores) / len(all_scores)
            patterns['consistency_score'] = max(0, 10 - (variance ** 0.5))
        
        return patterns
    
    def _generate_insights(self, weekly_data: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """Gera insights baseados nos dados."""
        insights = []
        
        # Insight sobre área mais forte
        if patterns.get('strongest_area'):
            insights.append(f"🎯 Sua área mais forte esta semana foi: {patterns['strongest_area']}")
        
        # Insight sobre área que precisa melhorar
        if patterns.get('weakest_area'):
            insights.append(f"📈 Área para focar: {patterns['weakest_area']}")
        
        # Insight sobre consistência
        consistency = patterns.get('consistency_score', 0)
        if consistency > 7:
            insights.append("✨ Você manteve uma rotina muito consistente!")
        elif consistency > 5:
            insights.append("🔄 Sua rotina teve algumas variações, mas está no caminho certo.")
        else:
            insights.append("🎯 Que tal tentar manter uma rotina mais regular?")
        
        # Insight sobre progresso geral
        overall = weekly_data['overall_average']
        if overall >= 8:
            insights.append("🏆 Semana excepcional! Continue assim!")
        elif overall >= 7:
            insights.append("👍 Boa semana! Você está progredindo bem!")
        elif overall >= 6:
            insights.append("📊 Semana equilibrada, há espaço para melhorias.")
        else:
            insights.append("💪 Semana desafiadora, mas você pode melhorar!")
        
        return insights
    
    def _generate_recommendations(self, weekly_data: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """Gera recomendações personalizadas."""
        recommendations = []
        
        # Recomendação baseada na área mais fraca
        weakest = patterns.get('weakest_area', '')
        if weakest:
            if weakest == 'Trabalho':
                recommendations.append("💼 Que tal organizar melhor suas tarefas de trabalho?")
            elif weakest == 'Treino':
                recommendations.append("🏃‍♂️ Tente incluir pelo menos 30min de atividade física por dia.")
            elif weakest == 'Estudos':
                recommendations.append("📚 Reserve um horário fixo para estudar todos os dias.")
            elif weakest == 'Mente':
                recommendations.append("🧘‍♀️ Pratique meditação ou atividades relaxantes.")
        
        # Recomendação baseada na consistência
        consistency = patterns.get('consistency_score', 0)
        if consistency < 5:
            recommendations.append("⏰ Tente manter horários mais regulares para suas atividades.")
        
        # Recomendação geral baseada na média
        overall = weekly_data['overall_average']
        if overall < 6:
            recommendations.append("🎯 Foque em pequenas melhorias diárias, elas fazem grande diferença!")
        elif overall >= 8:
            recommendations.append("🌟 Continue mantendo esse excelente padrão!")
        
        return recommendations
    
    def _get_motivational_message(self, performance_level: str) -> str:
        """Retorna uma mensagem motivacional baseada no nível de performance."""
        import random
        
        messages = self.analysis_templates[performance_level]['messages']
        return random.choice(messages)
    
    def _create_weekly_summary(self, weekly_data: Dict[str, Any], patterns: Dict[str, Any]) -> str:
        """Cria um resumo semanal personalizado."""
        summary = f"""
📊 RESUMO DA SEMANA:

🎯 Média Geral: {weekly_data['overall_average']}/10
📅 Total de dias avaliados: {weekly_data['total_reviews']}

🏆 Área mais forte: {patterns.get('strongest_area', 'N/A')}
📈 Área para melhorar: {patterns.get('weakest_area', 'N/A')}
✨ Consistência: {patterns.get('consistency_score', 0):.1f}/10
        """.strip()
        
        return summary
