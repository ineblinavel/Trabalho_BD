from flask import Flask
from database.Database import Database

# Importações dos repositórios
from repositores.MedicoRepository import MedicoRepository
from repositores.PrescricaoRepository import PrescricaoRepository
from repositores.ProcedimentoRepository import ProcedimentoRepository
from repositores.QuartoRepository import QuartoRepository
from repositores.TipoExameRepository import TipoExameRepository
from repositores.ResultadoExameRepository import ResultadoExameRepository
from repositores.RelatoriosRepository import RelatoriosRepository
from repositores.TelefoneMedicoRepository import TelefoneMedicoRepository
from repositores.TelefoneEnfermeiroRepository import TelefoneEnfermeiroRepository
from repositores.TelefonePacienteRepository import TelefonePacienteRepository

# Importações dos serviços
from services.medico_service import MedicoService
from services.prescricao_service import PrescricaoService
from services.procedimento_service import ProcedimentoService
from services.quarto_service import QuartoService
from services.tipo_exame_service import TipoExameService
from services.resultado_exame_service import ResultadoExameService
from services.relatorios_service import RelatoriosService
from services.telefone_medico_service import TelefoneMedicoService
from services.telefone_enfermeiro_service import TelefoneEnfermeiroService
from services.telefone_paciente_service import TelefonePacienteService

# Importações das rotas
from routes.medico_routes import init_medico_routes
from routes.prescricao_routes import init_prescricao_routes
from routes.procedimento_routes import init_procedimento_routes
from routes.quarto_routes import init_quarto_routes
from routes.tipo_exame_routes import init_tipo_exame_routes
from routes.resultado_exame_routes import init_resultado_exame_routes
from routes.relatorios_routes import init_relatorios_routes
from routes.telefone_medico_routes import init_telefone_medico_routes
from routes.telefone_enfermeiro_routes import init_telefone_enfermeiro_routes
from routes.telefone_paciente_routes import init_telefone_paciente_routes

app = Flask(__name__)
app.secret_key = 'segredo_muito_basico'

db_connection = Database()

# Médico
medico_repo = MedicoRepository(db_connection)
medico_service = MedicoService(medico_repo)
medico_bp = init_medico_routes(medico_service)
app.register_blueprint(medico_bp, url_prefix='/')

# Prescrição
prescricao_repo = PrescricaoRepository(db_connection)
prescricao_service = PrescricaoService(prescricao_repo)
prescricao_bp = init_prescricao_routes(prescricao_service)
app.register_blueprint(prescricao_bp, url_prefix='/')

# Procedimento
procedimento_repo = ProcedimentoRepository(db_connection)
procedimento_service = ProcedimentoService(procedimento_repo)
procedimento_bp = init_procedimento_routes(procedimento_service)
app.register_blueprint(procedimento_bp, url_prefix='/')

# Quarto
quarto_repo = QuartoRepository(db_connection)
quarto_service = QuartoService(quarto_repo)
quarto_bp = init_quarto_routes(quarto_service)
app.register_blueprint(quarto_bp, url_prefix='/')

# Tipo de Exame
tipo_exame_repo = TipoExameRepository(db_connection)
tipo_exame_service = TipoExameService(tipo_exame_repo)
tipo_exame_bp = init_tipo_exame_routes(tipo_exame_service)
app.register_blueprint(tipo_exame_bp, url_prefix='/')

# Resultado de Exame
resultado_exame_repo = ResultadoExameRepository(db_connection)
resultado_exame_service = ResultadoExameService(resultado_exame_repo)
resultado_exame_bp = init_resultado_exame_routes(resultado_exame_service)
app.register_blueprint(resultado_exame_bp, url_prefix='/')

# Relatórios
relatorios_repo = RelatoriosRepository(db_connection)
relatorios_service = RelatoriosService(relatorios_repo)
relatorios_bp = init_relatorios_routes(relatorios_service)
app.register_blueprint(relatorios_bp, url_prefix='/')

# Telefone Médico
tel_medico_repo = TelefoneMedicoRepository(db_connection)
tel_medico_service = TelefoneMedicoService(tel_medico_repo)
app.register_blueprint(init_telefone_medico_routes(tel_medico_service), url_prefix='/')

# Telefone Enfermeiro
tel_enfermeiro_repo = TelefoneEnfermeiroRepository(db_connection)
tel_enfermeiro_service = TelefoneEnfermeiroService(tel_enfermeiro_repo)
app.register_blueprint(init_telefone_enfermeiro_routes(tel_enfermeiro_service), url_prefix='/')

# Telefone Paciente
tel_paciente_repo = TelefonePacienteRepository(db_connection)
tel_paciente_service = TelefonePacienteService(tel_paciente_repo)
app.register_blueprint(init_telefone_paciente_routes(tel_paciente_service), url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

