/**
 * Uninove Quiz System for Reveal.js
 * Sistema de quizzes interativos para as aulas
 *
 * Suporta três padrões de markup:
 *
 * 1) Lista (padrão usado pelos decks das aulas):
 *    <div class="quiz-container">
 *      <div class="quiz-question">Enunciado</div>
 *      <ul class="quiz-options">
 *        <li data-correct="false"><span class="option-letter">A</span> Opção A</li>
 *        <li data-correct="true"><span class="option-letter">B</span> Opção B</li>
 *      </ul>
 *      <div class="quiz-feedback"
 *           data-correct-msg="Mensagem quando acerta"
 *           data-incorrect-msg="Mensagem quando erra"></div>
 *    </div>
 *
 * 2) Label/radio:
 *    <ul class="quiz-options">
 *      <label><input type="radio" name="q1" value="a"> Opção A</label>
 *      <label><input type="radio" name="q1" value="b"> Opção B</label>
 *    </ul>
 *
 * 3) Button (legacy):
 *    <ul>
 *      <li><button class="quiz-option" data-value="a">Opção A</button></li>
 *    </ul>
 *
 * Nos padrões 2 e 3 a section deve ter:
 *   data-correct="valor_correto"
 *   data-quiz-feedback="Texto de feedback"
 *
 * No padrão 1 a resposta certa é o <li data-correct="true"> e as mensagens
 * vêm dos atributos data-correct-msg / data-incorrect-msg do .quiz-feedback.
 */

