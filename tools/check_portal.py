#!/usr/bin/env python3
"""
Valida o portal da disciplina, aulas-1sem/index.html.

Cinco checagens, na ordem em que o aluno realmente encontra o portal:

1. Turma salva em localStorage como 'quarta': o modal de escolha nao aparece
   e os cards mostram as datas de quarta, com a Aula 01 em 05/08/2026.
2. Turma salva como 'quinta': mesma logica, com a Aula 01 em 06/08/2026.
3. localStorage com valor invalido e o relogio do navegador fixado numa
   sexta-feira (nem quarta, nem quinta): o modal aparece, porque
   resolverTurma() nao tem como decidir sozinho.
4. Existem exatamente 20 cards, um por aula.
5. Todo href de botao habilitado ("Slides" ou "Lab") responde HTTP 200 numa
   requisicao real. Botao desabilitado (classe "disabled") e ignorado,
   porque a aula ainda nao foi produzida. O servidor deste validador nao
   faz listagem de diretorio, de proposito: e assim que o GitHub Pages se
   comporta, e listagem de diretorio mascarava link quebrado (diretorio sem
   index.html "funcionava" aqui e dava 404 la).

Sai com codigo 1 e imprime o que falhou se qualquer checagem nao passar.

Uso:
    python3 tools/check_portal.py

Requer: pip install playwright && python3 -m playwright install chromium
"""
import http.server
import os
import socket
import socketserver
import sys
import threading
import urllib.parse

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTAL_URL_REL = "aulas-1sem/index.html"
CHAVE_TURMA = "uninove-turma"

# Sexta-feira: nao e quarta nem quinta, entao resolverTurma() so decide se
# tiver uma turma valida salva. Usada para forcar o modal na checagem 3.
DATA_QUE_NAO_E_QUARTA_NEM_QUINTA = (2026, 8, 7)


