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
            medicos = medico_service.get_all_medicos()
            return jsonify(medicos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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

    return medico_bp
