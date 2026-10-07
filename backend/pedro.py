from flask import Flask

app = Flask(__name__)


# ==========================================
# DADOS TEMPORÁRIOS
# ==========================================

feirantes = []
perfis = []


# ==========================================
# FEIRANTES
# ==========================================

def proximo_id(lista):

    if len(lista) == 0:
        return 1

    maior = 0

    for item in lista:

        if item["id"] > maior:
            maior = item["id"]

    return maior + 1


def cadastrar_feirante(cnpj, nome, email, senha):

    for feirante in feirantes:

        if feirante["email"].lower() == email.lower():
            return None

    feirante = {
        "id": proximo_id(feirantes),
        "cnpj": cnpj,
        "nome": nome,
        "email": email,
        "senha": senha,
        "status": "ativo"
    }

    feirantes.append(feirante)

    return feirante


def listar_feirantes():

    return feirantes


def buscar_feirante(id):

    for feirante in feirantes:

        if feirante["id"] == id:
            return feirante

    return None


def alterar_feirante(
    id,
    cnpj,
    nome,
    email,
    senha,
    status
):

    for feirante in feirantes:

        if feirante["id"] == id:

            for outro in feirantes:

                if outro["id"] != id:

                    if outro["email"].lower() == email.lower():
                        return None

            feirante["cnpj"] = cnpj
            feirante["nome"] = nome
            feirante["email"] = email
            feirante["senha"] = senha
            feirante["status"] = status

            return feirante

    return None


def excluir_feirante(id):

    for feirante in feirantes:

        if feirante["id"] == id:

            feirantes.remove(feirante)

            i = 0

            while i < len(perfis):

                if perfis[i]["feirante_id"] == id:
                    perfis.pop(i)
                else:
                    i += 1

            return True

    return False


# ==========================================
# PERFIL_FEIRANTE
# ==========================================

def cadastrar_perfil(
    feirante_id,
    nome_barraca,
    descricao,
    categoria
):

    if buscar_feirante(feirante_id) is None:
        return None

    for perfil in perfis:

        if perfil["feirante_id"] == feirante_id:
            return None

    perfil = {
        "id": proximo_id(perfis),
        "feirante_id": feirante_id,
        "nome_barraca": nome_barraca,
        "descricao": descricao,
        "categoria": categoria
    }

    perfis.append(perfil)

    return perfil


def listar_perfis():

    return perfis


def buscar_perfil(id):

    for perfil in perfis:

        if perfil["id"] == id:
            return perfil

    return None


def buscar_perfil_feirante(feirante_id):

    for perfil in perfis:

        if perfil["feirante_id"] == feirante_id:
            return perfil

    return None


def alterar_perfil(
    id,
    nome_barraca,
    descricao,
    categoria
):

    for perfil in perfis:

        if perfil["id"] == id:

            perfil["nome_barraca"] = nome_barraca
            perfil["descricao"] = descricao
            perfil["categoria"] = categoria

            return perfil

    return None


def excluir_perfil(id):

    for perfil in perfis:

        if perfil["id"] == id:

            perfis.remove(perfil)

            return True

    return False


# ==========================================
# TESTE
# ==========================================

feirante1 = cadastrar_feirante(
    "11111111111111",
    "Bruno",
    "bruno@email.com",
    "123456"
)

feirante2 = cadastrar_feirante(
    "22222222222222",
    "Manel",
    "manel@email.com",
    "654321"
)

feirante3 = cadastrar_feirante(
    "33333333333333",
    "Luiz",
    "luiz@email.com",
    "789456"
)


perfil1 = cadastrar_perfil(
    feirante1["id"],
    "Barraca do Bruno",
    "Produtos variados",
    "Alimentação"
)

perfil2 = cadastrar_perfil(
    feirante2["id"],
    "Barraca do Manel",
    "Produtos artesanais",
    "Artesanato"
)

perfil3 = cadastrar_perfil(
    feirante3["id"],
    "Barraca do Luiz",
    "Frutas e verduras",
    "Agricultura"
)


print("FEIRANTES:")
print(listar_feirantes())


print("\nPERFIS:")
print(listar_perfis())


print("\nBUSCAR FEIRANTE:")
print(buscar_feirante(1))


print("\nBUSCAR PERFIL:")
print(buscar_perfil_feirante(1))


print("\nALTERAR FEIRANTE:")
print(
    alterar_feirante(
        1,
        "11111111111111",
        "Bruno Atualizado",
        "bruno_novo@email.com",
        "987654",
        "ativo"
    )
)


print("\nALTERAR PERFIL:")
print(
    alterar_perfil(
        1,
        "Barraca do Bruno",
        "Produtos alimentícios e doces",
        "Alimentação"
    )
)


print("\nEXCLUIR PERFIL:")
print(excluir_perfil(2))


print("\nEXCLUIR FEIRANTE:")
print(excluir_feirante(3))


print("\nFEIRANTES FINAIS:")
print(listar_feirantes())


print("\nPERFIS FINAIS:")
print(listar_perfis())


if __name__ == "__main__":
    app.run(debug=True)