from flask import Flask, render_template, request, jsonify, send_file
import os
import io
from datetime import datetime

app = Flask(__name__)

# ========== ROTAS PRINCIPAIS ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modulos-treinamento')
def modulos_treinamento():
    return render_template('modulos_treinamento.html')

@app.route('/gerador-provas')
def gerador_provas():
    return render_template('gerador_provas.html')

@app.route('/planejador-aulas')
def planejador_aulas():
    return render_template('planejador_aulas.html')

@app.route('/adaptacao-aee')
def adaptacao_aee():
    return render_template('adaptacao_aee.html')

@app.route('/guia-rapido')
def guia_rapido():
    return render_template('guia_rapido.html')

@app.route('/correcao-redacoes')
def correcao_redacoes():
    return render_template('correcao_redacoes.html')

# ========== MÓDULOS COGNITIVOS EXISTENTES ==========

@app.route('/memoria')
def memoria():
    return render_template('memoria.html')

@app.route('/atencao')
def atencao():
    return render_template('atencao.html')

@app.route('/linguagem')
def linguagem():
    return render_template('linguagem.html')

@app.route('/raciocinio')
def raciocinio():
    return render_template('raciocinio.html')

# ========== APIs PARA GERADOR DE PROVAS ==========

@app.route('/api/gerar-prompt-prova', methods=['POST'])
def gerar_prompt_prova():
    """Gera prompt para criação de provas"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('disciplina') or not data.get('nivel'):
            return jsonify({'error': 'Disciplina e nível são obrigatórios'}), 400
        
        # Gerar prompt baseado nos dados
        prompt = criar_prompt_prova(data)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'message': 'Prompt gerado com sucesso!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/processar-resposta-ia', methods=['POST'])
def processar_resposta_ia():
    """Processa resposta da IA e separa prova/gabarito"""
    try:
        data = request.get_json()
        resposta_ia = data.get('resposta', '')
        
        if not resposta_ia.strip():
            return jsonify({'error': 'Resposta da IA não pode estar vazia'}), 400
        
        # Processar e separar conteúdo
        resultado = processar_conteudo_ia(resposta_ia)
        
        return jsonify({
            'success': True,
            'prova': resultado['prova'],
            'gabarito': resultado['gabarito'],
            'tem_gabarito': resultado['tem_gabarito']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== APIs PARA PLANEJADOR DE AULAS ==========

@app.route('/api/gerar-prompt-aula', methods=['POST'])
def gerar_prompt_aula():
    """Gera prompt para criação de planos de aula"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('disciplina') or not data.get('tema'):
            return jsonify({'error': 'Disciplina e tema são obrigatórios'}), 400
        
        # Gerar prompt baseado nos dados
        prompt = criar_prompt_aula(data)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'message': 'Prompt gerado com sucesso!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/processar-plano-aula', methods=['POST'])
