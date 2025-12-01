from flask import Blueprint, request, jsonify
from services.internacao_service import InternacaoService

def init_internacao_routes(internacao_service: InternacaoService):
    internacao_bp = Blueprint('internacao_bp', __name__, url_prefix='/internacoes')

    @internacao_bp.route('/', methods=['GET'])
    def get_all_internacoes():
        try:
            internacoes = internacao_service.get_all_internacoes()
            # Converte objetos date para string para JSON
            for i in internacoes:
                if i.get('data_admissao'): i['data_admissao'] = i['data_admissao'].strftime('%Y-%m-%d')
                if i.get('data_alta_efetiva'): i['data_alta_efetiva'] = i['data_alta_efetiva'].strftime('%Y-%m-%d')
                if i.get('data_alta_prevista'): i['data_alta_prevista'] = i['data_alta_prevista'].strftime('%Y-%m-%d')
            return jsonify(internacoes), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/ativas', methods=['GET'])
    def get_active_internacoes():
        try:
            internacoes = internacao_service.get_active_internacoes()
            for i in internacoes:
                if i.get('data_admissao'): i['data_admissao'] = i['data_admissao'].strftime('%Y-%m-%d')
                if i.get('data_alta_prevista'): i['data_alta_prevista'] = i['data_alta_prevista'].strftime('%Y-%m-%d')
            return jsonify(internacoes), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/<int:id_internacao>', methods=['GET'])
    def get_internacao(id_internacao):
        try:
            internacao = internacao_service.get_internacao_by_id(id_internacao)
            if internacao.get('data_admissao'): internacao['data_admissao'] = internacao['data_admissao'].strftime('%Y-%m-%d')
            if internacao.get('data_alta_efetiva'): internacao['data_alta_efetiva'] = internacao['data_alta_efetiva'].strftime('%Y-%m-%d')
            if internacao.get('data_alta_prevista'): internacao['data_alta_prevista'] = internacao['data_alta_prevista'].strftime('%Y-%m-%d')
            return jsonify(internacao), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/', methods=['POST'])
    def create_internacao():
        data = request.get_json()
        required_fields = ['id_paciente', 'crm_medico', 'corem_enfermeiro']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            # Tratamento robusto para campos que podem vir vazios
            id_paciente = int(data['id_paciente'])
            
            # Trata id_quarto (se for string vazia ou None, vira None)
            id_quarto = data.get('id_quarto')
            if id_quarto and str(id_quarto).strip():
                id_quarto = int(id_quarto)
            else:
                id_quarto = None

            # Trata data_alta_prevista (se for string vazia, vira None)
            data_alta_prevista = data.get('data_alta_prevista')
            if not data_alta_prevista:
                data_alta_prevista = None

            result = internacao_service.create_internacao(
                id_paciente=id_paciente,
                crm_medico=data['crm_medico'],
                corem_enfermeiro=data['corem_enfermeiro'],
                id_quarto=id_quarto,
                data_admissao=data.get('data_admissao'),
                data_alta_prevista=data_alta_prevista
            )
            return jsonify(result), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/<int:id_internacao>', methods=['PUT'])
    def update_internacao(id_internacao):
        data = request.get_json()
        update_data = {}
        for key, value in data.items():
            # Filtra apenas os campos válidos
            if key in ["id_paciente", "crm_medico", "corem_enfermeiro", "id_quarto", "data_admissao", "data_alta_prevista"]:
                # Se for data_alta_prevista e vier vazio, converte para None
                if key == "data_alta_prevista" and not value:
                    update_data[key] = None
                else:
                    update_data[key] = value

        if not update_data:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            if 'id_paciente' in update_data: 
                update_data['id_paciente'] = int(update_data['id_paciente'])
            
            if 'id_quarto' in update_data:
                val = update_data['id_quarto']
                update_data['id_quarto'] = int(val) if val and str(val).strip() else None

            result = internacao_service.update_internacao(id_internacao, **update_data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrada" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/<int:id_internacao>/alta', methods=['POST'])
    def realizar_alta(id_internacao):
        data = request.get_json()
        data_alta_efetiva = data.get('data_alta_efetiva')

        if not data_alta_efetiva:
            return jsonify({"error": "Missing required field: data_alta_efetiva"}), 400

        try:
            result = internacao_service.realizar_alta(id_internacao, data_alta_efetiva)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrada" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @internacao_bp.route('/<int:id_internacao>', methods=['DELETE'])
    def delete_internacao(id_internacao):
        try:
            result = internacao_service.delete_internacao(id_internacao)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return internacao_bp