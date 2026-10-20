import requests

def verificar_cnpj(cnpj):
    resposta = requests.get(
        f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}',
        timeout=10
    )

    if resposta.status_code == 200:
        return resposta.json().get('descricao_situacao_cadastral') == 'ATIVA'

    return False