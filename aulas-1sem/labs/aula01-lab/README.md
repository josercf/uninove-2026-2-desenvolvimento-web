# Laboratório da Aula 01

## Disciplina: Desenvolvimento Web
**Prof. José Romualdo | Uninove, Universidade Nove de Julho**

### Case: Clínica Vida+ (Fase 0, ambiente e versionamento)

O entregável de hoje não é código do sistema. É o ambiente de trabalho
montado e funcionando, e o primeiro commit de autoria sua no repositório da
Clínica Vida+, o case que vai atravessar as vinte aulas do semestre. A
partir da próxima aula, cada encontro faz esse mesmo sistema avançar um
passo concreto.

**Duração:** 60 minutos, individual.

---

## Pré-requisitos

- Conta no GitHub.
- Git instalado na máquina.
- VS Code.

---

## Passo 1: conta no GitHub e fork (15 min)

1. Crie ou confirme a sua conta em `github.com`. Use um nome de usuário
   profissional: esse endereço vira portfólio.
2. Abra o repositório-esqueleto
   [`github.com/josercf/uninove-2026-2-clinica-vida`](https://github.com/josercf/uninove-2026-2-clinica-vida).
3. Clique em **Fork** e confirme a criação da cópia sob a sua conta.
4. Confira que a página do seu repositório mostra
   `forked from josercf/uninove-2026-2-clinica-vida`.

Esse fork é o **seu repositório do semestre inteiro**. As vinte aulas evoluem
esse mesmo projeto, aula após aula. Não crie um repositório novo a cada
encontro.

---

## Passo 2: clonar o fork (10 min)

O clone traz o repositório inteiro, com todo o histórico, para a sua
máquina. Troque `SEU-USUARIO` pelo seu nome de usuário do GitHub.

```bash
git --version

git clone https://github.com/SEU-USUARIO/uninove-2026-2-clinica-vida.git
cd uninove-2026-2-clinica-vida

git log --oneline
```

Repare no `git log`: o histórico do projeto veio junto. Isso é o Git ser
**distribuído**. Abra a pasta no editor e leia o `README.md` antes de
seguir.

---

## Passo 3: identidade no Git (10 min)

A identidade é o que assina cada commit. Sem ela configurada, o seu
trabalho não é atribuído a você.

```bash
git config --global user.name "Nome Sobrenome"
git config --global user.email "email@exemplo.com"

git config user.name
git config user.email
```

O e-mail precisa ser **o mesmo cadastrado no GitHub**. Se for outro, os
commits aparecem no repositório mas não contam no seu perfil.

---

## Passo 4: editar o README (15 min)

Acrescente ao `README.md` do seu fork o bloco de identificação, preenchendo
nome completo, RA e turma:

```markdown
## Identificação

- **Nome completo:**
- **RA:**
- **Turma:** (quarta ou quinta)
```

```bash
git status              # o README aparece como modificado
git add README.md
git status              # agora ele aparece pronto para o commit
```

O `git add` não salva nada: ele escolhe **o que vai entrar na próxima
fotografia**. É por isso que o `git status` muda de resposta entre um
comando e outro.

---

## Passo 5: commit e push (10 min)

```bash
git commit -m "docs: identificação do aluno no README"

git log --oneline       # o seu commit, com o hash, no histórico

git push
```

Repare no padrão da mensagem: verbo no presente, escopo curto e a intenção
explícita. Atualize a página do seu fork no GitHub: o commit precisa
aparecer no histórico, com o seu nome ao lado.

---

## Entregável

- Link do seu fork no GitHub.
- Pelo menos **um commit de sua autoria**, visível no histórico e assinado
  com o nome e o e-mail configurados no Passo 3.

---

## Se algo der errado

- **`Permission denied (publickey)`**: o Git tentou autenticar por SSH sem
  uma chave cadastrada na sua conta. Como o clone do Passo 2 usa HTTPS, isso
  costuma acontecer se o remoto foi trocado para SSH em algum momento.
  Resolve com:
  ```bash
  git remote set-url origin https://github.com/SEU-USUARIO/uninove-2026-2-clinica-vida.git
  ```
- **`Author identity unknown`**: o `user.name` e o `user.email` não foram
  configurados antes do commit. Resolve repetindo os comandos do Passo 3:
  ```bash
  git config --global user.name "Nome Sobrenome"
  git config --global user.email "email@exemplo.com"
  ```
- **`fatal: not a git repository`**: o comando foi executado fora da pasta
  do repositório clonado, geralmente porque o `cd` do Passo 2 foi
  esquecido. Resolve entrando na pasta certa:
  ```bash
  cd uninove-2026-2-clinica-vida
  ```
