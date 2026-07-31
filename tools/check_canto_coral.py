#!/usr/bin/env python3
"""
Verifica, pixel a pixel, se o triangulo coral do canto superior direito de cada
slide chegou inteiro na tela.

POR QUE ESTE SCRIPT EXISTE
--------------------------
`tools/check_slides.py` NAO enxerga este defeito. O `.decor-coral` tem caixa
zerada no proprio <div> (quem desenha o triangulo e o pseudo-elemento ::after),
e o validador descarta do conjunto comparado qualquer elemento de caixa nula.
Um "OK" dele nao prova nada sobre este canto.

Na revisao da Aula 01, a `.uninove-logo-header` (fundo branco opaco do PNG,
z-index 1 contra z-index 0 do triangulo) abria um retangulo palido dentro do
triangulo em 17 dos 21 slides. A checagem geometrica de caixas nao pegou o
defeito porque so elementos de texto tinham sido comparados; e mesmo comparando
todas as caixas, a interseccao de caixa continua existindo depois da correcao
(a logo transparente segue por cima do triangulo, so que agora deixa o coral
passar). Por isso a verificacao correta e por PIXEL, no resultado renderizado, e
nao por retangulo do DOM.

O QUE E VERIFICADO
------------------
Para cada `section` que tem `.decor-coral`, todo pixel do interior do triangulo
precisa ter a cor do coral da marca aplicada com a opacidade do tema
(#C84B31 a 75% sobre o branco do slide). Sao ignorados:

  - a faixa da `.top-bar`, decoracao de borda que o template desenha de
    proposito sobre o topo do slide inteiro;
  - uma folga de 2px na hipotenusa, por causa do antialiasing da borda.

NUMERACAO DOS SLIDES
--------------------
Os slides sao reportados em BASE 0, o mesmo indice usado por `Reveal.slide(i)` e
pelo `tools/check_slides.py`. O primeiro slide do deck e o slide 0. Manter a
mesma base nos dois validadores evita que um relatorio aponte para o slide
errado quando os dois rodam sobre o mesmo deck.

Uso:
    python3 tools/check_canto_coral.py                        # todos os decks
    python3 tools/check_canto_coral.py aulas-1sem/aulas/aula01.html

Requer: pip install playwright pillow && python3 -m playwright install chromium
"""
import glob
import http.server
import os
import socket
import socketserver
import sys
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LARGURA, ALTURA = 1280, 720
LADO = 80          # o triangulo do ::after ocupa um quadrado de 80x80
ALTURA_TOP_BAR = 6  # faixa superior do template, desenhada por cima de proposito
FOLGA = 2          # antialiasing da hipotenusa
TOLERANCIA = 12    # por canal

# #C84B31 (coral da marca) com opacity 0.75 sobre o branco do slide
CORAL_ESPERADO = tuple(round(0.75 * c + 0.25 * 255) for c in (0xC8, 0x4B, 0x31))


def porta_livre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def servir(porta):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *a, directory=RAIZ, **k
    )
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", porta), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def pixels_corrompidos(caminho_png):
    """Pixels do interior do triangulo que nao estao na cor esperada."""
    img = Image.open(caminho_png).convert("RGB")
    px = img.load()
    ruins = []
    for y in range(ALTURA_TOP_BAR, LADO):
        for x in range(LARGURA - LADO, LARGURA):
            # dentro do triangulo (vertices em 1200,0 / 1280,0 / 1280,80)
            if x < (LARGURA - LADO) + y + FOLGA:
                continue
            if x > LARGURA - FOLGA or y > LADO - FOLGA:
                continue
            cor = px[x, y]
            if max(abs(a - b) for a, b in zip(cor, CORAL_ESPERADO)) > TOLERANCIA:
                ruins.append((x, y, cor))
    return ruins


def checar(page, url, nome, tmp_dir):
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(900)
    # Sem transicao: screenshot no meio da animacao mede o slide errado.
    page.evaluate("() => Reveal.configure({transition: 'none'})")
    total = page.evaluate(
        "() => document.querySelectorAll('.reveal .slides > section').length"
    )

    problemas = 0
    conferidos = 0
    for i in range(total):
        page.evaluate("i => Reveal.slide(i, 0)", i)
        page.wait_for_timeout(300)
        dados = page.evaluate(
            """() => {
                const s = document.querySelector('.reveal .slides section.present');
                const r = s.getBoundingClientRect();
                return {rect: [r.left, r.top, r.width, r.height],
                        decor: !!s.querySelector('.decor-coral')};
            }"""
        )
        if [round(v) for v in dados["rect"]] != [0, 0, LARGURA, ALTURA]:
            print("  slide %-2d  ainda em transicao, medida descartada" % i)
            problemas += 1
            continue
        if not dados["decor"]:
            continue

        destino = os.path.join(tmp_dir, "_canto_%02d.png" % i)
        page.screenshot(path=destino)
        ruins = pixels_corrompidos(destino)
        os.remove(destino)
        conferidos += 1
        if ruins:
            problemas += 1
            print(
                "  slide %-2d  %d pixels do triangulo coral cobertos, ex.: %s"
                % (i, len(ruins), ruins[:3])
            )

    print("\n%s  (%d slides, %d com decor-coral)" % (nome, total, conferidos))
    if not problemas:
        print("  OK: triangulo coral inteiro em todos os slides")
    return problemas


def main():
    alvos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not alvos:
        alvos = sorted(glob.glob(os.path.join(RAIZ, "aulas-1sem", "aulas", "*.html")))

    porta = porta_livre()
    srv = servir(porta)
    tmp_dir = os.path.join(RAIZ, ".canto-coral-tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    total = 0
    try:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            pagina = navegador.new_page(
                viewport={"width": LARGURA, "height": ALTURA}
            )
            for alvo in alvos:
                rel = os.path.relpath(os.path.abspath(alvo), RAIZ)
                url = "http://127.0.0.1:%d/%s" % (porta, rel.replace(os.sep, "/"))
                total += checar(pagina, url, os.path.basename(alvo), tmp_dir)
            navegador.close()
    finally:
        srv.shutdown()
        if os.path.isdir(tmp_dir) and not os.listdir(tmp_dir):
            os.rmdir(tmp_dir)

    print("\n" + "=" * 62)
    if total:
        print("%d slide(s) com o triangulo coral coberto." % total)
        return 1
    print("Triangulo coral inteiro em todos os decks conferidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
