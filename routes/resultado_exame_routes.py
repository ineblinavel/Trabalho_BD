from flask import Blueprint, request, jsonify
from services.resultado_exame_service import ResultadoExameService

def init_resultado_exame_routes(service: ResultadoExameService):
    # Definindo o prefixo base /resultados-exame
    bp = Blueprint('resultado_exame_bp', __name__, url_prefix='/resultados-exame')

    # Rota GET ALL corrigida
    @bp.route('/', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    # Rota POST corrigida
    @bp.route('/', methods=['POST'])
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

    # PUT para atualizar um resultado
    @bp.route('/<int:id_resultado_exame>', methods=['PUT'])
    def update(id_resultado_exame):
        data = request.get_json()
        try:
            res = service.update(id_resultado_exame, data)
            return jsonify(res), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404 # Tratamento de "não encontrado" (esperado do service)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # DELETE para deletar um resultado
    @bp.route('/<int:id_resultado_exame>', methods=['DELETE'])
    def delete(id_resultado_exame):
        try:
            res = service.delete(id_resultado_exame)
            return jsonify(res), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404 # Tratamento de "não encontrado"
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return bp