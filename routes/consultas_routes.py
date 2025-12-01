from flask import Blueprint, request, jsonify
from services.consultas_service import ConsultasService

def init_consultas_routes(consulta_service: ConsultasService):
    consulta_bp = Blueprint('consulta_bp', __name__, url_prefix='/consultas')

    @consulta_bp.route('/', methods=['GET'])
    def get_all_consultas():
        try:
            consultas = consulta_service.get_all_consultas()
            # Converte objetos datetime para string para JSON
            for c in consultas:
                c['data_hora_agendamento'] = c['data_hora_agendamento'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(consultas), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @consulta_bp.route('/<int:id_consulta>', methods=['GET'])
    def get_consulta(id_consulta):
        try:
            consulta = consulta_service.get_consulta_by_id(id_consulta)
            consulta['data_hora_agendamento'] = consulta['data_hora_agendamento'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(consulta), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @consulta_bp.route('/medico/<string:crm>', methods=['GET'])
    def get_consultas_medico(crm):
        try:
            consultas = consulta_service.get_consultas_by_medico(crm)
            for c in consultas:
                if c.get('data_hora_agendamento'):
                    c['data_hora_agendamento'] = c['data_hora_agendamento'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(consultas), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @consulta_bp.route('/', methods=['POST'])
    def create_consulta():
        data = request.get_json()
        required_fields = ['crm_medico', 'id_paciente', 'data_hora_agendamento']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            id_paciente = int(data['id_paciente'])
            result = consulta_service.create_consulta(
                crm=data['crm_medico'],
                id_paciente=id_paciente,
                data_hora=data['data_hora_agendamento']
            )
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @consulta_bp.route('/<int:id_consulta>', methods=['PUT'])
    def update_consulta(id_consulta):
        data = request.get_json()
        status = data.get('status')
        data_hora = data.get('data_hora_agendamento')
        diagnostico = data.get('diagnostico')

        if not any([status, data_hora, diagnostico]): # Verifica se pelo menos um foi enviado
            return jsonify({"error": "No data provided for update"}), 400

        try:
            result = consulta_service.update_consulta(
                id_consulta=id_consulta,
                status=status,
                data_hora=data_hora,
                diagnostico=diagnostico
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @consulta_bp.route('/<int:id_consulta>', methods=['DELETE'])
    def delete_consulta(id_consulta):
        try:
            result = consulta_service.delete_consulta(id_consulta)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return consulta_bp