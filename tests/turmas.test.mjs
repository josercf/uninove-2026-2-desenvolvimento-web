import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  TURMAS,
  resolverTurma,
  dataDaAula,
  formatarData,
} from '../aulas-1sem/assets/js/turmas.js';

test('cada turma tem 20 encontros', () => {
  assert.equal(TURMAS.quarta.datas.length, 20);
  assert.equal(TURMAS.quinta.datas.length, 20);
});

test('as datas de quarta caem todas numa quarta-feira', () => {
  for (const iso of TURMAS.quarta.datas) {
    const [a, m, d] = iso.split('-').map(Number);
    assert.equal(new Date(a, m - 1, d).getDay(), 3, `${iso} nao e quarta`);
  }
});

test('as datas de quinta caem todas numa quinta-feira', () => {
  for (const iso of TURMAS.quinta.datas) {
    const [a, m, d] = iso.split('-').map(Number);
    assert.equal(new Date(a, m - 1, d).getDay(), 4, `${iso} nao e quinta`);
  }
});

test('quarta-feira resolve para a turma de quarta', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 5), salva: null }), 'quarta');
});

test('quinta-feira resolve para a turma de quinta', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 6), salva: null }), 'quinta');
});

test('outro dia da semana nao resolve turma nenhuma', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 8), salva: null }), null);
});

test('a turma salva tem precedencia sobre o dia da semana', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 5), salva: 'quinta' }), 'quinta');
});

test('valor salvo invalido e ignorado e cai no dia da semana', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 6), salva: 'sexta' }), 'quinta');
});

test('valor salvo invalido num dia sem aula devolve null', () => {
  assert.equal(resolverTurma({ hoje: new Date(2026, 7, 8), salva: 'sexta' }), null);
});

test('dataDaAula devolve a data local correta, sem deslocamento de fuso', () => {
  const d = dataDaAula('quarta', 1);
  assert.equal(d.getDate(), 5);
  assert.equal(d.getMonth(), 7);
  assert.equal(d.getFullYear(), 2026);
});

test('dataDaAula cobre da aula 1 a aula 20', () => {
  assert.equal(formatarData(dataDaAula('quarta', 20)), '16/12/2026');
  assert.equal(formatarData(dataDaAula('quinta', 20)), '17/12/2026');
});

test('dataDaAula rejeita numero fora da faixa', () => {
  assert.throws(() => dataDaAula('quarta', 0), /fora da faixa/);
  assert.throws(() => dataDaAula('quarta', 21), /fora da faixa/);
});

test('dataDaAula rejeita turma desconhecida', () => {
  assert.throws(() => dataDaAula('sexta', 1), /turma desconhecida/);
});

test('formatarData usa o padrao brasileiro com dois digitos', () => {
  assert.equal(formatarData(new Date(2026, 7, 5)), '05/08/2026');
  assert.equal(formatarData(new Date(2026, 11, 16)), '16/12/2026');
});
