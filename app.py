from flask import Flask, render_template, session, redirect, url_for
from database.Database import Database
from datetime import timedelta
# IMPORTS DOS REPOSITÓRIOS BASE
from repositores.MedicoRepository import MedicoRepository
from repositores.PacienteRepository import PacienteRepository
from repositores.EnfermeiroRepository import EnfermeiroRepository
from repositores.ConsultasRepository import ConsultasRepository
from repositores.MedicamentoRepository import MedicamentoRepository
from repositores.ExameRepository import ExameRepository

# IMPORTS DOS REPOSITÓRIOS ESPECÍFICOS
from repositores.AgendaMedicoRepository import AgendaMedicoRepository
from repositores.EstoqueMedicamentoRepository import EstoqueMedicamentoRepository
from repositores.FornecedorRepository import FornecedorRepository
from repositores.InternacaoRepository import InternacaoRepository
from repositores.QuartoRepository import QuartoRepository
from repositores.TipoExameRepository import TipoExameRepository
from repositores.ResultadoExameRepository import ResultadoExameRepository
from repositores.PrescricaoRepository import PrescricaoRepository
from repositores.ProcedimentoRepository import ProcedimentoRepository
from repositores.RelatoriosRepository import RelatoriosRepository
from repositores.TelefoneMedicoRepository import TelefoneMedicoRepository
from repositores.TelefoneEnfermeiroRepository import TelefoneEnfermeiroRepository
from repositores.TelefonePacienteRepository import TelefonePacienteRepository
from repositores.UsuarioRepository import UsuarioRepository
from repositores.LogSalarioRepository import LogSalarioRepository

# IMPORTS DOS SERVIÇOS
from services.medico_service import MedicoService
from services.paciente_service import PacienteService
from services.enfermeiro_service import EnfermeiroService
from services.consultas_service import ConsultasService
from services.medicamento_service import MedicamentoService
from services.exame_service import ExameService
from services.agendamedico_service import AgendaMedicoService
from services.fornecedor_service import FornecedorService
from services.estoquemedicamento_service import EstoqueMedicamentoService
from services.internacao_service import InternacaoService
from services.prescricao_service import PrescricaoService
from services.procedimento_service import ProcedimentoService
from services.quarto_service import QuartoService
from services.tipo_exame_service import TipoExameService
from services.resultado_exame_service import ResultadoExameService
from services.relatorios_service import RelatoriosService
from services.telefone_medico_service import TelefoneMedicoService
from services.telefone_enfermeiro_service import TelefoneEnfermeiroService
from services.telefone_paciente_service import TelefonePacienteService
from services.auth_service import AuthService
from services.log_salario_service import LogSalarioService

# IMPORTS DAS ROTAS
from routes.medico_routes import init_medico_routes
from routes.paciente_routes import init_paciente_routes
from routes.enfermeiro_routes import init_enfermeiro_routes
from routes.consultas_routes import init_consultas_routes
from routes.medicamento_routes import init_medicamento_routes
from routes.exame_routes import init_exame_routes
from routes.agendamedico_routes import init_agendamedico_routes
from routes.fornecedor_routes import init_fornecedor_routes
from routes.estoquemedicamento_routes import init_estoquemedicamento_routes
from routes.internacao_routes import init_internacao_routes
from routes.prescricao_routes import init_prescricao_routes
from routes.procedimento_routes import init_procedimento_routes
from routes.quarto_routes import init_quarto_routes
from routes.tipo_exame_routes import init_tipo_exame_routes
from routes.resultado_exame_routes import init_resultado_exame_routes
from routes.relatorios_routes import init_relatorios_routes
from routes.telefone_medico_routes import init_telefone_medico_routes
from routes.telefone_enfermeiro_routes import init_telefone_enfermeiro_routes
from routes.telefone_paciente_routes import init_telefone_paciente_routes
from routes.auth_routes import init_auth_routes
from routes.log_salario_routes import init_log_salario_routes


app = Flask(__name__)
app.secret_key = 'segredo_muito_basico'

# Define um nome único para o cookie para evitar conflitos com outros apps em localhost
app.config['SESSION_COOKIE_NAME'] = 'hospitalgest_session'
# Define que a sessão deve durar por um tempo fixo (ex: 2 horas ou 7 dias)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_PERMANENT'] = True