def processar_plano_aula():
    """Processa resposta da IA para plano de aula"""
    try:
        data = request.get_json()
        resposta_ia = data.get('resposta', '')
        
        if not resposta_ia.strip():
            return jsonify({'error': 'Resposta da IA não pode estar vazia'}), 400
        
        # Processar conteúdo
        plano_formatado = formatar_plano_aula(resposta_ia)
        
        return jsonify({
            'success': True,
            'plano': plano_formatado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== APIs PARA ADAPTAÇÃO AEE ==========

@app.route('/api/gerar-prompt-aee', methods=['POST'])
def gerar_prompt_aee():
    """Gera prompt para adaptação AEE"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('conteudo_original') or not data.get('deficiencia'):
            return jsonify({'error': 'Conteúdo original e tipo de deficiência são obrigatórios'}), 400
        
        # Gerar prompt baseado nos dados
        prompt = criar_prompt_aee(data)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'message': 'Prompt de adaptação gerado com sucesso!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== DOWNLOAD DE ARQUIVOS ==========

@app.route('/api/download/<tipo>')
def download_arquivo(tipo):
    """Download de arquivos gerados"""
    try:
        conteudo = request.args.get('conteudo', '')
        
        if not conteudo:
            return jsonify({'error': 'Conteúdo não fornecido'}), 400
        
        # Definir nome do arquivo baseado no tipo
        nomes_arquivo = {
            'prova': 'prova.txt',
            'gabarito': 'gabarito.txt',
            'plano-aula': 'plano_de_aula.txt',
            'material-aee': 'material_adaptado_aee.txt'
        }
        
        nome_arquivo = nomes_arquivo.get(tipo, 'arquivo.txt')
        
        # Criar arquivo em memória
        arquivo_io = io.BytesIO()
        arquivo_io.write(conteudo.encode('utf-8'))
        arquivo_io.seek(0)
        
        return send_file(
            arquivo_io,
            as_attachment=True,
            download_name=nome_arquivo,
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== FUNÇÕES AUXILIARES ==========

def criar_prompt_prova(data):
    """Cria prompt para geração de provas"""
    prompt_lines = []
    
    prompt_lines.append("GERAR PROVA DETALHADA")
    prompt_lines.append("\n**Contexto da Prova:**")
    
    if data.get('escola'):
        prompt_lines.append(f"- Escola: {data['escola']}")
    if data.get('professor'):
        prompt_lines.append(f"- Professor: {data['professor']}")
    
    prompt_lines.append(f"- Disciplina: {data['disciplina']}")
    prompt_lines.append(f"- Nível/Etapa de Ensino: {data['nivel']}")
    
    if data.get('turma'):
        prompt_lines.append(f"- Turma: {data['turma']}")
    
    prompt_lines.append("\n**Estrutura da Prova:**")
    
    if data.get('num_questoes'):
        prompt_lines.append(f"- Número Total de Questões: {data['num_questoes']}")
    
    if data.get('tipos_questao'):
        tipos = ', '.join(data['tipos_questao'])
        prompt_lines.append(f"- Tipos de Questão: {tipos}")
    
    if data.get('topicos_conteudos'):
        prompt_lines.append(f"- Tópicos/Conteúdos a Cobrir: {data['topicos_conteudos']}")
    
    prompt_lines.append("\n**Foco Pedagógico:**")
    
    dificuldade = data.get('dificuldade', 'Balanceado (Foco Médio)')
    prompt_lines.append(f"- Nível de Dificuldade: {dificuldade}")
    
    if data.get('habilidades_avaliar'):
        prompt_lines.append(f"- Habilidades Cognitivas: {data['habilidades_avaliar']}")
    
    if data.get('bncc_alignment') and 'Sim' in data['bncc_alignment']:
        prompt_lines.append(f"- Alinhamento BNCC: Garantir alinhamento com habilidades da BNCC para {data['disciplina']} - {data['nivel']}")
    
    if data.get('tempo_resolucao'):
        prompt_lines.append(f"\n**Tempo:** {data['tempo_resolucao']} minutos")
    
    if data.get('sistema_pontuacao'):
        prompt_lines.append(f"**Pontuação:** {data['sistema_pontuacao']}")
    
    prompt_lines.append("\n**Instrução Final:** Elabore a prova seguindo as diretrizes acima, garantindo clareza e adequação ao público-alvo. Inclua um gabarito detalhado com justificativas.")
    
    return '\n'.join(prompt_lines)

def criar_prompt_aula(data):
    """Cria prompt para geração de planos de aula"""
    prompt_lines = []
    
    prompt_lines.append("CRIAR PLANO DE AULA DETALHADO")
    prompt_lines.append("\n**Dados Essenciais:**")
    
    if data.get('escola'):
        prompt_lines.append(f"- Escola: {data['escola']}")
    if data.get('professor'):
        prompt_lines.append(f"- Professor: {data['professor']}")
    
    prompt_lines.append(f"- Disciplina: {data['disciplina']}")
    prompt_lines.append(f"- Tema Central: {data['tema']}")
    prompt_lines.append(f"- Nível/Etapa: {data['nivel']}")
    
    if data.get('turma'):
        prompt_lines.append(f"- Turma: {data['turma']}")
    
    prompt_lines.append("\n**Objetivos de Aprendizagem:**")
    if data.get('objetivos'):
        prompt_lines.append(f"{data['objetivos']}")
    
    prompt_lines.append("\n**Conteúdos Específicos:**")
    if data.get('conteudos'):
        prompt_lines.append(f"{data['conteudos']}")
    
    prompt_lines.append("\n**Metodologia:**")
    if data.get('metodologia'):
        prompt_lines.append(f"- Estratégias: {data['metodologia']}")
    
    if data.get('recursos'):
        prompt_lines.append(f"- Recursos: {data['recursos']}")
    
    if data.get('atividades'):
        prompt_lines.append(f"- Atividades: {data['atividades']}")
    
    prompt_lines.append("\n**Avaliação:**")
    if data.get('avaliacao'):
        prompt_lines.append(f"{data['avaliacao']}")
    
    if data.get('duracao'):
        prompt_lines.append(f"\n**Duração:** {data['duracao']}")
    
    if data.get('bncc') and 'Sim' in data['bncc']:
        prompt_lines.append(f"\n**BNCC:** Garantir alinhamento com competências da BNCC para {data['disciplina']}")
    
    if data.get('observacoes'):
        prompt_lines.append(f"\n**Observações:** {data['observacoes']}")
    
    prompt_lines.append("\n**Instrução Final:** Elabore um plano de aula completo e funcional, detalhando atividades e garantindo coerência pedagógica.")
    
    return '\n'.join(prompt_lines)

def criar_prompt_aee(data):
    """Cria prompt para adaptação AEE"""
    prompt_lines = []
    
    prompt_lines.append("ADAPTAÇÃO PARA ATENDIMENTO EDUCACIONAL ESPECIALIZADO (AEE)")
    prompt_lines.append("\n**Perfil do Estudante:**")
    
    if data.get('idade'):
        prompt_lines.append(f"- Idade/Série: {data['idade']}")
    
    prompt_lines.append(f"- Tipo de Deficiência/Necessidade: {data['deficiencia']}")
    
    if data.get('caracteristicas'):
        prompt_lines.append(f"- Características Específicas: {data['caracteristicas']}")
    
    prompt_lines.append("\n**Material Original:**")
    prompt_lines.append(f"- Disciplina: {data.get('disciplina', 'Não especificada')}")
    prompt_lines.append(f"- Tipo de Material: {data.get('tipo_material', 'Não especificado')}")
    
    if data.get('objetivos'):
        prompt_lines.append(f"- Objetivos: {data['objetivos']}")
    
    prompt_lines.append(f"\n**Conteúdo a ser Adaptado:**")
    prompt_lines.append(f"{data['conteudo_original']}")
    
    prompt_lines.append("\n**Adaptações Solicitadas:**")
    prompt_lines.append(f"- Nível de Adaptação: {data.get('nivel_adaptacao', 'Não especificado')}")
    
    if data.get('tipos_adaptacao'):
        adaptacoes = ', '.join(data['tipos_adaptacao'])
        prompt_lines.append(f"- Tipos de Adaptação: {adaptacoes}")
    
    if data.get('recursos_especificos'):
        prompt_lines.append(f"- Recursos Específicos: {data['recursos_especificos']}")
    
    if data.get('estrategias'):
        prompt_lines.append(f"- Estratégias Pedagógicas: {data['estrategias']}")
    
    prompt_lines.append("\n**Instrução Final:** Adapte o material mantendo os objetivos educacionais, mas tornando-o acessível e adequado às necessidades específicas do estudante. Inclua sugestões de implementação.")
    
    return '\n'.join(prompt_lines)

def processar_conteudo_ia(resposta_ia):
    """Processa resposta da IA e separa prova/gabarito"""
    import re
    
    # Remove formatação Markdown básica
    resposta_limpa = re.sub(r'\*\*(.*?)\*\*|__(.*?)__|---+', r'\1\2', resposta_ia)
    resposta_limpa = re.sub(r'^[#]{1,6}\s*(.*)$', r'\1', resposta_limpa, flags=re.MULTILINE)
    
    # Tenta separar gabarito
    gabarito_regex = r'(GABARITO|RESPOSTAS|SOLUÇÕES|RESOLUÇÃO|GABARITO OFICIAL)(:?)(?!.*(GABARITO|RESPOSTAS|SOLUÇÕES|RESOLUÇÃO|GABARITO OFICIAL))\n([\s\S]*)'
    match = re.search(gabarito_regex, resposta_limpa, re.IGNORECASE)
    
    if match:
        prova_content = resposta_limpa[:match.start()].strip()
        gabarito_content = match.group(4).strip() if match.group(4) else ""
        
        # Verifica se a separação faz sentido
        if len(prova_content) > 50 and len(gabarito_content) > 10:
            return {
                'prova': prova_content,
                'gabarito': gabarito_content,
                'tem_gabarito': True
            }
    
    # Se não conseguiu separar, retorna tudo como prova
    return {
        'prova': resposta_limpa,
        'gabarito': '',
        'tem_gabarito': False
    }

def formatar_plano_aula(resposta_ia):
    """Formata resposta da IA para plano de aula"""
    import re
    
    # Remove formatação Markdown básica
    resposta_limpa = re.sub(r'\*\*(.*?)\*\*|__(.*?)__|---+', r'\1\2', resposta_ia)
    resposta_limpa = re.sub(r'^[#]{1,6}\s*(.*)$', r'\1', resposta_limpa, flags=re.MULTILINE)
    
    return resposta_limpa.strip()

if __name__ == '__main__':
    app.run(debug=True)