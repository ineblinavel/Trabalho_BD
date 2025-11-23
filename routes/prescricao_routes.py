from flask import Blueprint, request, jsonify
from services.prescricao_service import PrescricaoService

def init_prescricao_routes(prescricao_service: PrescricaoService):
    # O prefixo base é definido aqui: /prescricoes
    prescricao_bp = Blueprint('prescricao_bp', __name__, url_prefix='/prescricoes')

    # Rota para listar todas as prescrições
    @prescricao_bp.route('/', methods=['GET'])
    def get_prescricoes():
        try:
            prescricoes = prescricao_service.get_all_prescricoes()
            return jsonify(prescricoes), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rota para buscar uma prescrição específica por ID
    @prescricao_bp.route('/<int:id_prescricao>', methods=['GET'])
    def get_prescricao(id_prescricao):
        try:
            prescricao = prescricao_service.get_prescricao_by_id(id_prescricao)
            if prescricao:
                return jsonify(prescricao), 200
            return jsonify({'message': 'Prescrição não encontrada'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rota para criar uma nova prescrição
    @prescricao_bp.route('/', methods=['POST'])
    def create_prescricao():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        # Campos obrigatórios baseados no repositório
        id_consulta = data.get('id_consulta')
        id_medicamento = data.get('id_medicamento')
        quantidade_prescrita = data.get('quantidade_prescrita')

        # Campos opcionais
        dosagem = data.get('dosagem')
        frequencia_uso = data.get('frequencia_uso')

        if not all([id_consulta, id_medicamento, quantidade_prescrita]):
            return jsonify({"error": "Campos obrigatórios: id_consulta, id_medicamento, quantidade_prescrita"}), 400

        try:
            result = prescricao_service.create_prescricao(
                int(id_consulta),
                int(id_medicamento),
                int(quantidade_prescrita),
                dosagem,
                frequencia_uso
            )
            return jsonify(result), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rota para atualizar uma prescrição existente
    @prescricao_bp.route('/<int:id_prescricao>', methods=['PUT'])
    def update_prescricao(id_prescricao):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        try:
            # Passamos o dicionário 'data' diretamente para o serviço filtrar os campos
            result = prescricao_service.update_prescricao(id_prescricao, data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rota para deletar uma prescrição
    @prescricao_bp.route('/<int:id_prescricao>', methods=['DELETE'])
    def delete_prescricao(id_prescricao):
        try:
            result = prescricao_service.delete_prescricao(id_prescricao)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return prescricao_bp