# Conexão com Banco de Dados
db_connection = Database()

# IMPORTS E INICIALIZAÇÃO DE TODOS OS REPOSITÓRIOS
medico_repo = MedicoRepository(db_connection)
paciente_repo = PacienteRepository(db_connection)
enfermeiro_repo = EnfermeiroRepository(db_connection)
consultas_repo = ConsultasRepository(db_connection)
medicamento_repo = MedicamentoRepository(db_connection)
exame_repo = ExameRepository(db_connection)
prescricao_repo = PrescricaoRepository(db_connection)
procedimento_repo = ProcedimentoRepository(db_connection)
quarto_repo = QuartoRepository(db_connection)
tipo_exame_repo = TipoExameRepository(db_connection)
resultado_exame_repo = ResultadoExameRepository(db_connection)
relatorios_repo = RelatoriosRepository(db_connection)
tel_medico_repo = TelefoneMedicoRepository(db_connection)
tel_enfermeiro_repo = TelefoneEnfermeiroRepository(db_connection)
tel_paciente_repo = TelefonePacienteRepository(db_connection)
usuario_repo = UsuarioRepository(db_connection)
agenda_repo = AgendaMedicoRepository(db_connection)
fornecedor_repo = FornecedorRepository(db_connection)
estoque_repo = EstoqueMedicamentoRepository(db_connection)
internacao_repo = InternacaoRepository(db_connection)
log_salario_repo = LogSalarioRepository(db_connection)


# REGISTRO DOS SERVIÇOS E ROTAS

# Auth
auth_service = AuthService(usuario_repo)
app.register_blueprint(init_auth_routes(auth_service))

# Logs Salario
log_salario_service = LogSalarioService(log_salario_repo)
app.register_blueprint(init_log_salario_routes(log_salario_service))

# Médicos
medico_service = MedicoService(medico_repo, usuario_repo)
app.register_blueprint(init_medico_routes(medico_service))

# Pacientes
paciente_service = PacienteService(paciente_repo)
app.register_blueprint(init_paciente_routes(paciente_service))

# Enfermeiros
enfermeiro_service = EnfermeiroService(enfermeiro_repo, usuario_repo)
app.register_blueprint(init_enfermeiro_routes(enfermeiro_service))

# Medicamentos
medicamento_service = MedicamentoService(medicamento_repo)
app.register_blueprint(init_medicamento_routes(medicamento_service))

# Fornecedores
fornecedor_service = FornecedorService(fornecedor_repo)
app.register_blueprint(init_fornecedor_routes(fornecedor_service))

# Estoque de Medicamentos
estoque_service = EstoqueMedicamentoService(estoque_repo, medicamento_repo, fornecedor_repo)
app.register_blueprint(init_estoquemedicamento_routes(estoque_service))

# Agenda Médica
agenda_service = AgendaMedicoService(agenda_repo, medico_repo)
app.register_blueprint(init_agendamedico_routes(agenda_service))

# Consultas
consultas_service = ConsultasService(consultas_repo, medico_repo, paciente_repo, agenda_repo)
app.register_blueprint(init_consultas_routes(consultas_service))

# Exames
exame_service = ExameService(exame_repo, medico_repo, paciente_repo, tipo_exame_repo)
app.register_blueprint(init_exame_routes(exame_service))

# Internações
internacao_service = InternacaoService(internacao_repo, medico_repo, paciente_repo, enfermeiro_repo, quarto_repo)
app.register_blueprint(init_internacao_routes(internacao_service))

# Prescrições
# Depende de: PrescricaoRepo, ConsultaRepo, MedicamentoRepo
prescricao_service = PrescricaoService(prescricao_repo, consultas_repo, medicamento_repo)
app.register_blueprint(init_prescricao_routes(prescricao_service))

# Procedimentos
# Depende de: ProcedimentoRepo, MedicoRepo, PacienteRepo
procedimento_service = ProcedimentoService(procedimento_repo, medico_repo, paciente_repo)
app.register_blueprint(init_procedimento_routes(procedimento_service))

# Quartos
quarto_service = QuartoService(quarto_repo)
app.register_blueprint(init_quarto_routes(quarto_service))