def porta_livre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class SemListagemHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler comum serve a listagem de arquivos quando o
    caminho e um diretorio sem index.html dentro. O GitHub Pages nao faz
    isso: devolve 404. Sem essa diferenca, um botao "Lab" apontando para um
    diretorio que so tem README.md pareceria funcionar aqui e quebraria em
    producao (foi exatamente o defeito que a checagem 5 antiga, baseada em
    existencia em disco, deixou passar)."""

    def list_directory(self, path):
        self.send_error(404, "File not found")
        return None


def servir(porta):
    handler = lambda *a, **k: SemListagemHandler(  # noqa: E731
        *a, directory=RAIZ, **k
    )
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", porta), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def js_relogio_fixo(ano, mes, dia):
    """Sobrescreve o Date global do navegador para sempre devolver a mesma
    data local, preservando o comportamento normal quando o construtor
    recebe argumentos. Precisa rodar antes de qualquer script da pagina,
    por isso e injetado via add_init_script."""
    return """
    (() => {
      const RealDate = Date;
      class DataFixa extends RealDate {
        constructor(...args) {
          if (args.length === 0) {
            super(%d, %d, %d);
          } else {
            super(...args);
          }
        }
        static now() {
          return new RealDate(%d, %d, %d).getTime();
        }
      }
      window.Date = DataFixa;
    })();
    """ % (ano, mes - 1, dia, ano, mes - 1, dia)


def js_localstorage_turma(valor):
    if valor is None:
        return "window.localStorage.removeItem(%r);" % CHAVE_TURMA
    return "window.localStorage.setItem(%r, %r);" % (CHAVE_TURMA, valor)


def abrir_pagina(navegador, porta, turma_salva=None, data_fixa=None):
    """Cria um contexto isolado (localStorage proprio) e navega ate o
    portal, com as sobreposicoes indicadas ja aplicadas antes do primeiro
    script da pagina rodar."""
    contexto = navegador.new_context()
    contexto.add_init_script(js_localstorage_turma(turma_salva))
    if data_fixa:
        contexto.add_init_script(js_relogio_fixo(*data_fixa))
    page = contexto.new_page()
    page.goto("http://127.0.0.1:%d/%s" % (porta, PORTAL_URL_REL), wait_until="networkidle")
    page.wait_for_timeout(300)
    return contexto, page


def texto_data_da_aula(page, numero):
    card = page.query_selector('.card[data-aula="%d"] .card-data' % numero)
    return card.inner_text().strip() if card else None


def modal_esta_visivel(page):
    return page.is_visible("#modal-turma")


def checar_turma_sem_modal(navegador, porta, turma, data_esperada_aula01, erros):
    contexto, page = abrir_pagina(navegador, porta, turma_salva=turma)
    try:
        if modal_esta_visivel(page):
            erros.append(
                "checagem 1/2: com localStorage=%r o modal aparece, e nao deveria" % turma
            )
            return
        data_aula01 = texto_data_da_aula(page, 1)
        if data_aula01 != data_esperada_aula01:
            erros.append(
                "checagem 1/2: com localStorage=%r a Aula 01 mostra %r, esperado %r"
                % (turma, data_aula01, data_esperada_aula01)
            )
    finally:
        contexto.close()


def checar_modal_aparece_quando_nao_da_para_decidir(navegador, porta, erros):
    contexto, page = abrir_pagina(
        navegador,
        porta,
        turma_salva="valor-invalido",
        data_fixa=DATA_QUE_NAO_E_QUARTA_NEM_QUINTA,
    )
    try:
        if not modal_esta_visivel(page):
            erros.append(
                "checagem 3: com localStorage invalido e relogio numa sexta-feira, "
                "o modal deveria aparecer e nao apareceu"
            )
    finally:
        contexto.close()


def checar_total_de_cards(navegador, porta, erros):
    contexto, page = abrir_pagina(navegador, porta, turma_salva="quarta")
    try:
        total = page.eval_on_selector_all("[data-aula]", "els => els.length")
        if total != 20:
            erros.append("checagem 4: existem %d cards com data-aula, esperado 20" % total)

        container = page.query_selector("[data-total-cards]")
        if container is None:
            erros.append("checagem 4: nenhum elemento com o atributo data-total-cards")
        else:
            declarado = container.get_attribute("data-total-cards")
            if declarado != "20":
                erros.append(
                    "checagem 4: data-total-cards vale %r, esperado '20'" % declarado
                )
    finally:
        contexto.close()


def checar_links_dos_botoes_habilitados(navegador, porta, erros):
    contexto, page = abrir_pagina(navegador, porta, turma_salva="quarta")
    try:
        botoes = page.eval_on_selector_all(
            "a.btn:not(.disabled)",
            "els => els.map(el => ({ href: el.getAttribute('href'), texto: el.textContent.trim() }))",
        )
        if not botoes:
            erros.append("checagem 5: nenhum botao habilitado encontrado no portal")

        for botao in botoes:
            href = botao["href"]
            if not href:
                erros.append(
                    "checagem 5: botao habilitado '%s' nao tem href" % botao["texto"]
                )
                continue
            url = urllib.parse.urljoin(page.url, href)
            resposta = contexto.request.get(url)
            if resposta.status != 200:
                erros.append(
                    "checagem 5: GET %s (botao '%s') devolveu %d, esperado 200"
                    % (url, botao["texto"], resposta.status)
                )
    finally:
        contexto.close()


def main():
    porta = porta_livre()
    httpd = servir(porta)
    erros = []

    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            try:
                checar_turma_sem_modal(navegador, porta, "quarta", "05/08/2026", erros)
                checar_turma_sem_modal(navegador, porta, "quinta", "06/08/2026", erros)
                checar_modal_aparece_quando_nao_da_para_decidir(navegador, porta, erros)
                checar_total_de_cards(navegador, porta, erros)
                checar_links_dos_botoes_habilitados(navegador, porta, erros)
            finally:
                navegador.close()
    finally:
        httpd.shutdown()

    print("=" * 62)
    if erros:
        print("%d checagem(ns) falhou(aram):\n" % len(erros))
        for erro in erros:
            print("  - %s" % erro)
        return 1

    print("Todas as checagens do portal passaram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
