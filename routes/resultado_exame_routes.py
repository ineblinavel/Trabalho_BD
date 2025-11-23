from flask import Blueprint, request, jsonify
from services.resultado_exame_service import ResultadoExameService

def init_resultado_exame_routes(service: ResultadoExameService):
    bp = Blueprint('resultado_exame_bp', __name__)

    @bp.route('/resultados-exame', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/resultados-exame', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            # id_exame, resultado_obtido, data_resultado (YYYY-MM-DD)
            res = service.create(
                int(data['id_exame']), 
                data['resultado_obtido'], 
                data['data_resultado']
            )
            return jsonify(res), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return bp