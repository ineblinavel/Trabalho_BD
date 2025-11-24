from flask import Blueprint, request, jsonify
from services.quarto_service import QuartoService

def init_quarto_routes(service: QuartoService):
    # Definindo o prefixo base /quartos
    bp = Blueprint('quarto_bp', __name__, url_prefix='/quartos')

    # Rota GET ALL corrigida
    @bp.route('/', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    # Rota GET MAPA corrigida
    @bp.route('/mapa', methods=['GET'])
    def get_mapa():
        return jsonify(service.get_mapa_leitos()), 200

    # Rota GET ONE corrigida
    @bp.route('/<int:num_quarto>', methods=['GET'])
    def get_one(num_quarto):
        result = service.get_by_id(num_quarto)
        if result: return jsonify(result), 200
        return jsonify({'message': 'Quarto não encontrado'}), 404

    # Rota POST corrigida
    @bp.route('/', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(
                int(data['num_quarto']),
                data['tipo_de_quarto'],
                float(data['valor_diaria'])
            )
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Rota PUT corrigida
    @bp.route('/<int:num_quarto>', methods=['PUT'])
    def update(num_quarto):
        return jsonify(service.update(num_quarto, request.get_json())), 200

    return bp