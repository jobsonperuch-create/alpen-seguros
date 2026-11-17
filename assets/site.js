/* Alpen Seguros — fotos ao rolar, abas, formulário de cotação */
(function () {
  // Fotos aparecem quando entram na tela
  var figs = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    figs.forEach(function (f) { io.observe(f); });
  } else {
    figs.forEach(function (f) { f.classList.add('in'); });
  }

  // Abas que filtram os cards de seguro
  var tabs = document.querySelectorAll('.tabs button');
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      var seg = b.getAttribute('data-seg');
      tabs.forEach(function (t) { t.setAttribute('aria-pressed', t === b ? 'true' : 'false'); });
      document.querySelectorAll('.cards li').forEach(function (li) {
        li.hidden = seg !== 'todos' && (' ' + li.getAttribute('data-seg') + ' ').indexOf(' ' + seg + ' ') < 0;
        if (!li.hidden) { var f = li.querySelector('.reveal'); if (f) f.classList.add('in'); }
      });
    });
  });
})();

(function () {
  var WA = '5527999857302';
  var form = document.getElementById('cotacao');
  if (!form) return;
  var err = document.getElementById('err');
  var nome = document.getElementById('nome');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function goToForm() {
    form.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    setTimeout(function () { nome.focus({ preventScroll: true }); }, 450);
  }
  document.querySelectorAll('[data-focus]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); goToForm(); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var n = nome.value.trim();
    if (!n) {
      err.textContent = 'Digite seu nome para o corretor saber com quem está falando.';
      nome.focus();
      return;
    }
    err.textContent = '';
    var p = form.querySelector('input[name="produto"]:checked').value;
    var c = document.getElementById('cidade').value.trim();
    var msg = 'Olá! Sou ' + n + (c ? ' de ' + c : '') + '. Quero uma cotação de ' + p + '.';
    if (typeof window.alpenConversao === 'function') window.alpenConversao();
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
  });

  // Esconde a barra fixa do celular enquanto o formulário está na tela
  var bar = document.querySelector('.mbar');
  if (bar && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      bar.classList.toggle('hide', entries[0].isIntersecting);
    }, { threshold: 0.15 }).observe(form);
  }
})();
