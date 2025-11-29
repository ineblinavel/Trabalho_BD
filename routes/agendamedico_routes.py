from flask import Blueprint, request, jsonify
from services.agendamedico_service import AgendaMedicoService

def init_agendamedico_routes(agenda_service: AgendaMedicoService):
    agenda_bp = Blueprint('agenda_bp', __name__, url_prefix='/agenda')

    @agenda_bp.route('/', methods=['GET'])
    def get_all_agendas():
        try:
            agendas = agenda_service.get_all_agendas()
            # Converte objetos date/time para string para JSON
            result = []
            for a in agendas:
                a['data'] = a['data'].strftime('%Y-%m-%d')
                a['inicio_platao'] = str(a['inicio_platao'])
                a['fim_platao'] = str(a['fim_platao'])
                result.append(a)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/<int:id_agenda>', methods=['GET'])
    def get_agenda(id_agenda):
        try:
            agenda = agenda_service.get_agenda_by_id(id_agenda)
            agenda['data'] = agenda['data'].strftime('%Y-%m-%d')
            agenda['inicio_platao'] = str(agenda['inicio_platao'])
            agenda['fim_platao'] = str(agenda['fim_platao'])
            return jsonify(agenda), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/<int:id_agenda>/slots', methods=['GET'])
    def get_available_slots(id_agenda):
        try:
            slots = agenda_service.get_available_slots(id_agenda)
            return jsonify(slots), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/', methods=['POST'])
    def create_agenda():
        data = request.get_json()
        required_fields = ['crm_medico', 'data', 'inicio_platao', 'fim_platao', 'duracao_slot_minutos']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            duracao = int(data['duracao_slot_minutos'])
            result = agenda_service.create_agenda(
                crm=data['crm_medico'],
                data=data['data'],
                inicio=data['inicio_platao'],
                fim=data['fim_platao'],
                duracao=duracao
            )
            return jsonify(result), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/<int:id_agenda>', methods=['PUT'])
    def update_agenda(id_agenda):
        data = request.get_json()
        required_fields = ['data', 'inicio_platao', 'fim_platao', 'duracao_slot_minutos']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            duracao = int(data['duracao_slot_minutos'])
            result = agenda_service.update_agenda(
                id_agenda=id_agenda,
                data=data['data'],
                inicio=data['inicio_platao'],
                fim=data['fim_platao'],
                duracao=duracao
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrada" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/<int:id_agenda>', methods=['DELETE'])
    def delete_agenda(id_agenda):
        try:
            result = agenda_service.delete_agenda(id_agenda)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @agenda_bp.route('/medico/<string:crm>', methods=['GET'])
    def get_agendas_by_medico(crm):
        try:
            agendas = agenda_service.get_agendas_by_medico(crm)
            result = []
            for a in agendas:
                a['data'] = a['data'].strftime('%Y-%m-%d')
                a['inicio_platao'] = str(a['inicio_platao'])
                a['fim_platao'] = str(a['fim_platao'])
                result.append(a)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return agenda_bp