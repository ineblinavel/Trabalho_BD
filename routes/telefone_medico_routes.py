from flask import Blueprint, request, jsonify, session
from services.telefone_medico_service import TelefoneMedicoService

def init_telefone_medico_routes(service: TelefoneMedicoService):
    # Definindo o prefixo base /telefones/medicos
    bp = Blueprint('telefone_medico_bp', __name__, url_prefix='/telefones/medicos')

    # Rota GET ALL corrigida
    @bp.route('/', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    # Rota GET BY CRM corrigida
    @bp.route('/<crm>', methods=['GET'])
    def get_by_crm(crm):
        # Se o CRM for numérico/string, a rota captura.
        # Retorna lista de telefones do médico
        result = service.get_by_crm(crm)
        if result is not None: return jsonify(result), 200
        return jsonify([]), 200

    # Rota POST corrigida
    @bp.route('/', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            # Permitir apenas que o próprio médico (ou admin) cadastre seus telefones
            caller = session.get('referencia_id')
            role = session.get('role')
            if role != 'admin' and caller != data.get('crm_medico'):
                return jsonify({'error': 'Operação não autorizada'}), 403

            res = service.create(data['crm_medico'], data['numero_telefone'])
            return jsonify(res), 201
        except KeyError as e:
             return jsonify({'error': f'Campo obrigatório faltando: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rotas PUT e DELETE corrigidas
    @bp.route('/<int:id_telefone>', methods=['PUT'])
    def update(id_telefone):
        data = request.get_json()
        # Verifica se o telefone pertence ao usuário autenticado (ou admin)
        registro = service.get_by_id(id_telefone)
        if not registro:
            return jsonify({'error': 'Registro não encontrado'}), 404
        caller = session.get('referencia_id')
        role = session.get('role')
        if role != 'admin' and caller != registro.get('crm_medico'):
            return jsonify({'error': 'Operação não autorizada'}), 403

        return jsonify(service.update(id_telefone, data.get('numero_telefone'))), 200

    @bp.route('/<int:id_telefone>', methods=['DELETE'])
    def delete(id_telefone):
        registro = service.get_by_id(id_telefone)
        if not registro:
            return jsonify({'error': 'Registro não encontrado'}), 404
        caller = session.get('referencia_id')
        role = session.get('role')
        if role != 'admin' and caller != registro.get('crm_medico'):
            return jsonify({'error': 'Operação não autorizada'}), 403

        return jsonify(service.delete(id_telefone)), 200

    return bp