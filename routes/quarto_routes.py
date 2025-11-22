from flask import Blueprint, request, jsonify
from services.quarto_service import QuartoService

def init_quarto_routes(service: QuartoService):
    bp = Blueprint('quarto_bp', __name__)

    @bp.route('/quartos', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/quartos/mapa', methods=['GET'])
    def get_mapa():
        return jsonify(service.get_mapa_leitos()), 200

    @bp.route('/quartos/<int:num_quarto>', methods=['GET'])
    def get_one(num_quarto):
        result = service.get_by_id(num_quarto)
        if result: return jsonify(result), 200
        return jsonify({'message': 'Quarto não encontrado'}), 404

    @bp.route('/quartos', methods=['POST'])
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

    @bp.route('/quartos/<int:num_quarto>', methods=['PUT'])
    def update(num_quarto):
        return jsonify(service.update(num_quarto, request.get_json())), 200

    return bp