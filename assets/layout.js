// Cabeçalho com menu, rodapé e botões de entrada — compartilhado por todas as páginas.
// Carregar depois de /config.js e /tracking.js. Páginas novas ganham o menu automaticamente.
(function () {
  var cfg = window.SONAR_CONFIG || { niches: {}, campaignTypes: {} };
  var here = location.pathname.replace(/\/index\.html$/, "").replace(/\/$/, "") || "/";
  var groups = Object.keys(cfg.niches).filter(function (k) { return cfg.niches[k].active; })
    .map(function (k) { var n = cfg.niches[k]; return { key: k, n: n, path: n.path || "/" + k }; });

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (a) { e.setAttribute(a, attrs[a]); });
    if (text) e.textContent = text;
    return e;
  }
  function link(path, label) {
    var a = el("a", { href: path }, label);
    if (path === here) a.setAttribute("aria-current", "page");
    return a;
  }

  // Cabeçalho
  var header = el("header", { "class": "site-header" }), wrap = el("div", { "class": "wrap" });
  var logo = el("a", { "class": "logo", href: "/", "aria-label": "Club Sonar — início" });
  logo.appendChild(el("span", { "class": "logo-dot", "aria-hidden": "true" }));
  logo.appendChild(document.createTextNode("CLUB SONAR"));
  var btn = el("button", { "class": "menu-btn", type: "button", "aria-expanded": "false", "aria-controls": "site-menu" }, "☰ Grupos");
  var menu = el("nav", { "class": "menu", id: "site-menu", "aria-label": "Grupos" });
  menu.appendChild(link("/", "🏠 Início · todos os grupos"));
  menu.appendChild(el("hr"));
  groups.forEach(function (g) { menu.appendChild(link(g.path, (g.n.emoji ? g.n.emoji + " " : "") + g.n.title)); });
  btn.addEventListener("click", function (ev) {
    ev.stopPropagation();
    var open = menu.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("click", function (ev) {
    if (!menu.contains(ev.target)) { menu.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") { menu.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
  });
  wrap.appendChild(logo); wrap.appendChild(btn); wrap.appendChild(menu);
  header.appendChild(wrap);
  document.body.insertBefore(header, document.body.firstChild);

  // Rodapé
  var footer = el("footer", { "class": "site-footer" }), fw = el("div", { "class": "wrap" }), fnav = el("nav", { "aria-label": "Rodapé" });
  fnav.appendChild(link("/", "Início"));
  groups.forEach(function (g) { fnav.appendChild(link(g.path, g.n.title)); });
  fw.appendChild(fnav);
  fw.appendChild(el("p", null, "Grupos gratuitos de ofertas no WhatsApp · Não pedimos seus dados."));
  fw.appendChild(el("p", null, "Como afiliados, podemos receber comissão por compras feitas pelos links, sem custo extra para você. Preços e estoque podem mudar a qualquer momento."));
  footer.appendChild(fw);
  document.body.appendChild(footer);

  // Botões de entrada: <a class="cta" data-join="pet">
  var enabled = cfg.campaignTypes.GROUP_ACQUISITION && cfg.campaignTypes.GROUP_ACQUISITION.enabled;
  document.querySelectorAll("[data-join]").forEach(function (a) {
    var key = a.getAttribute("data-join"), n = cfg.niches[key];
    if (!enabled || !n || !n.active || !n.groupUrl) {
      a.setAttribute("aria-disabled", "true"); a.textContent = "Em breve"; return;
    }
    a.href = n.groupUrl; a.rel = "noopener";
    a.addEventListener("click", function () {
      if (window.SonarTrack) window.SonarTrack.track("group_join_click", { group: n.groupName, niche: key, from: a.getAttribute("data-from") || here });
    });
  });
})();