(function () {
  'use strict';

  function initQuizzes() {
    var quizSlides = document.querySelectorAll('.quiz-slide');
    for (var i = 0; i < quizSlides.length; i++) {
      setupQuiz(quizSlides[i]);
    }
  }

  function setupQuiz(slide) {
    // Os listeners são registrados uma única vez por slide. Revisitar o slide
    // apenas limpa o estado visual (ver resetQuizOnSlideChange); registrar de
    // novo acumularia handlers a cada visita.
    if (slide._quizInit) return;
    slide._quizInit = true;

    // Detectar qual padrão está sendo usado
    var labels = slide.querySelectorAll('.quiz-options label');
    var buttons = slide.querySelectorAll('button.quiz-option');
    var items = slide.querySelectorAll('.quiz-options li[data-correct]');

    if (labels.length > 0) {
      initLabelQuiz(slide, labels);
    } else if (buttons.length > 0) {
      initButtonQuiz(slide, buttons);
    } else if (items.length > 0) {
      initListQuiz(slide, items);
    }
  }

  /**
   * Padrão lista: ul.quiz-options > li[data-correct="true|false"]
   * As mensagens vêm do próprio .quiz-feedback (data-correct-msg/data-incorrect-msg).
   */
  function initListQuiz(slide, items) {
    var feedbackEl = slide.querySelector('.quiz-feedback');
    var answered = false;

    for (var i = 0; i < items.length; i++) {
      (function (item) {
        item.addEventListener('click', function () {
          if (answered) return;
          answered = true;

          var isCorrect = item.getAttribute('data-correct') === 'true';

          for (var j = 0; j < items.length; j++) {
            var li = items[j];
            li.style.pointerEvents = 'none';

            if (li.getAttribute('data-correct') === 'true') {
              li.classList.add('is-correct');
            } else if (li === item) {
              li.classList.add('is-wrong');
            } else {
              li.classList.add('is-dimmed');
            }
          }

          showFeedback(feedbackEl, isCorrect, null);
        });
      })(items[i]);
    }

    slide._quizReset = function () { answered = false; };
  }

  /**
   * Padrão label/radio: ul.quiz-options > label > input[type="radio"]
   */
  function initLabelQuiz(slide, labels) {
    var feedbackEl = slide.querySelector('.quiz-feedback');
    var correctAnswer = slide.getAttribute('data-correct');
    var feedbackText = slide.getAttribute('data-quiz-feedback') || '';
    var answered = false;

    for (var i = 0; i < labels.length; i++) {
      (function(label) {
        label.addEventListener('click', function () {
          if (answered) return;

          var radio = label.querySelector('input[type="radio"]');
          if (!radio) return;
          radio.checked = true;

          answered = true;
          var selectedValue = radio.value;
          var isCorrect = selectedValue === correctAnswer;

          // Estilizar todas as labels
          for (var j = 0; j < labels.length; j++) {
            var lbl = labels[j];
            var inp = lbl.querySelector('input[type="radio"]');
            lbl.style.pointerEvents = 'none';
            lbl.style.transition = 'all 0.3s ease';

            if (inp && inp.value === correctAnswer) {
              lbl.style.background = '#eafaf1';
              lbl.style.borderColor = '#27ae60';
              lbl.style.borderLeftColor = '#27ae60';
              lbl.style.color = '#1e8449';
              lbl.style.fontWeight = '700';
            } else if (lbl === label && !isCorrect) {
              lbl.style.background = '#fdedec';
              lbl.style.borderColor = '#e74c3c';
              lbl.style.borderLeftColor = '#e74c3c';
              lbl.style.color = '#c0392b';
              lbl.style.textDecoration = 'line-through';
            } else {
              lbl.style.opacity = '0.4';
            }
          }

          showFeedback(feedbackEl, isCorrect, feedbackText);
        });
      })(labels[i]);
    }

    // Guardar referências para reset
    slide._quizLabels = labels;
    slide._quizAnswered = function() { return answered; };
    slide._quizReset = function() { answered = false; };
  }

  /**
   * Padrão button (legacy): button.quiz-option com data-value
   */
  function initButtonQuiz(slide, buttons) {
    var feedbackEl = slide.querySelector('.quiz-feedback');
    var correctAnswer = slide.getAttribute('data-correct');
    var feedbackText = slide.getAttribute('data-quiz-feedback') || '';
    var answered = false;

    for (var i = 0; i < buttons.length; i++) {
      (function(btn) {
        btn.addEventListener('click', function () {
          if (answered) return;
          answered = true;

          var selectedValue = btn.getAttribute('data-value');
          var isCorrect = selectedValue === correctAnswer;

          // Estilizar todos os botões
          for (var j = 0; j < buttons.length; j++) {
            var b = buttons[j];
            b.style.pointerEvents = 'none';
            b.style.transition = 'all 0.3s ease';

            if (b.getAttribute('data-value') === correctAnswer) {
              b.style.background = '#eafaf1';
              b.style.borderColor = '#27ae60';
              b.style.borderLeftColor = '#27ae60';
              b.style.color = '#1e8449';
              b.style.fontWeight = '700';
            } else if (b === btn && !isCorrect) {
              b.style.background = '#fdedec';
              b.style.borderColor = '#e74c3c';
              b.style.borderLeftColor = '#e74c3c';
              b.style.color = '#c0392b';
              b.style.textDecoration = 'line-through';
            } else {
              b.style.opacity = '0.4';
            }
          }

          showFeedback(feedbackEl, isCorrect, feedbackText);
        });
      })(buttons[i]);
    }

    slide._quizButtons = buttons;
    slide._quizAnswered = function() { return answered; };
    slide._quizReset = function() { answered = false; };
  }

  /**
   * Exibir feedback do quiz
   */
  function showFeedback(feedbackEl, isCorrect, feedbackText) {
    if (!feedbackEl) return;

    // feedbackText null => usar as mensagens declaradas no próprio elemento,
    // que já vêm redigidas por extenso (não recebem prefixo).
    var message;
    if (feedbackText === null) {
      message = feedbackEl.getAttribute(
        isCorrect ? 'data-correct-msg' : 'data-incorrect-msg'
      ) || '';
    } else {
      message = (isCorrect ? 'Correto! ' : 'Incorreto. ') + feedbackText;
    }

    feedbackEl.className = 'quiz-feedback ' + (isCorrect ? 'correct' : 'incorrect');
    feedbackEl.innerHTML = message;
  }

  /**
   * Reset do quiz ao mudar de slide (permite refazer ao voltar)
   */
  function resetQuizOnSlideChange() {
    Reveal.on('slidechanged', function(event) {
      var prevSlide = event.previousSlide;
      if (!prevSlide || !prevSlide.classList.contains('quiz-slide')) return;

      // Reset labels
      var labels = prevSlide.querySelectorAll('.quiz-options label');
      for (var i = 0; i < labels.length; i++) {
        labels[i].style.pointerEvents = '';
        labels[i].style.background = '';
        labels[i].style.borderColor = '';
        labels[i].style.borderLeftColor = '';
        labels[i].style.color = '';
        labels[i].style.fontWeight = '';
        labels[i].style.textDecoration = '';
        labels[i].style.opacity = '';
      }

      // Reset buttons
      var buttons = prevSlide.querySelectorAll('button.quiz-option');
      for (var j = 0; j < buttons.length; j++) {
        buttons[j].style.pointerEvents = '';
        buttons[j].style.background = '';
        buttons[j].style.borderColor = '';
        buttons[j].style.borderLeftColor = '';
        buttons[j].style.color = '';
        buttons[j].style.fontWeight = '';
        buttons[j].style.textDecoration = '';
        buttons[j].style.opacity = '';
      }

      // Reset itens de lista
      var items = prevSlide.querySelectorAll('.quiz-options li[data-correct]');
      for (var n = 0; n < items.length; n++) {
        items[n].style.pointerEvents = '';
        items[n].classList.remove('is-correct', 'is-wrong', 'is-dimmed');
      }

      // Reset radios
      var radios = prevSlide.querySelectorAll('input[type="radio"]');
      for (var k = 0; k < radios.length; k++) {
        radios[k].checked = false;
      }

      // Reset feedback (limpar o inline display para a classe voltar a mandar)
      var feedbackEl = prevSlide.querySelector('.quiz-feedback');
      if (feedbackEl) {
        feedbackEl.style.display = '';
        feedbackEl.className = 'quiz-feedback';
        feedbackEl.innerHTML = '';
      }

      // Reset answered state (os listeners continuam registrados)
      if (prevSlide._quizReset) {
        prevSlide._quizReset();
      }
    });
  }

  /**
   * Timer regressivo para quizzes e intervalo.
   *
   *   startTimer('quiz1Timer', 60)   // 60 segundos
   *   startTimer('breakTimer', 1800) // 30 minutos
   *
   * A duração é sempre em SEGUNDOS. Chamadas repetidas no mesmo elemento são
   * ignoradas enquanto o timer estiver correndo, para que apertar o play duas
   * vezes não crie dois intervalos disputando o mesmo display.
   */
  var runningTimers = {};

  window.startTimer = function (elementId, seconds) {
    var el = document.getElementById(elementId);
    if (!el || runningTimers[elementId]) return;

    var remaining = seconds;

    function render() {
      var mins = Math.floor(remaining / 60);
      var secs = remaining % 60;
      el.textContent = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
    }

    render();
    el.classList.remove('timer-done');

    var interval = setInterval(function () {
      remaining--;
      render();
      if (remaining <= 0) {
        clearInterval(interval);
        delete runningTimers[elementId];
        el.textContent = 'TEMPO ESGOTADO';
        el.classList.add('timer-done');
      }
    }, 1000);

    runningTimers[elementId] = interval;
    return interval;
  };

  function boot() {
    initQuizzes();
    if (typeof Reveal !== 'undefined' && Reveal.isReady && Reveal.isReady()) {
      resetQuizOnSlideChange();
    } else if (typeof Reveal !== 'undefined') {
      Reveal.on('ready', function() {
        initQuizzes();
        resetQuizOnSlideChange();
      });
    }
  }

  if (document.readyState === 'complete') {
    setTimeout(boot, 500);
  } else {
    window.addEventListener('load', function() { setTimeout(boot, 500); });
  }

})();
