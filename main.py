from repositores.MedicoRepository import MedicoRepository

medico_repo = MedicoRepository()

def main():
    print("\n--- LISTA DE MÉDICOS CADASTRADOS ---")
    medicos = medico_repo.find_all()
    for medico in medicos:
        print(f"CRM: {medico['crm']}, Nome: {medico['nome_medico']}, CPF: {medico['cpf']}, Salário: {medico['salario']}")




if __name__ == "__main__":
    main()