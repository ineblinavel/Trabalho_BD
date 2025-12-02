from flask import Blueprint, request, jsonify, session
from services.telefone_enfermeiro_service import TelefoneEnfermeiroService

def init_telefone_enfermeiro_routes(service: TelefoneEnfermeiroService):
    # Definindo o prefixo base /telefones/enfermeiros
    bp = Blueprint('telefone_enfermeiro_bp', __name__, url_prefix='/telefones/enfermeiros')

    # Rota GET ALL corrigida
    @bp.route('/', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    # Rota GET BY COREM corrigida
    @bp.route('/<corem>', methods=['GET'])
    def get_by_corem(corem):
        result = service.get_by_corem(corem)
        return jsonify(result if result else []), 200

    # Rota POST corrigida
    @bp.route('/', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            caller = session.get('referencia_id')
            role = session.get('role')
            if role != 'admin' and caller != data.get('corem_enfermeiro'):
                return jsonify({'error': 'Operação não autorizada'}), 403

            res = service.create(data['corem_enfermeiro'], data['numero_telefone'])
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rotas PUT e DELETE corrigidas
    @bp.route('/<int:id_telefone>', methods=['PUT'])
    def update(id_telefone):
        data = request.get_json()
        registro = service.get_by_id(id_telefone)
        if not registro:
            return jsonify({'error': 'Registro não encontrado'}), 404
        caller = session.get('referencia_id')
        role = session.get('role')
        if role != 'admin' and caller != registro.get('corem_enfermeiro'):
            return jsonify({'error': 'Operação não autorizada'}), 403

        return jsonify(service.update(id_telefone, data.get('numero_telefone'))), 200

    @bp.route('/<int:id_telefone>', methods=['DELETE'])
    def delete(id_telefone):
        registro = service.get_by_id(id_telefone)
        if not registro:
            return jsonify({'error': 'Registro não encontrado'}), 404
        caller = session.get('referencia_id')
        role = session.get('role')
        if role != 'admin' and caller != registro.get('corem_enfermeiro'):
            return jsonify({'error': 'Operação não autorizada'}), 403

        return jsonify(service.delete(id_telefone)), 200

    return bp