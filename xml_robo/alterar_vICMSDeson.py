import os
import re
import logging
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES — ajuste aqui conforme necessário
# ============================================================

# Pasta onde estão os arquivos XML
PASTA_XML = os.path.dirname(os.path.abspath(__file__))

# Novo valor que será colocado em todos os campos <vICMSDeson>
NOVO_VALOR = "00.00"

# ============================================================
# CONFIGURAÇÃO DO LOG
# ============================================================

# Arquivo de log salvo na mesma pasta dos XMLs
LOG_FILE = os.path.join(PASTA_XML, f"log_alteracao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # também exibe no terminal
    ]
)

# ============================================================
# FUNÇÃO: Altera todos os campos <vICMSDeson> de um XML
# ============================================================

def alterar_vicmsdeson(caminho_arquivo: str, novo_valor: str) -> bool:
    """
    Lê o arquivo XML, substitui todos os valores de <vICMSDeson>
    pelo novo_valor e sobrescreve o arquivo original.

    Retorna True se alterou com sucesso, False se houve erro.
    """
    try:
        # Lê o conteúdo original do arquivo
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Regex que captura qualquer valor dentro de <vICMSDeson>...</vICMSDeson>
        padrao = r"<vICMSDeson>[^<]*</vICMSDeson>"
        substituto = f"<vICMSDeson>{novo_valor}</vICMSDeson>"

        # Conta quantas ocorrências foram encontradas antes de substituir
        ocorrencias = len(re.findall(padrao, conteudo))

        if ocorrencias == 0:
            logging.warning(f"  [AVISO] Nenhum campo <vICMSDeson> encontrado em: {os.path.basename(caminho_arquivo)}")
            return False

        # Realiza a substituição de todas as ocorrências
        conteudo_novo = re.sub(padrao, substituto, conteudo)

        # Sobrescreve o arquivo original com o conteúdo alterado
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo_novo)

        logging.info(f"  [OK] {os.path.basename(caminho_arquivo)} — {ocorrencias} campo(s) alterado(s)")
        return True

    except Exception as e:
        logging.error(f"  [ERRO] {os.path.basename(caminho_arquivo)} — {e}")
        return False


# ============================================================
# FUNÇÃO PRINCIPAL: percorre a pasta e processa cada XML
# ============================================================

def processar_pasta(pasta: str, novo_valor: str):
    """
    Varre a pasta procurando arquivos .xml e chama
    alterar_vicmsdeson() para cada um.
    """

    # Verifica se a pasta existe antes de começar
    if not os.path.isdir(pasta):
        logging.error(f"Pasta não encontrada: {pasta}")
        return

    # Lista apenas arquivos com extensão .xml (case-insensitive)
    arquivos_xml = [
        f for f in os.listdir(pasta)
        if f.lower().endswith(".xml")
    ]

    total = len(arquivos_xml)

    if total == 0:
        logging.warning("Nenhum arquivo .xml encontrado na pasta.")
        return

    logging.info(f"{'='*50}")
    logging.info(f"Início do processamento — {total} arquivo(s) encontrado(s)")
    logging.info(f"Pasta: {pasta}")
    logging.info(f"Novo valor para <vICMSDeson>: {novo_valor}")
    logging.info(f"{'='*50}")

    # Contadores para o resumo final
    sucesso = 0
    falha = 0

    # Itera sobre cada arquivo XML encontrado
    for nome_arquivo in sorted(arquivos_xml):
        caminho_completo = os.path.join(pasta, nome_arquivo)

        resultado = alterar_vicmsdeson(caminho_completo, novo_valor)

        if resultado:
            sucesso += 1
        else:
            falha += 1

    # Exibe resumo ao final
    logging.info(f"{'='*50}")
    logging.info(f"Processamento concluído!")
    logging.info(f"  Sucesso : {sucesso} arquivo(s)")
    logging.info(f"  Falha   : {falha} arquivo(s)")
    logging.info(f"  Log salvo em: {LOG_FILE}")
    logging.info(f"{'='*50}")


# ============================================================
# ENTRADA DO SCRIPT
# ============================================================

if __name__ == "__main__":
    processar_pasta(PASTA_XML, NOVO_VALOR)
