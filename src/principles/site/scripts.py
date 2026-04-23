"""Client-side JavaScript served alongside the static site."""

FILTER_JS = """\
(function () {
  var input = document.getElementById('principle-filter');
  var table = document.getElementById('principle-index');
  var countEl = document.getElementById('filter-count');
  if (!input || !table) return;
  var rows = Array.prototype.slice.call(table.tBodies[0].rows);
  var total = rows.length;

  function update() {
    var q = input.value.toLowerCase().trim();
    var shown = 0;
    rows.forEach(function (r) {
      var ok = !q || r.dataset.search.indexOf(q) !== -1;
      r.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    if (countEl) countEl.textContent = q ? shown + ' / ' + total : '';
  }

  input.addEventListener('input', update);
})();
"""
