from flask import Blueprint, request, jsonify
from services.estoquemedicamento_service import EstoqueMedicamentoService

def init_estoquemedicamento_routes(estoque_service: EstoqueMedicamentoService):
    estoque_bp = Blueprint('estoque_bp', __name__, url_prefix='/estoque')

    @estoque_bp.route('/', methods=['GET'])
    def get_all_estoque():
        try:
            estoque = estoque_service.get_all_estoque()
            # Converte objetos date para string para JSON
            for item in estoque:
                item['data_validade'] = item['data_validade'].strftime('%Y-%m-%d')
            return jsonify(estoque), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/<int:id_estoque>', methods=['GET'])
    def get_estoque(id_estoque):
        try:
            item = estoque_service.get_estoque_by_id(id_estoque)
            item['data_validade'] = item['data_validade'].strftime('%Y-%m-%d')
            return jsonify(item), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/vencidos', methods=['GET'])
    def get_expired_stock():
        try:
            items = estoque_service.get_expired_stock()
            for item in items:
                item['data_validade'] = item['data_validade'].strftime('%Y-%m-%d')
            return jsonify(items), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/', methods=['POST'])
    def create_estoque():
        data = request.get_json()
        required_fields = ['data_validade', 'preco_unitario', 'quantidade', 'id_medicamento', 'cnpj_fornecedor']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            preco_unitario = float(data['preco_unitario'])
            quantidade = int(data['quantidade'])
            id_medicamento = int(data['id_medicamento'])

            result = estoque_service.create_estoque(
                data_validade=data['data_validade'],
                preco_unitario=preco_unitario,
                quantidade=quantidade,
                id_medicamento=id_medicamento,
                cnpj_fornecedor=data['cnpj_fornecedor']
            )
            return jsonify(result), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/<int:id_estoque>', methods=['PUT'])
    def update_estoque(id_estoque):
        data = request.get_json()
        update_data = {}
        for key, value in data.items():
            if key in ['data_validade', 'preco_unitario', 'quantidade', 'id_medicamento', 'cnpj_fornecedor']:
                update_data[key] = value

        if not update_data:
            return jsonify({"error": "No data provided for update"}), 400

        try:
            # Converte tipos se necessário antes de passar para o service
            if 'preco_unitario' in update_data: update_data['preco_unitario'] = float(update_data['preco_unitario'])
            if 'quantidade' in update_data: update_data['quantidade'] = int(update_data['quantidade'])
            if 'id_medicamento' in update_data: update_data['id_medicamento'] = int(update_data['id_medicamento'])

            result = estoque_service.update_estoque(id_estoque, **update_data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404 if "não encontrado" in str(e) else 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/<int:id_estoque>', methods=['DELETE'])
    def delete_estoque(id_estoque):
        try:
            result = estoque_service.delete_estoque(id_estoque)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @estoque_bp.route('/<int:id_estoque>/consumir', methods=['POST'])
    def consumir_estoque(id_estoque):
        data = request.get_json()
        quantidade = data.get('quantidade')

        if not quantidade:
            return jsonify({"error": "Quantidade não informada"}), 400

        try:
            result = estoque_service.consumir_estoque(id_estoque, int(quantidade))
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return estoque_bp