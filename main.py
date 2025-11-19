from repositores.MedicoRepository import MedicoRepository

medico_repo = MedicoRepository()

def main():
    print("\n--- LISTA DE MÉDICOS CADASTRADOS ---")
    medicos = medico_repo.find_all()
    for medico in medicos:
        print(f"CRM: {medico['crm']}, Nome: {medico['nome_medico']}, CPF: {medico['cpf']}, Salário: {medico['salario']}")


    medico_bycrm = medico_repo.find_by_crm("123456")
    if medico_bycrm:
        print("\n--- MÉDICO ENCONTRADO POR CRM ---")
        print(f"CRM: {medico_bycrm['crm']}, Nome: {medico_bycrm['nome_medico']}, CPF: {medico_bycrm['cpf']}, Salário: {medico_bycrm['salario']}")
    else:
        print("\nMédico com CRM 123456 não encontrado.")



if __name__ == "__main__":
    main()