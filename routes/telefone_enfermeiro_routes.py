from flask import Blueprint, request, jsonify
from services.telefone_enfermeiro_service import TelefoneEnfermeiroService

def init_telefone_enfermeiro_routes(service: TelefoneEnfermeiroService):
    bp = Blueprint('telefone_enfermeiro_bp', __name__)

    @bp.route('/telefones/enfermeiros', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/telefones/enfermeiros/<corem>', methods=['GET'])
    def get_by_corem(corem):
        result = service.get_by_corem(corem)
        return jsonify(result if result else []), 200

    @bp.route('/telefones/enfermeiros', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(data['corem_enfermeiro'], data['numero_telefone'])
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/telefones/enfermeiros/<int:id_telefone>', methods=['PUT'])
    def update(id_telefone):
        data = request.get_json()
        return jsonify(service.update(id_telefone, data.get('numero_telefone'))), 200

    @bp.route('/telefones/enfermeiros/<int:id_telefone>', methods=['DELETE'])
    def delete(id_telefone):
        return jsonify(service.delete(id_telefone)), 200

    return bp