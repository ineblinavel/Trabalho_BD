from flask import Flask
from database.Database import Database
from repositores.MedicoRepository import MedicoRepository
from services.medico_service import MedicoService
from routes.medico_routes import init_medico_routes

app = Flask(__name__)
app.secret_key = 'segredo_muito_basico'

db_connection = Database()
medico_repo = MedicoRepository(db_connection)
medico_service = MedicoService(medico_repo)

# Register Blueprints
medico_blueprint = init_medico_routes(medico_service)
app.register_blueprint(medico_blueprint, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

