from datetime import datetime
from math import isfinite
import requests

def verificar_cnpj(cnpj):
    resposta = requests.get(
        f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'
    )

    if resposta.status_code == 200:
        return resposta.json().get('descricao_situacao_cadastral') == 'ATIVA'

    return False

def validar_produto(nome, descricao, preco_texto, foto):

    if nome == "":
        return "Informe o nome do produto."

    if len(nome) > 80:
        return "O nome deve ter no máximo 80 caracteres."

    if len(descricao) > 200:
        return "A descrição deve ter no máximo 200 caracteres."

    if len(foto) > 255:
        return "A foto deve ter no máximo 255 caracteres."

    try:
        preco = float(preco_texto.replace(",", "."))
    except ValueError:
        return "Preço inválido."

    if not isfinite(preco) or preco <= 0:
        return "O preço deve ser maior que zero."

    return None


def hora_valida(texto):

    try:
        datetime.strptime(texto, "%H:%M")
        return True
    except (ValueError, TypeError):
        return False


def validar_localizacao(
    latitude_texto,
    longitude_texto,
    endereco,
    hora_abertura,
    hora_fechamento
):

    try:
        latitude = float(latitude_texto.replace(",", "."))
        longitude = float(longitude_texto.replace(",", "."))
    except ValueError:
        return "Latitude e longitude devem ser números."

    if not isfinite(latitude) or not -90 <= latitude <= 90:
        return "Latitude inválida."

    if not isfinite(longitude) or not -180 <= longitude <= 180:
        return "Longitude inválida."

    if endereco == "":
        return "Informe o endereço."

    if len(endereco) > 200:
        return "O endereço deve ter no máximo 200 caracteres."

    if not hora_valida(hora_abertura):
        return "Horário de abertura inválido. Use HH:MM."

    if not hora_valida(hora_fechamento):
        return "Horário de fechamento inválido. Use HH:MM."

    abertura = datetime.strptime(hora_abertura, "%H:%M").time()
    fechamento = datetime.strptime(hora_fechamento, "%H:%M").time()

    if abertura >= fechamento:
        return "A abertura deve ser anterior ao fechamento."

    return None
