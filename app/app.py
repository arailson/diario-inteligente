"""
Aplicação Flask - Diário Inteligente
Servidor web para formulário de avaliação diária.
"""

import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from src.models.review import Review
from src.services.database_service import DatabaseService
from src.services.confirmation_service import ConfirmationService


def create_app():
    """Factory para criar a aplicação Flask."""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Inicializa os serviços
    db_service = DatabaseService()
    confirmation_service = ConfirmationService()
    
    @app.route('/')
    def index():
        """Página inicial - redireciona para o formulário."""
        return redirect(url_for('formulario'))
    
    @app.route('/formulario')
    def formulario():
        """Página do formulário de avaliação."""
        email = request.args.get('email', '')
        date = request.args.get('date', datetime.now().strftime('%d/%m/%Y'))
        
        return render_template('formulario.html', email=email, date=date)
    
    @app.route('/api/submit', methods=['POST'])
    def submit_form():
        """API para receber os dados do formulário."""
        try:
            data = request.get_json()
            
            # Valida os dados
            required_fields = ['work', 'training', 'studies', 'mind', 
                             'positive_points', 'negative_points', 'email']
            
            for field in required_fields:
                if field not in data or data[field] == '':
                    return jsonify({
                        'success': False,
                        'error': f'Campo {field} é obrigatório'
                    }), 400
            
            # Valida notas (0-10)
            for field in ['work', 'training', 'studies', 'mind']:
                try:
                    value = int(data[field])
                    if value < 0 or value > 10:
                        return jsonify({
                            'success': False,
                            'error': f'Campo {field} deve ser entre 0 e 10'
                        }), 400
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': f'Campo {field} deve ser um número'
                    }), 400
            
            # Cria o objeto Review
            review = Review(
                work=int(data['work']),
                training=int(data['training']),
                studies=int(data['studies']),
                mind=int(data['mind']),
                positive_points=data['positive_points'],
                negative_points=data['negative_points']
            )
            
            # Salva no banco de dados
            result = db_service.insert_review(review)
            
            if not result.success:
                return jsonify({
                    'success': False,
                    'error': 'Erro ao salvar avaliação no banco de dados'
                }), 500
            
            # Envia confirmação para o usuário
            user_email = data['email']
            confirmation_service.send_evaluation_confirmation(review, user_email)
            
            # Envia notificação para admin
            confirmation_service.send_admin_notification(review, user_email)
            
            return jsonify({
                'success': True,
                'message': 'Avaliação enviada com sucesso!',
                'review_id': review.id,
                'average_score': review.get_average_score()
            }), 200
            
        except Exception as e:
            print(f"Erro ao processar formulário: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Erro interno do servidor'
            }), 500
    
    @app.route('/sucesso')
    def sucesso():
        """Página de confirmação após envio."""
        return render_template('sucesso.html')
    
    @app.route('/health')
    def health():
        """Endpoint de health check."""
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now().isoformat()
        })
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor iniciado em http://localhost:5000")
    print("📝 Acesse http://localhost:5000/formulario para preencher avaliação")
    app.run(debug=True, host='0.0.0.0', port=5000)

