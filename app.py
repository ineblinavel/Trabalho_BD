from flask import Flask
from database.Database import Database

# IMPORTS DOS REPOSITÓRIOS BASE
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository
from repositores.EnfermeiroRepository import EnfermeiroRepository
from repositores.ConsultasRepository import ConsultasRepository
from repositores.MedicamentoRepository import MedicamentoRepository
from repositores.ExameRepository import ExameRepository

# IMPORTS DOS REPOSITÓRIOS ESPECÍFICOS
from repositores.PrescricaoRepository import PrescricaoRepository
from repositores.ProcedimentoRepository import ProcedimentoRepository
from repositores.QuartoRepository import QuartoRepository
from repositores.TipoExameRepository import TipoExameRepository
from repositores.ResultadoExameRepository import ResultadoExameRepository
from repositores.RelatoriosRepository import RelatoriosRepository
from repositores.TelefoneMedicoRepository import TelefoneMedicoRepository
from repositores.TelefoneEnfermeiroRepository import TelefoneEnfermeiroRepository
from repositores.TelefonePacienteRepository import TelefonePacienteRepository

# IMPORTS DOS SERVIÇOS
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

# IMPORTS DAS ROTAS
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

# Conexão com Banco de Dados
db_connection = Database()

# IMPORTS DE REPOSITORIOS BASE PARA VALIDAÇÕES
medico_repo = MedicoRepository(db_connection)
paciente_repo = PacienteRepository(db_connection)
enfermeiro_repo = EnfermeiroRepository(db_connection)
consultas_repo = ConsultasRepository(db_connection)
medicamento_repo = MedicamentoRepository(db_connection)
exame_repo = ExameRepository(db_connection)


# REGISTRO DOS SERVIÇOS E ROTAS

# Médicos
medico_service = MedicoService(medico_repo)
app.register_blueprint(init_medico_routes(medico_service), url_prefix='/')

# Prescrições
# Depende de: PrescricaoRepo, ConsultaRepo, MedicamentoRepo
prescricao_repo = PrescricaoRepository(db_connection)
prescricao_service = PrescricaoService(prescricao_repo, consultas_repo, medicamento_repo)
app.register_blueprint(init_prescricao_routes(prescricao_service), url_prefix='/')

# Procedimentos
# Depende de: ProcedimentoRepo, MedicoRepo, PacienteRepo
procedimento_repo = ProcedimentoRepository(db_connection)
procedimento_service = ProcedimentoService(procedimento_repo, medico_repo, paciente_repo)
app.register_blueprint(init_procedimento_routes(procedimento_service), url_prefix='/')

# Quartos
quarto_repo = QuartoRepository(db_connection)
quarto_service = QuartoService(quarto_repo)
app.register_blueprint(init_quarto_routes(quarto_service), url_prefix='/')

# Tipos de Exame
tipo_exame_repo = TipoExameRepository(db_connection)
tipo_exame_service = TipoExameService(tipo_exame_repo)
app.register_blueprint(init_tipo_exame_routes(tipo_exame_service), url_prefix='/')

# Resultados de Exame
# Depende de: ResultadoExameRepo, ExameRepo
resultado_exame_repo = ResultadoExameRepository(db_connection)
resultado_exame_service = ResultadoExameService(resultado_exame_repo, exame_repo)
app.register_blueprint(init_resultado_exame_routes(resultado_exame_service), url_prefix='/')

# Relatórios
relatorios_repo = RelatoriosRepository(db_connection)
relatorios_service = RelatoriosService(relatorios_repo)
app.register_blueprint(init_relatorios_routes(relatorios_service), url_prefix='/')

# Telefones
# Depende de: TelefoneMedicoRepo, MedicoRepo
tel_medico_repo = TelefoneMedicoRepository(db_connection)
tel_medico_service = TelefoneMedicoService(tel_medico_repo, medico_repo)
app.register_blueprint(init_telefone_medico_routes(tel_medico_service), url_prefix='/')

# Telefones (Enfermeiro)
# Depende de: TelefoneEnfermeiroRepo, EnfermeiroRepo
tel_enfermeiro_repo = TelefoneEnfermeiroRepository(db_connection)
tel_enfermeiro_service = TelefoneEnfermeiroService(tel_enfermeiro_repo, enfermeiro_repo)
app.register_blueprint(init_telefone_enfermeiro_routes(tel_enfermeiro_service), url_prefix='/')

# Telefones (Paciente)
# Depende de: TelefonePacienteRepo, PacienteRepo
tel_paciente_repo = TelefonePacienteRepository(db_connection)
tel_paciente_service = TelefonePacienteService(tel_paciente_repo, paciente_repo)
app.register_blueprint(init_telefone_paciente_routes(tel_paciente_service), url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)