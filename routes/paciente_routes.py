from flask import Blueprint, request, jsonify
from services.paciente_service import PacienteService
import base64 # <--- ESSENCIAL

def init_paciente_routes(paciente_service: PacienteService):
    paciente_bp = Blueprint('paciente_bp', __name__, url_prefix='/pacientes')

    @paciente_bp.route('/', methods=['GET'])
    def get_all_pacientes():
        try:
            pacientes = paciente_service.get_all_pacientes()

            for p in pacientes:
                # 1. Tratamento seguro de Data
                if p.get('data_nascimento') and hasattr(p['data_nascimento'], 'strftime'):
                    p['data_nascimento'] = p['data_nascimento'].strftime('%Y-%m-%d')

                # 2. Tratamento da Foto (Binário -> Base64)
                if p.get('foto'):
                    try:
                        # Converte os bytes do banco em string base64 para o HTML exibir
                        foto_bytes = p['foto']
                        if isinstance(foto_bytes, bytes):
                             # Decodifica se for bytes (padrão MySQL)
                            p['foto_base64'] = base64.b64encode(foto_bytes).decode('utf-8')
                        elif isinstance(foto_bytes, str):
                            # Se for string vazia, trata como nulo
                            p['foto_base64'] = None
                        else:
                             # Caso tipo inesperado
                             p['foto_base64'] = None

                        # Remove a chave 'foto' original para não poluir o JSON
                        del p['foto']

                    except Exception as img_err:
                        print(f"Erro ao processar imagem do paciente {p.get('id_paciente')}: {img_err}")
                        p['foto_base64'] = None
                else:
                    p['foto_base64'] = None

            return jsonify(pacientes), 200
        except Exception as e:
            # Imprime o erro no terminal do Flask para debug
            print(f"Erro crítico na rota GET /pacientes/: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/<int:id_paciente>', methods=['GET'])
    def get_paciente(id_paciente):
        try:
            paciente = paciente_service.get_paciente_by_id(id_paciente)
            if paciente and paciente.get('data_nascimento') and hasattr(paciente['data_nascimento'], 'strftime'):
                paciente['data_nascimento'] = paciente['data_nascimento'].strftime('%Y-%m-%d')
            return jsonify(paciente), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/<int:id_paciente>/historico', methods=['GET'])
    def get_paciente_historico(id_paciente):
        try:
            historico = paciente_service.get_paciente_historico(id_paciente)
            for h in historico:
                if h.get('data_evento') and hasattr(h['data_evento'], 'strftime'):
                    h['data_evento'] = h['data_evento'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(historico), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/', methods=['POST'])
    def create_paciente():
        data = request.get_json()
        required_fields = ['nome_paciente', 'cpf', 'data_nascimento', 'endereco']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            result = paciente_service.create_paciente(
                nome=data['nome_paciente'],
                cpf=data['cpf'],
                data_nascimento=data['data_nascimento'],
                endereco=data['endereco']
            )
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/<int:id_paciente>/foto', methods=['POST'])
    def update_foto(id_paciente):
        data = request.get_json()
        foto_base64 = data.get('foto_base64')

        if not foto_base64:
            return jsonify({"error": "Missing required field: foto_base64"}), 400

        try:
            # Decodifica Base64 para Bytes
            foto_data = base64.b64decode(foto_base64)
            result = paciente_service.update_foto(id_paciente, foto_data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/<int:id_paciente>/foto', methods=['GET'])
    def get_foto(id_paciente):
        try:
            foto_bytes = paciente_service.get_foto(id_paciente)
            if not foto_bytes:
                return jsonify({"message": "Foto não encontrada"}), 404

            foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
            return jsonify({"foto_base64": foto_base64}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @paciente_bp.route('/<int:id_paciente>', methods=['DELETE'])
    def delete_paciente(id_paciente):
        try:
            result = paciente_service.delete_paciente(id_paciente)
            return jsonify(result), 200
        except ValueError as e:
            # Erros de integridade/validação retornam 409 Conflict
            return jsonify({'error': str(e)}), 409
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return paciente_bp