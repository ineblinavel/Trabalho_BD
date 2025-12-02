from flask import Blueprint, request, jsonify, session
from services.enfermeiro_service import EnfermeiroService

def init_enfermeiro_routes(enfermeiro_service: EnfermeiroService):
    enfermeiro_bp = Blueprint('enfermeiro_bp', __name__, url_prefix='/enfermeiros')

    @enfermeiro_bp.route('/', methods=['GET'])
    def get_all_enfermeiros():
        try:
            enfermeiros = enfermeiro_service.get_all_enfermeiros()
            return jsonify(enfermeiros), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @enfermeiro_bp.route('/<string:corem>', methods=['GET'])
    def get_enfermeiro(corem):
        try:
            enfermeiro = enfermeiro_service.get_enfermeiro_by_corem(corem)
            return jsonify(enfermeiro), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @enfermeiro_bp.route('/', methods=['POST'])
    def create_enfermeiro():
        data = request.get_json()
        required_fields = ['corem', 'cpf', 'nome_enfermeiro']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            result = enfermeiro_service.create_enfermeiro(
                corem=data['corem'],
                cpf=data['cpf'],
                nome_enfermeiro=data['nome_enfermeiro']
            )
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @enfermeiro_bp.route('/<string:corem>', methods=['PUT'])
    def update_enfermeiro(corem):
        data = request.get_json()
        cpf = data.get('cpf')
        nome_enfermeiro = data.get('nome_enfermeiro')

        if not cpf and not nome_enfermeiro:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            result = enfermeiro_service.update_enfermeiro(
                corem=corem,
                cpf=cpf,
                nome_enfermeiro=nome_enfermeiro
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrado" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @enfermeiro_bp.route('/<string:corem>', methods=['DELETE'])
    def delete_enfermeiro(corem):
        # Apenas admins podem deletar enfermeiros via API
        if session.get('role') != 'admin':
            return jsonify({'error': 'Operação não autorizada'}), 403
        try:
            result = enfermeiro_service.delete_enfermeiro(corem)
            return jsonify(result), 200
        except ValueError as e:
            # Erros de validação ou integridade referencial são retornados como 409 (Conflict)
            return jsonify({'error': str(e)}), 409
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return enfermeiro_bp