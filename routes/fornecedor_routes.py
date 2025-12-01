from flask import Blueprint, request, jsonify
from services.fornecedor_service import FornecedorService

def init_fornecedor_routes(fornecedor_service: FornecedorService):
    fornecedor_bp = Blueprint('fornecedor_bp', __name__, url_prefix='/fornecedores')

    @fornecedor_bp.route('/', methods=['GET'])
    def get_all_fornecedores():
        try:
            fornecedores = fornecedor_service.get_all_fornecedores()
            return jsonify(fornecedores), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fornecedor_bp.route('/<path:cnpj>', methods=['GET'])
    def get_fornecedor(cnpj):
        try:
            fornecedor = fornecedor_service.get_fornecedor_by_cnpj(cnpj)
            return jsonify(fornecedor), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fornecedor_bp.route('/', methods=['POST'])
    def create_fornecedor():
        data = request.get_json()
        required_fields = ['cnpj']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: cnpj"}), 400

        try:
            result = fornecedor_service.create_fornecedor(
                cnpj=data['cnpj'],
                nome_empresa=data.get('nome_empresa')
            )
            return jsonify(result), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fornecedor_bp.route('/<path:cnpj>', methods=['PUT'])
    def update_fornecedor(cnpj):
        data = request.get_json()
        nome_empresa = data.get('nome_empresa')

        if not nome_empresa:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            result = fornecedor_service.update_fornecedor(
                cnpj=cnpj,
                nome_empresa=nome_empresa
            )
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrado" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @fornecedor_bp.route('/<path:cnpj>', methods=['DELETE'])
    def delete_fornecedor(cnpj):
        try:
            result = fornecedor_service.delete_fornecedor(cnpj)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return fornecedor_bp