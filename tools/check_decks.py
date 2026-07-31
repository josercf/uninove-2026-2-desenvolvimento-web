#!/usr/bin/env python3
"""
Valida a estrutura de cada deck aulaXX.html, de forma estatica.

POR QUE ESTE SCRIPT EXISTE
--------------------------
`check_slides.py` mede geometria e `check_canto_coral.py` mede pixel: os dois
abrem o navegador e olham como o slide ficou. Nenhum dos dois olha o CONTEUDO
do arquivo. Com as Aulas 02 a 20 sendo produzidas a partir de copias da Aula
01, os defeitos mais caros sao justamente os que passam ilesos por geometria e
por pixel:

  - um deck copiado da Aula 01 sem trocar `data-data-da-aula` projeta a data da
    Aula 01 em sala, e passa em todos os outros validadores;
  - um `<div class="decor-coral">` esquecido nao gera erro nenhum: o triangulo
    simplesmente nao aparece, e o `check_canto_coral.py` pula o slide porque
    so confere slides que TEM o elemento;
  - `class="quiz-slide"` sem `content-slide` perde a top-bar, a logo e o
    rodape, porque o CSS so define essas barras para `content-slide`;
  - dois `data-correct="true"` no mesmo quiz fazem o script pintar duas
    respostas de verde;
  - `href="#/ref-slide"` sem o `id="ref-slide"` correspondente e um link morto;
  - rodape fora de sequencia depois de inserir ou remover um slide;
  - `src` ou `href` relativo apontando para arquivo que nao existe da 404 no
    GitHub Pages, que nao faz listagem de diretorio;
  - `<code>` solto dentro de uma alternativa de quiz parte a frase na
    projecao, porque a `li` e um contexto de flex (ADR-007). Este defeito
    escapou tres vezes, em tres decks diferentes, antes de virar checagem.

AS OITO CHECAGENS
-----------------
1. Existe exatamente um `data-data-da-aula` no deck, e o valor e igual ao
   numero da aula no nome do arquivo (`aula05.html` exige valor 5).
2. Toda `section` com classe `content-slide`, `quiz-slide` ou `exercise-slide`
   tem um `<div class="decor-coral">`.
3. Toda `quiz-slide` e `exercise-slide` tambem tem `content-slide` na lista de
   classes.
4. Todo `.quiz-container` tem exatamente um `data-correct="true"`.
5. Toda ancora interna `href="#/..."` aponta para um `id` que existe no
   documento (indice numerico de slide, `#/7`, e aceito se estiver dentro da
   faixa de slides do deck).
6. Os `footer-page` formam sequencia crescente, sem pular nem repetir.
7. Todo `src` e `href` relativo a arquivo local existe no disco. Diretorio so
   conta como existente se tiver `index.html` dentro, porque e assim que o
   GitHub Pages se comporta.
8. Nenhuma alternativa de quiz tem elemento inline solto como filho direto da
   `<li>`: so `.option-letter` e `.option-text` sao permitidos. A `li` e
   `display: flex` com `gap: 12px`, entao um `<code>` solto vira item de flex
   proprio e a frase se parte com 12px de buraco de cada lado (ADR-007).

NUMERACAO DOS SLIDES
--------------------
Os slides sao reportados em BASE 0, a mesma base de `check_slides.py`,
`check_canto_coral.py` e `Reveal.slide(i)`. O primeiro slide do deck e o
slide 0.

Sai com codigo 1 e imprime aula, slide e problema se qualquer checagem falhar.

Uso:
    python3 tools/check_decks.py                       # todos os decks
    python3 tools/check_decks.py aulas-1sem/aulas/aula01.html

Nao requer Playwright: le o HTML direto do disco.
"""
import glob
import io
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DECKS = os.path.join(RAIZ, "aulas-1sem", "aulas")

CLASSES_QUE_EXIGEM_DECOR = ("content-slide", "quiz-slide", "exercise-slide")
CLASSES_QUE_EXIGEM_CONTENT = ("quiz-slide", "exercise-slide")

# Atributos que carregam caminho de arquivo e precisam existir no disco.
ATRIBUTOS_DE_CAMINHO = ("src", "href")

# Esquemas que nao apontam para arquivo local.
ESQUEMAS_EXTERNOS = ("http", "https", "mailto", "tel", "data", "javascript")

# Elementos sem tag de fechamento: nao abrem nivel de aninhamento.
TAGS_VAZIAS = (
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
)

# Os unicos filhos diretos que uma alternativa de quiz pode ter. Qualquer
# outro elemento inline solto vira item de flex proprio (ADR-007).
FILHOS_PERMITIDOS_NA_ALTERNATIVA = ("option-letter", "option-text")


