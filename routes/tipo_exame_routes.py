from flask import Blueprint, request, jsonify
from services.tipo_exame_service import TipoExameService

def init_tipo_exame_routes(service: TipoExameService):
    bp = Blueprint('tipo_exame_bp', __name__)

    @bp.route('/tipos-exame', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/tipos-exame', methods=['POST'])
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

    @bp.route('/tipos-exame/<int:id_tipo>', methods=['PUT'])
    def update(id_tipo):
        return jsonify(service.update(id_tipo, request.get_json())), 200

    @bp.route('/tipos-exame/<int:id_tipo>', methods=['DELETE'])
    def delete(id_tipo):
        return jsonify(service.delete(id_tipo)), 200

    return bp