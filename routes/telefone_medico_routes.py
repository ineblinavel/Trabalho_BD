from flask import Blueprint, request, jsonify
from services.telefone_medico_service import TelefoneMedicoService

def init_telefone_medico_routes(service: TelefoneMedicoService):
    bp = Blueprint('telefone_medico_bp', __name__)

    @bp.route('/telefones/medicos', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/telefones/medicos/<crm>', methods=['GET'])
    def get_by_crm(crm):
        # Se o CRM for numérico/string, a rota captura.
        # Retorna lista de telefones do médico
        result = service.get_by_crm(crm)
        if result is not None: return jsonify(result), 200
        return jsonify([]), 200

    @bp.route('/telefones/medicos', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(data['crm_medico'], data['numero_telefone'])
            return jsonify(res), 201
        except KeyError as e:
             return jsonify({'error': f'Campo obrigatório faltando: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/telefones/medicos/<int:id_telefone>', methods=['PUT'])
    def update(id_telefone):
        data = request.get_json()
        return jsonify(service.update(id_telefone, data.get('numero_telefone'))), 200

    @bp.route('/telefones/medicos/<int:id_telefone>', methods=['DELETE'])
    def delete(id_telefone):
        return jsonify(service.delete(id_telefone)), 200

    return bp