def classes_de(attrs):
    return (attrs.get("class") or "").split()


class LeitorDeDeck(HTMLParser):
    """Percorre o deck uma vez e recolhe tudo o que as oito checagens usam.

    As `section` dos decks nunca sao aninhadas (o Reveal usa slides verticais
    aninhados, que este acervo nao usa), entao 'a secao atual' e sempre a
    ultima aberta.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.secoes = []          # uma entrada por slide, em ordem de documento
        self.ids = set()
        self.datas_da_aula = []   # (valor, linha)
        self.quizzes = []         # {'secao', 'linha', 'corretas'}
        self.ancoras = []         # (alvo, linha, secao)
        self.caminhos = []        # (atributo, valor, linha, secao)
        self.rodapes = []         # (valor_texto, linha, secao)
        self.alternativas = []    # {'secao', 'linha', 'soltos'}
        self._quiz_aberto = None
        self._capturando_rodape = None
        self._quiz_options_aberto = False
        self._li_aberta = None
        self._profundidade_na_li = 0

    # -- utilidades ------------------------------------------------------
    @property
    def secao_atual(self):
        return len(self.secoes) - 1 if self.secoes else None

    # -- eventos do parser -----------------------------------------------
    def handle_starttag(self, tag, attrs):
        self._processar_tag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        # <path ... /> dentro de SVG: conta como abertura, nunca abre bloco.
        self._processar_tag(tag, attrs, autofechada=True)

    def _processar_tag(self, tag, attrs, autofechada=False):
        attrs = {k: (v if v is not None else "") for k, v in attrs}
        linha = self.getpos()[0]
        classes = classes_de(attrs)

        if "id" in attrs and attrs["id"]:
            self.ids.add(attrs["id"])

        if tag == "section":
            self.secoes.append(
                {"linha": linha, "classes": classes, "decor": False}
            )
            self._quiz_aberto = None

        if "decor-coral" in classes and self.secao_atual is not None:
            self.secoes[self.secao_atual]["decor"] = True

        # -- alternativas de quiz (checagem 8) -----------------------------
        # Precisamos saber se um elemento inline e filho DIRETO da <li>: o que
        # esta dentro do `.option-text` ja e um item de flex so, e nao quebra.
        if "quiz-options" in classes:
            self._quiz_options_aberto = True

        if self._quiz_options_aberto and tag == "li" and self._li_aberta is None:
            self._li_aberta = {
                "secao": self.secao_atual,
                "linha": linha,
                "soltos": [],
            }
            self._profundidade_na_li = 0
        elif self._li_aberta is not None:
            if self._profundidade_na_li == 0:
                permitido = any(
                    c in classes for c in FILHOS_PERMITIDOS_NA_ALTERNATIVA
                )
                if not permitido:
                    self._li_aberta["soltos"].append(tag)
            if not autofechada and tag not in TAGS_VAZIAS:
                self._profundidade_na_li += 1

        if "quiz-container" in classes:
            self._quiz_aberto = {
                "secao": self.secao_atual,
                "linha": linha,
                "corretas": 0,
            }
            self.quizzes.append(self._quiz_aberto)

        if attrs.get("data-correct") == "true" and self._quiz_aberto is not None:
            self._quiz_aberto["corretas"] += 1

        if "data-data-da-aula" in attrs:
            self.datas_da_aula.append((attrs["data-data-da-aula"], linha))

        if "footer-page" in classes and not autofechada:
            self._capturando_rodape = {
                "texto": [],
                "linha": linha,
                "secao": self.secao_atual,
            }

        for atributo in ATRIBUTOS_DE_CAMINHO:
            valor = attrs.get(atributo)
            if not valor:
                continue
            if valor.startswith("#"):
                if atributo == "href":
                    self.ancoras.append((valor, linha, self.secao_atual))
                continue
            self.caminhos.append((atributo, valor, linha, self.secao_atual))

    def handle_data(self, data):
        if self._capturando_rodape is not None:
            self._capturando_rodape["texto"].append(data)

    def handle_endtag(self, tag):
        if self._li_aberta is not None:
            if self._profundidade_na_li > 0:
                if tag not in TAGS_VAZIAS:
                    self._profundidade_na_li -= 1
            elif tag == "li":
                self.alternativas.append(self._li_aberta)
                self._li_aberta = None
        if tag == "ul":
            self._quiz_options_aberto = False

        if self._capturando_rodape is not None and tag == "div":
            rodape = self._capturando_rodape
            self._capturando_rodape = None
            self.rodapes.append(
                ("".join(rodape["texto"]).strip(), rodape["linha"], rodape["secao"])
            )


# -- as oito checagens ---------------------------------------------------
def checar_data_da_aula(leitor, numero_da_aula, erros, rotulo):
    if len(leitor.datas_da_aula) != 1:
        erros.append(
            "%s  linha %s: existem %d atributos data-data-da-aula, esperado "
            "exatamente 1"
            % (
                rotulo,
                leitor.datas_da_aula[0][1] if leitor.datas_da_aula else "?",
                len(leitor.datas_da_aula),
            )
        )
        return
    valor, linha = leitor.datas_da_aula[0]
    try:
        numero = int(valor)
    except ValueError:
        erros.append(
            "%s  linha %d: data-data-da-aula vale %r, que nao e um numero"
            % (rotulo, linha, valor)
        )
        return
    if numero != numero_da_aula:
        erros.append(
            "%s  linha %d: data-data-da-aula vale %d, mas o arquivo e da aula "
            "%d. O deck projetaria a data da Aula %02d em sala."
            % (rotulo, linha, numero, numero_da_aula, numero)
        )


def checar_decor_coral(leitor, erros, rotulo):
    for i, secao in enumerate(leitor.secoes):
        if not any(c in secao["classes"] for c in CLASSES_QUE_EXIGEM_DECOR):
            continue
        if not secao["decor"]:
            erros.append(
                "%s  slide %d (linha %d, class=%r): sem <div class=\"decor-coral\">; "
                "o triangulo coral nao aparece e nenhum outro validador acusa"
                % (rotulo, i, secao["linha"], " ".join(secao["classes"]))
            )


def checar_content_slide_em_quiz_e_exercicio(leitor, erros, rotulo):
    for i, secao in enumerate(leitor.secoes):
        for classe in CLASSES_QUE_EXIGEM_CONTENT:
            if classe in secao["classes"] and "content-slide" not in secao["classes"]:
                erros.append(
                    "%s  slide %d (linha %d): class=%r sem 'content-slide'; sem "
                    "ela o slide perde top-bar, logo e rodape, que so existem "
                    "no CSS de .content-slide"
                    % (rotulo, i, secao["linha"], " ".join(secao["classes"]))
                )


def checar_quiz_com_uma_resposta(leitor, erros, rotulo):
    for quiz in leitor.quizzes:
        if quiz["corretas"] != 1:
            erros.append(
                "%s  slide %s (linha %d): .quiz-container com %d "
                "data-correct=\"true\", esperado exatamente 1"
                % (rotulo, quiz["secao"], quiz["linha"], quiz["corretas"])
            )


def checar_alternativas_sem_inline_solto(leitor, erros, rotulo):
    """Checagem 8: alternativa de quiz nao pode ter elemento inline solto.

    `.quiz-slide .quiz-options li` e `display: flex` com `gap: 12px`. Cada
    trecho de texto solto e cada elemento inline vira um item de flex
    separado, entao um `<code>` no meio da alternativa ganha 12px de buraco de
    cada lado, no lugar onde deveria haver um espaco normal, e a frase se parte
    na projecao. A saida e envolver o texto em `<span class="option-text">`.

    Nada disso estoura os 1280x720 nem sobrepoe bloco, entao `check_slides.py`
    aprova. O defeito apareceu tres vezes, em tres decks diferentes, antes de
    virar esta checagem. Ver ADR-007.
    """
    for alt in leitor.alternativas:
        if not alt["soltos"]:
            continue
        tags = ", ".join("<%s>" % t for t in sorted(set(alt["soltos"])))
        erros.append(
            "%s  slide %s (linha %d): alternativa de quiz com %s solto fora de "
            "<span class=\"option-text\">; a li e display:flex com gap:12px, "
            "entao o trecho vira item proprio e a frase se parte na projecao "
            "(ADR-007)" % (rotulo, alt["secao"], alt["linha"], tags)
        )


def checar_ancoras_internas(leitor, erros, rotulo):
    total_de_slides = len(leitor.secoes)
    for alvo, linha, secao in leitor.ancoras:
        if not alvo.startswith("#/"):
            continue
        destino = alvo[2:].strip("/")
        if not destino:
            continue
        if destino.isdigit():
            if int(destino) >= total_de_slides:
                erros.append(
                    "%s  slide %s (linha %d): href=%r aponta para o slide %s, "
                    "mas o deck tem %d slides"
                    % (rotulo, secao, linha, alvo, destino, total_de_slides)
                )
            continue
        if destino not in leitor.ids:
            erros.append(
                "%s  slide %s (linha %d): href=%r nao encontra nenhum id=%r no "
                "documento"
                % (rotulo, secao, linha, alvo, destino)
            )


def checar_sequencia_dos_rodapes(leitor, erros, rotulo):
    anterior = None
    for texto, linha, secao in leitor.rodapes:
        if not texto.isdigit():
            erros.append(
                "%s  slide %s (linha %d): footer-page com %r, que nao e um numero"
                % (rotulo, secao, linha, texto)
            )
            continue
        numero = int(texto)
        if anterior is not None and numero != anterior + 1:
            erros.append(
                "%s  slide %s (linha %d): footer-page %d vem depois de %d; a "
                "sequencia %s"
                % (
                    rotulo,
                    secao,
                    linha,
                    numero,
                    anterior,
                    "repete" if numero == anterior
                    else ("retrocede" if numero < anterior else "pula"),
                )
            )
        anterior = numero


def checar_caminhos_locais(leitor, caminho_do_deck, erros, rotulo):
    base = os.path.dirname(os.path.abspath(caminho_do_deck))
    for atributo, valor, linha, secao in leitor.caminhos:
        if valor.startswith("//"):
            continue
        esquema = urlparse(valor).scheme.lower()
        if esquema in ESQUEMAS_EXTERNOS:
            continue
        if esquema:
            continue
        relativo = unquote(valor.split("#")[0].split("?")[0])
        if not relativo:
            continue
        if os.path.isabs(relativo):
            alvo = os.path.join(RAIZ, relativo.lstrip("/"))
        else:
            alvo = os.path.normpath(os.path.join(base, relativo))
        if os.path.isdir(alvo):
            if os.path.isfile(os.path.join(alvo, "index.html")):
                continue
            erros.append(
                "%s  slide %s (linha %d): %s=%r aponta para um diretorio sem "
                "index.html; o GitHub Pages devolve 404, porque nao faz "
                "listagem de diretorio"
                % (rotulo, secao, linha, atributo, valor)
            )
            continue
        if not os.path.isfile(alvo):
            erros.append(
                "%s  slide %s (linha %d): %s=%r nao existe no disco (%s)"
                % (rotulo, secao, linha, atributo, valor,
                   os.path.relpath(alvo, RAIZ))
            )


def numero_da_aula_no_nome(caminho):
    achado = re.search(r"aula(\d+)\.html$", os.path.basename(caminho))
    return int(achado.group(1)) if achado else None


def checar_deck(caminho, erros):
    rotulo = os.path.basename(caminho)
    numero = numero_da_aula_no_nome(caminho)
    if numero is None:
        erros.append(
            "%s: nome fora do padrao aulaXX.html; nao da para conferir a data "
            "da aula" % rotulo
        )
        return 0

    leitor = LeitorDeDeck()
    leitor.feed(io.open(caminho, encoding="utf-8").read())
    leitor.close()

    antes = len(erros)
    checar_data_da_aula(leitor, numero, erros, rotulo)
    checar_decor_coral(leitor, erros, rotulo)
    checar_content_slide_em_quiz_e_exercicio(leitor, erros, rotulo)
    checar_quiz_com_uma_resposta(leitor, erros, rotulo)
    checar_alternativas_sem_inline_solto(leitor, erros, rotulo)
    checar_ancoras_internas(leitor, erros, rotulo)
    checar_sequencia_dos_rodapes(leitor, erros, rotulo)
    checar_caminhos_locais(leitor, caminho, erros, rotulo)

    novos = len(erros) - antes
    print(
        "\n%s  (%d slides, %d quiz, %d rodapes)"
        % (rotulo, len(leitor.secoes), len(leitor.quizzes), len(leitor.rodapes))
    )
    if novos:
        print("  %d problema(s):" % novos)
        for erro in erros[antes:]:
            print("  - %s" % erro)
    else:
        print("  OK: as oito checagens estruturais passaram")
    return novos


def main():
    alvos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not alvos:
        alvos = sorted(glob.glob(os.path.join(PASTA_DECKS, "aula*.html")))
    if not alvos:
        print("Nenhum deck encontrado em %s" % os.path.relpath(PASTA_DECKS, RAIZ))
        return 1

    erros = []
    for alvo in alvos:
        checar_deck(alvo, erros)

    print("\n" + "=" * 62)
    if erros:
        print("%d problema(s) estrutural(is) em %d deck(s)." % (len(erros), len(alvos)))
        return 1
    print("Estrutura correta nos %d deck(s) conferido(s)." % len(alvos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
