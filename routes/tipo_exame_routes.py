from flask import Blueprint, request, jsonify
from services.tipo_exame_service import TipoExameService

def init_tipo_exame_routes(service: TipoExameService):
    # Definindo o prefixo base /tipos-exame
    bp = Blueprint('tipo_exame_bp', __name__, url_prefix='/tipos-exame')

    # Rota GET ALL corrigida
    @bp.route('/', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    # Rota POST corrigida
    @bp.route('/', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(
                data['nome_do_exame'],
                float(data['preco']),
                data.get('descricao')
            )
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rotas PUT e DELETE corrigidas
    @bp.route('/<int:id_tipo>', methods=['PUT'])
    def update(id_tipo):
        return jsonify(service.update(id_tipo, request.get_json())), 200

    @bp.route('/<int:id_tipo>', methods=['DELETE'])
    def delete(id_tipo):
        return jsonify(service.delete(id_tipo)), 200

    return bp