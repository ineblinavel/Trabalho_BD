from flask import Blueprint, request, jsonify, render_template
from services.medico_service import MedicoService

def init_medico_routes(medico_service: MedicoService):
    medico_bp = Blueprint('medico_bp', __name__, template_folder='templates', static_folder='static',url_prefix='/medicos')

    @medico_bp.route('/', methods=['GET'])
    def index():
        return render_template('add_medico.html')

    @medico_bp.route('/medicos', methods=['GET'])
    def get_medicos():
        try:
            include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
            medicos = medico_service.get_all_medicos(include_inactive=include_inactive)
            return jsonify(medicos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medico_bp.route('/<string:crm>', methods=['GET'])
    def get_medico(crm):
        try:
            medico = medico_service.get_medico_by_crm(crm)
            if medico:
                return jsonify(medico), 200
            return jsonify({'error': 'Médico não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medico_bp.route('', methods=['POST'])
    @medico_bp.route('/', methods=['POST'])
    @medico_bp.route('/medicos', methods=['POST'])
    def create_medico():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        crm = data.get('crm')
        nome_medico = data.get('nome_medico')
        cpf = data.get('cpf')
        salario = data.get('salario')

        if not all([crm, nome_medico, cpf, salario]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            salario = float(salario)
            result = medico_service.create_medico(crm, nome_medico, cpf, salario)
            return jsonify(result), 201
        except ValueError:
            return jsonify({"error": "Salario must be a valid number"}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medico_bp.route('/<string:crm>', methods=['PUT'])
    def update_medico(crm):
        data = request.get_json()
        try:
            result = medico_service.update_medico(
                crm,
                nome_medico=data.get('nome_medico'),
                cpf=data.get('cpf'),
                salario=data.get('salario')
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medico_bp.route('/<string:crm>', methods=['DELETE'])
    def delete_medico(crm):
        try:
            result = medico_service.delete_medico(crm)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @medico_bp.route('/<string:crm>/reactivate', methods=['POST'])
    def reactivate_medico(crm):
        try:
            result = medico_service.reactivate_medico(crm)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return medico_bp
