from flask import Blueprint, jsonify, request
from services.log_salario_service import LogSalarioService

def init_log_salario_routes(service: LogSalarioService):
    bp = Blueprint('log_salario_bp', __name__, url_prefix='/logs-salario')

    @bp.route('/', methods=['GET'])
    def get_all():
        try:
            crm = request.args.get('crm')
            logs = service.get_all_logs(crm)
            # Convert datetime to string
            for log in logs:
                if log.get('data_alteracao'):
                    log['data_alteracao'] = log['data_alteracao'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(logs), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return bp
