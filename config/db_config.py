import os

# As variáveis de ambiente serão injetadas pelo Docker Compose.
# Elas correspondem aos valores definidos no docker-compose.yml.
ConectorConfig = {
    'host': os.getenv('MYSQL_HOST', 'db'),  # 'db' é o nome do serviço no docker-compose
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DATABASE', 'GerenciamentoHospital')
}
