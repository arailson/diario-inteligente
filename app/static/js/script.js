/**
 * Diário Inteligente - JavaScript
 * Gerencia a interatividade do formulário de avaliação
 */

// Armazena as seleções
const selections = {
    work: null,
    training: null,
    studies: null,
    mind: null
};

// Inicializa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Formulário carregado');
    
    // Adiciona eventos aos botões de escala
    initializeScaleButtons();
    
    // Adiciona evento ao formulário
    const form = document.getElementById('evaluationForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Inicializa os botões de escala
 */
function initializeScaleButtons() {
    const buttons = document.querySelectorAll('.btn-scale');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const value = this.getAttribute('data-value');
            
            selectRating(this, category, value);
        });
    });
    
    console.log(`✅ ${buttons.length} botões inicializados`);
}

/**
 * Seleciona uma nota na escala
 */
function selectRating(element, category, value) {
    // Remove seleção anterior da mesma categoria
    const categoryButtons = document.querySelectorAll(`[data-category="${category}"]`);
    categoryButtons.forEach(button => {
        button.classList.remove('selected');
    });
    
    // Seleciona o botão clicado
    element.classList.add('selected');
    
    // Armazena a seleção
    selections[category] = value;
    
    console.log(`✅ ${category}: ${value}`);
}

/**
 * Valida o formulário
 */
function validateForm() {
    const errors = [];
    
    // Valida seleções de notas
    for (const [category, value] of Object.entries(selections)) {
        if (value === null) {
            errors.push(`Selecione uma nota para ${getCategoryName(category)}`);
        }
    }
    
    // Valida pontos positivos
    const positivePoints = document.getElementById('positive_points').value.trim();
    if (!positivePoints) {
        errors.push('Preencha os pontos positivos');
    }
    
    // Valida pontos negativos
    const negativePoints = document.getElementById('negative_points').value.trim();
    if (!negativePoints) {
        errors.push('Preencha os pontos negativos');
    }
    
    // Valida email
    const email = document.getElementById('userEmail').value.trim();
    if (!email) {
        errors.push('Email é obrigatório');
    }
    
    return errors;
}

/**
 * Obtém o nome amigável da categoria
 */
function getCategoryName(category) {
    const names = {
        work: 'Trabalho',
        training: 'Treino',
        studies: 'Estudos',
        mind: 'Estado Mental'
    };
    return names[category] || category;
}

/**
 * Mostra mensagem de erro
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Oculta após 5 segundos
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

/**
 * Mostra mensagem de sucesso
 */
function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Manipula o envio do formulário
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    console.log('📤 Enviando formulário...');
    
    // Valida o formulário
    const errors = validateForm();
    if (errors.length > 0) {
        showError(errors.join(', '));
        return;
    }
    
    // Desabilita o botão de envio
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Enviando...';
    
    // Prepara os dados
    const data = {
        work: parseInt(selections.work),
        training: parseInt(selections.training),
        studies: parseInt(selections.studies),
        mind: parseInt(selections.mind),
        positive_points: document.getElementById('positive_points').value.trim(),
        negative_points: document.getElementById('negative_points').value.trim(),
        email: document.getElementById('userEmail').value.trim()
    };
    
    console.log('📊 Dados:', data);
    
    try {
        // Envia os dados para o servidor
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            console.log('✅ Sucesso:', result);
            
            // Mostra mensagem de sucesso
            showSuccess('✅ Avaliação enviada com sucesso!');
            
            // Aguarda 2 segundos e redireciona
            setTimeout(() => {
                window.location.href = '/sucesso';
            }, 2000);
            
        } else {
            console.error('❌ Erro:', result);
            showError(result.error || 'Erro ao enviar avaliação');
            
            // Reabilita o botão
            submitBtn.disabled = false;
            submitBtn.textContent = '📤 Enviar Avaliação';
        }
        
    } catch (error) {
        console.error('❌ Erro de rede:', error);
        showError('Erro ao conectar com o servidor');
        
        // Reabilita o botão
        submitBtn.disabled = false;
        submitBtn.textContent = '📤 Enviar Avaliação';
    }
}

/**
 * Utilitário para debug
 */
window.getSelections = function() {
    console.log('Current selections:', selections);
    return selections;
};