# Tipos de Exame
tipo_exame_service = TipoExameService(tipo_exame_repo)
app.register_blueprint(init_tipo_exame_routes(tipo_exame_service))
# Resultados de Exame
# Depende de: ResultadoExameRepo, ExameRepo
resultado_exame_service = ResultadoExameService(resultado_exame_repo, exame_repo)
app.register_blueprint(init_resultado_exame_routes(resultado_exame_service))

# Relatórios
relatorios_service = RelatoriosService(relatorios_repo)
app.register_blueprint(init_relatorios_routes(relatorios_service))

# Telefones
# Depende de: TelefoneMedicoRepo, MedicoRepo
tel_medico_service = TelefoneMedicoService(tel_medico_repo, medico_repo)
app.register_blueprint(init_telefone_medico_routes(tel_medico_service))

# Telefones (Enfermeiro)
# Depende de: TelefoneEnfermeiroRepo, EnfermeiroRepo
tel_enfermeiro_service = TelefoneEnfermeiroService(tel_enfermeiro_repo, enfermeiro_repo)
app.register_blueprint(init_telefone_enfermeiro_routes(tel_enfermeiro_service))

# Telefones (Paciente)
# Depende de: TelefonePacienteRepo, PacienteRepo
tel_paciente_service = TelefonePacienteService(tel_paciente_repo, paciente_repo)
app.register_blueprint(init_telefone_paciente_routes(tel_paciente_service))


# Rota para o Dashboard
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    role = session.get('role')
    if role == 'admin':
        return redirect('/ui/portal/admin')
    elif role == 'medico':
        return redirect('/ui/portal/medico')
    elif role == 'enfermeiro':
        return redirect('/ui/portal/enfermeiro')

    return render_template('index.html')


@app.route('/ui/portal/admin')
def portal_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('portal_admin.html')

@app.route('/ui/portal/medico')
def portal_medico():
    if 'user_id' not in session or session.get('role') != 'medico':
        return redirect('/login')
    return render_template('portal_medico.html')

@app.route('/ui/portal/enfermeiro')
def portal_enfermeiro():
    if 'user_id' not in session or session.get('role') != 'enfermeiro':
        return redirect('/login')
    return render_template('portal_enfermeiro.html')
# Rotas para as interfaces (UI)
# Use prefixos como /ui/ para diferenciar das rotas de dados se preferir
@app.route('/ui/medicos')
def view_medicos():
    return render_template('medicos.html')

@app.route('/ui/quartos')
def view_quartos():
    return render_template('quartos.html')

@app.route('/ui/pacientes')
def view_pacientes():
    # Crie o templates/pacientes.html similar ao de médicos
    return render_template('pacientes.html')

@app.route('/ui/estoque')
def view_estoque():
    return render_template('estoque.html')

@app.route('/ui/medicos/novo')
def view_add_medico():
    return render_template('add_medico.html')

@app.route('/ui/pacientes/novo')
def view_add_paciente():
    return render_template('add_paciente.html')

@app.route('/ui/estoque/novo')
def view_add_estoque():
    return render_template('add_estoque.html')

@app.route('/ui/internacoes/nova')
def view_nova_internacao():
    return render_template('nova_internacao.html')

@app.route('/ui/consultas/nova')
def view_nova_consulta():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('nova_consulta.html')

@app.route('/ui/pacientes/<int:id_paciente>/historico')
def view_paciente_historico(id_paciente):
    # O ID será pego pelo JavaScript via URL, mas a rota precisa existir
    return render_template('paciente_historico.html', id_paciente=id_paciente)

@app.route('/ui/exames')
def view_exames():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('exames.html')

@app.route('/ui/relatorios')
def view_relatorios():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('relatorios.html')

@app.route('/ui/enfermeiros')
def view_enfermeiros():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('enfermeiros.html')

@app.route('/ui/enfermeiros/novo')
def view_add_enfermeiro():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('add_enfermeiro.html')

@app.route('/ui/admin/fornecedores')
def view_admin_fornecedores():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin/fornecedores.html')

@app.route('/ui/admin/tipos-exame')
def view_admin_tipos_exame():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin/tipos_exame.html')

@app.route('/ui/admin/medicamentos')
def view_admin_medicamentos():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin/medicamentos.html')

@app.route('/ui/admin/logs-salario')
def view_admin_logs_salario():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin/logs_salario.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)