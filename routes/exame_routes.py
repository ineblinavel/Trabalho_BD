from flask import Blueprint, request, jsonify
from services.exame_service import ExameService

def init_exame_routes(exame_service: ExameService):
    exame_bp = Blueprint('exame_bp', __name__, url_prefix='/exames')

    @exame_bp.route('/', methods=['GET'])
    def get_all_exames():
        try:
            exames = exame_service.get_all_exames()
            # Converte objetos date para string para JSON
            for e in exames:
                if e.get('data_coleta'): e['data_coleta'] = e['data_coleta'].strftime('%Y-%m-%d')
                e['data_solicitacao'] = e['data_solicitacao'].strftime('%Y-%m-%d')
            return jsonify(exames), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @exame_bp.route('/<int:id_exame>', methods=['GET'])
    def get_exame_details(id_exame):
        try:
            exame = exame_service.get_exame_details_by_id(id_exame)
            # Converte objetos date para string para JSON
            if exame.get('data_coleta'): exame['data_coleta'] = exame['data_coleta'].strftime('%Y-%m-%d')
            exame['data_solicitacao'] = exame['data_solicitacao'].strftime('%Y-%m-%d')
            if exame.get('data_resultado'): exame['data_resultado'] = exame['data_resultado'].strftime('%Y-%m-%d')
            return jsonify(exame), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @exame_bp.route('/paciente/<int:id_paciente>/status/<string:status>', methods=['GET'])
    def get_exames_by_paciente_and_status(id_paciente, status):
        try:
            exames = exame_service.get_exames_by_paciente_and_status(id_paciente, status)
            for e in exames:
                if e.get('data_coleta'): e['data_coleta'] = e['data_coleta'].strftime('%Y-%m-%d')
                e['data_solicitacao'] = e['data_solicitacao'].strftime('%Y-%m-%d')
            return jsonify(exames), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @exame_bp.route('/', methods=['POST'])
    def create_exame():
        data = request.get_json()
        required_fields = ['status', 'crm_medico_responsavel', 'data_solicitacao', 'id_paciente', 'id_tipo_exame']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            id_paciente = int(data['id_paciente'])
            id_tipo_exame = int(data['id_tipo_exame'])

            result = exame_service.create_exame(
                status=data['status'],
                crm_medico_responsavel=data['crm_medico_responsavel'],
                data_solicitacao=data['data_solicitacao'],
                id_paciente=id_paciente,
                id_tipo_exame=id_tipo_exame,
                data_coleta=data.get('data_coleta')
            )
            return jsonify(result), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @exame_bp.route('/<int:id_exame>', methods=['PUT'])
    def update_exame(id_exame):
        data = request.get_json()
        update_data = {}
        for key, value in data.items():
            if key in ["status", "crm_medico_responsavel", "data_coleta", "data_solicitacao", "id_paciente", "id_tipo_exame"]:
                update_data[key] = value

        if not update_data:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            # Converte tipos se necessário antes de passar para o service
            if 'id_paciente' in update_data: update_data['id_paciente'] = int(update_data['id_paciente'])
            if 'id_tipo_exame' in update_data: update_data['id_tipo_exame'] = int(update_data['id_tipo_exame'])

            result = exame_service.update_exame(id_exame, **update_data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrado" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @exame_bp.route('/<int:id_exame>', methods=['DELETE'])
    def delete_exame(id_exame):
        try:
            result = exame_service.delete_exame(id_exame)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return exame_bp