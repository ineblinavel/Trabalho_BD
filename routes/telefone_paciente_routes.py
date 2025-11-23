from flask import Blueprint, request, jsonify
from services.telefone_paciente_service import TelefonePacienteService

def init_telefone_paciente_routes(service: TelefonePacienteService):
    bp = Blueprint('telefone_paciente_bp', __name__)

    @bp.route('/telefones/pacientes', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/telefones/pacientes/<int:id_paciente>', methods=['GET'])
    def get_by_paciente(id_paciente):
        result = service.get_by_paciente(id_paciente)
        return jsonify(result if result else []), 200

    @bp.route('/telefones/pacientes', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(int(data['id_paciente']), data['numero_telefone'])
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/telefones/pacientes/<int:id_telefone>', methods=['PUT'])
    def update(id_telefone):
        data = request.get_json()
        return jsonify(service.update(id_telefone, data.get('numero_telefone'))), 200

    @bp.route('/telefones/pacientes/<int:id_telefone>', methods=['DELETE'])
    def delete(id_telefone):
        return jsonify(service.delete(id_telefone)), 200

    return bp