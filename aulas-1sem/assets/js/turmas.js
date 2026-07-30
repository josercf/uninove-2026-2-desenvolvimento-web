/**
 * Turmas de Desenvolvimento Web, Uninove 2026.2.
 *
 * O conteudo das duas turmas e identico; o que muda e o calendario. Este modulo
 * concentra as datas e a regra de qual turma exibir.
 *
 * Datas sao sempre montadas componente a componente. `new Date('2026-08-05')`
 * seria interpretado como meia-noite UTC e viraria 04/08 no fuso de Sao Paulo.
 */

export const TURMAS = {
  quarta: {
    rotulo: 'Quarta-feira',
    identificador: null, // preencher quando a instituicao divulgar
    datas: [
      '2026-08-05', '2026-08-12', '2026-08-19', '2026-08-26', '2026-09-02',
      '2026-09-09', '2026-09-16', '2026-09-23', '2026-09-30', '2026-10-07',
      '2026-10-14', '2026-10-21', '2026-10-28', '2026-11-04', '2026-11-11',
      '2026-11-18', '2026-11-25', '2026-12-02', '2026-12-09', '2026-12-16',
    ],
  },
  quinta: {
    rotulo: 'Quinta-feira',
    identificador: null,
    datas: [
      '2026-08-06', '2026-08-13', '2026-08-20', '2026-08-27', '2026-09-03',
      '2026-09-10', '2026-09-17', '2026-09-24', '2026-10-01', '2026-10-08',
      '2026-10-15', '2026-10-22', '2026-10-29', '2026-11-05', '2026-11-12',
      '2026-11-19', '2026-11-26', '2026-12-03', '2026-12-10', '2026-12-17',
    ],
  },
};

const DIA_DA_SEMANA = { 3: 'quarta', 4: 'quinta' };

/**
 * Decide qual turma exibir.
 *
 * @param {{ hoje: Date, salva: string|null }} entrada
 * @returns {'quarta'|'quinta'|null} null quando nao ha como decidir sozinho
 */
export function resolverTurma({ hoje, salva }) {
  if (salva === 'quarta' || salva === 'quinta') return salva;
  return DIA_DA_SEMANA[hoje.getDay()] || null;
}

/**
 * Data do enesimo encontro de uma turma.
 *
 * @param {'quarta'|'quinta'} turma
 * @param {number} numeroDaAula de 1 a 20
 * @returns {Date} data local, sem deslocamento de fuso
 */
export function dataDaAula(turma, numeroDaAula) {
  const dados = TURMAS[turma];
  if (!dados) throw new Error(`turma desconhecida: ${turma}`);
  if (!Number.isInteger(numeroDaAula) || numeroDaAula < 1 || numeroDaAula > dados.datas.length) {
    throw new Error(`numero de aula fora da faixa: ${numeroDaAula}`);
  }
  const [ano, mes, dia] = dados.datas[numeroDaAula - 1].split('-').map(Number);
  return new Date(ano, mes - 1, dia);
}

/**
 * @param {Date} data
 * @returns {string} no formato DD/MM/AAAA
 */
export function formatarData(data) {
  const dd = String(data.getDate()).padStart(2, '0');
  const mm = String(data.getMonth() + 1).padStart(2, '0');
  return `${dd}/${mm}/${data.getFullYear()}`;
}
