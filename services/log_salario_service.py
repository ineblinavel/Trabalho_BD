from repositores.LogSalarioRepository import LogSalarioRepository

class LogSalarioService:
    def __init__(self, log_repo: LogSalarioRepository):
        self.log_repo = log_repo

    def get_all_logs(self, crm=None):
        return self.log_repo.get_all_logs(crm)
