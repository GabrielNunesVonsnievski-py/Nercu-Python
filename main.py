import json
import os

ARQUIVO = "listChamados.json"


def carregar_chamados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return []
            return json.loads(conteudo)
    return []

def salvar_chamados(chamados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(chamados, f, ensure_ascii=False, indent=4)

def proximo_id(chamados):
    if not chamados:
        return 1
    return max(c["id"] for c in chamados) + 1

def abrir_chamado(chamados):
    print("\n--- Abrir Chamado ---")
    titulo = input("Título: ").strip()
    if not titulo:
        print("Título não pode ser vazio.")
        return

    print("Categorias: 1-Hardware  2-Software  3-Rede  4-Outro")
    categorias = {"1": "Hardware", "2": "Software", "3": "Rede", "4": "Outro"}
    cat = input("Categoria: ")
    categoria = categorias.get(cat, "Outro")

    print("Prioridade: 1-Baixa  2-Média  3-Alta")
    prioridades = {"1": "Baixa", "2": "Média", "3": "Alta"}
    pri = input("Prioridade: ")
    prioridade = prioridades.get(pri, "Baixa")

    responsavel = input("Responsável: ").strip()

    chamado = {
        "id": proximo_id(chamados),
        "titulo": titulo,
        "categoria": categoria,
        "prioridade": prioridade,
        "status": "Aberto",
        "responsavel": responsavel
    }

    chamados.append(chamado)
    salvar_chamados(chamados)
    print(f"Chamado #{chamado['id']} aberto com sucesso!")

def listar_chamados(chamados):
    print("\n--- Listar Chamados ---")
    print("Filtrar por status: 1-Todos  2-Abertos  3-Em andamento  4-Encerrados")
    filtro = input("Filtro: ")

    filtros = {"1": None, "2": "Aberto", "3": "Em andamento", "4": "Encerrado"}
    status_filtro = filtros.get(filtro, None)

    if not status_filtro:
        lista = chamados
    else:
        lista = [c for c in chamados if c["status"] == status_filtro]

    if not lista:
        print("Nenhum chamado encontrado.")
        return

    print(f"\n{'ID':<5} {'Título':<25} {'Categoria':<12} {'Prioridade':<10} {'Status':<14} {'Responsável'}")
    print("-" * 80)
    for c in lista:
        print(f"{c['id']:<5} {c['titulo']:<25} {c['categoria']:<12} {c['prioridade']:<10} {c['status']:<14} {c['responsavel']}")
    print("-" * 80)    

def atualizar_status(chamados):
    print("\n--- Atualizar Status ---")
    listar_chamados(chamados)

    try:
        id_chamado = int(input("\nID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return

    chamado = next((c for c in chamados if c["id"] == id_chamado), None)
    if not chamado:
        print("Chamado não encontrado.")
        return

    print("Novo status: 1-Aberto  2-Em andamento  3-Encerrado")
    opcoes = {"1": "Aberto", "2": "Em andamento", "3": "Encerrado"}
    op = input("Status: ")
    novo_status = opcoes.get(op)

    if not novo_status:
        print("Opção inválida.")
        return

    chamado["status"] = novo_status
    salvar_chamados(chamados)
    print(f"Chamado #{id_chamado} atualizado para '{novo_status}'.")

def encerrar_chamado(chamados):
    print("\n--- Encerrar Chamado ---")
    listar_chamados(chamados)

    try:
        id_chamado = int(input("\nID do chamado a encerrar: "))
    except ValueError:
        print("ID inválido.")
        return

    chamado = next((c for c in chamados if c["id"] == id_chamado), None)
    if not chamado:
        print("Chamado não encontrado.")
        return

    if chamado["status"] == "Encerrado":
        print("Chamado já está encerrado.")
        return

    chamado["status"] = "Encerrado"
    salvar_chamados(chamados)
    print(f"Chamado #{id_chamado} encerrado com sucesso!")

def main():
    chamados = carregar_chamados()

    while True:
        print("\n=== NERCU PYTHON ===")
        print("1. Abrir Chamado")
        print("2. Listar Chamados")
        print("3. Atualizar Status")
        print("4. Encerrar Chamado")
        print("0. Sair")

        try:
            opcao = int(input("Digite o número da sua escolha: "))
        except ValueError:
            print("Digite apenas números!")
            continue

        if opcao == 1:
            abrir_chamado(chamados)
        elif opcao == 2:
            listar_chamados(chamados)
        elif opcao == 3:
            atualizar_status(chamados)
        elif opcao == 4:
            encerrar_chamado(chamados)
        elif opcao == 0:
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


main()