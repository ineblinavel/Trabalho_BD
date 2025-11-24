from flask import Blueprint, request, jsonify
from services.medicamento_service import MedicamentoService

def init_medicamento_routes(medicamento_service: MedicamentoService):
    medicamento_bp = Blueprint('medicamento_bp', __name__, url_prefix='/medicamentos')

    @medicamento_bp.route('/', methods=['GET'])
    def get_all_medicamentos():
        try:
            medicamentos = medicamento_service.get_all_medicamentos()
            return jsonify(medicamentos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medicamento_bp.route('/<int:id_medicamento>', methods=['GET'])
    def get_medicamento(id_medicamento):
        try:
            medicamento = medicamento_service.get_medicamento_by_id(id_medicamento)
            return jsonify(medicamento), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medicamento_bp.route('/', methods=['POST'])
    def create_medicamento():
        data = request.get_json()
        required_fields = ['nome_comercial']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: nome_comercial"}), 400

        try:
            result = medicamento_service.create_medicamento(
                nome_comercial=data['nome_comercial'],
                fabricante=data.get('fabricante')
            )
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medicamento_bp.route('/<int:id_medicamento>', methods=['PUT'])
    def update_medicamento(id_medicamento):
        data = request.get_json()
        nome_comercial = data.get('nome_comercial')
        fabricante = data.get('fabricante')

        if not nome_comercial and not fabricante:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            result = medicamento_service.update_medicamento(
                id_medicamento=id_medicamento,
                nome_comercial=nome_comercial,
                fabricante=fabricante
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrado" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medicamento_bp.route('/<int:id_medicamento>', methods=['DELETE'])
    def delete_medicamento(id_medicamento):
        try:
            result = medicamento_service.delete_medicamento(id_medicamento)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            # Exceções como integridade referencial podem ser capturadas aqui
            return jsonify({'error': f"Erro ao deletar Medicamento: {str(e)}"}), 400

    return medicamento_bp