from flask import Blueprint, request, jsonify
from services.relatorios_service import RelatoriosService

def init_relatorios_routes(service: RelatoriosService):
    bp = Blueprint('relatorios_bp', __name__)

    @bp.route('/relatorios/faturamento', methods=['GET'])
    def get_faturamento():
        ano = request.args.get('ano', type=int)
        mes = request.args.get('mes', type=int)
        try:
            dados = service.get_faturamento(ano, mes)
            return jsonify(dados), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return bp