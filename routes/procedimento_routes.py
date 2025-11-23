from flask import Blueprint, request, jsonify
from services.procedimento_service import ProcedimentoService

def init_procedimento_routes(service: ProcedimentoService):
    bp = Blueprint('procedimento_bp', __name__)

    @bp.route('/procedimentos', methods=['GET'])
    def get_all():
        return jsonify(service.get_all()), 200

    @bp.route('/procedimentos/<int:id_procedimento>', methods=['GET'])
    def get_one(id_procedimento):
        result = service.get_by_id(id_procedimento)
        if result: return jsonify(result), 200
        return jsonify({'message': 'Não encontrado'}), 404

    @bp.route('/procedimentos', methods=['POST'])
    def create():
        data = request.get_json()
        try:
            res = service.create(
                data['crm_medico'], 
                int(data['id_paciente']), 
                data['nome_procedimento'], 
                float(data['custo'])
            )
            return jsonify(res), 201
        except KeyError as e:
            return jsonify({'error': f'Campo obrigatório faltando: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/procedimentos/<int:id_procedimento>', methods=['PUT'])
    def update(id_procedimento):
        return jsonify(service.update(id_procedimento, request.get_json())), 200

    @bp.route('/procedimentos/<int:id_procedimento>', methods=['DELETE'])
    def delete(id_procedimento):
        return jsonify(service.delete(id_procedimento)), 200

    return bp