(function () {
  var C = window.SONAR_CONFIG || {};
  var KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid"];
  var params = new URLSearchParams(location.search);
  var utm = {};
  KEYS.forEach(function (k) { if (params.get(k)) utm[k] = params.get(k); });
  try {
    if (Object.keys(utm).length) sessionStorage.setItem("sonar_utm", JSON.stringify(utm));
    else utm = JSON.parse(sessionStorage.getItem("sonar_utm") || "{}");
  } catch (e) {}

  window.dataLayer = window.dataLayer || [];
  function track(event, extra) {
    var payload = Object.assign({ event: event, landing: location.pathname, campaign_type: "GROUP_ACQUISITION" }, utm, extra || {});
    window.dataLayer.push(payload);
    if (window.fbq) window.fbq("trackCustom", event, payload);
    if (window.gtag) window.gtag("event", event, payload);
  }

  // Meta Pixel: só carrega se configurado E se o visitante aceitou no banner (LGPD).
  // A escolha fica no localStorage ("granted" ou "denied"); sem escolha, o banner aparece e nada da Meta é carregado.
  var CONSENT_KEY = "sonar_consent";
  function getConsent() { try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem(CONSENT_KEY, v); } catch (e) {} }

  function loadPixel() {
    if (window.fbq) { window.fbq("consent", "grant"); return; }
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq("init", C.metaPixelId);
    window.fbq("track", "PageView");
  }

  var banner = null;
  function closeBanner() { if (banner) { banner.remove(); banner = null; } }
  function showBanner() {
    if (banner) return;
    banner = document.createElement("div");
    banner.className = "consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Consentimento de privacidade");
    banner.innerHTML = '<p>Usamos cookies para medir nossos anúncios. <a href="/privacidade">Saiba mais</a></p>' +
      '<div class="row"><button type="button" data-consent="denied">Não, obrigado</button><button type="button" data-consent="granted">OK</button></div>';
    banner.addEventListener("click", function (ev) {
      var v = ev.target.getAttribute && ev.target.getAttribute("data-consent");
      if (!v) return;
      setConsent(v);
      closeBanner();
      if (v === "granted") loadPixel();
      else if (window.fbq) window.fbq("consent", "revoke"); // recusou depois de ter aceitado: para de enviar nesta página
    });
    document.body.appendChild(banner);
  }

  if (C.metaPixelId) {
    var consent = getConsent();
    if (consent === "granted") loadPixel();
    else if (consent !== "denied") showBanner();
    // Link do rodapé "Preferências de privacidade": reabre o banner para rever a escolha
    document.addEventListener("click", function (ev) {
      if (ev.target.closest && ev.target.closest("[data-consent-open]")) showBanner();
    });
  }
  // GA4 (só carrega se configurado)
  if (C.ga4Id) {
    var s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + C.ga4Id;
    document.head.appendChild(s);
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date()); window.gtag("config", C.ga4Id);
  }

  window.SonarTrack = { track: track, utm: utm };
  track("page_view");

  // cta_click: todo botão com data-cta (posição em data-position, variante A/B em data-variant)
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("[data-cta]");
    if (!a) return;
    var niche = a.getAttribute("data-niche"), n = (C.niches || {})[niche] || {};
    track("cta_click", { niche: niche, group: n.groupName, position: a.getAttribute("data-position"), variant: a.getAttribute("data-variant") || "A" });
    if (window.fbq) window.fbq("track", "Lead", { content_name: n.groupName || "grupo", content_category: niche });
  });

  // scroll_50: uma vez por página
  var scrolled = false;
  window.addEventListener("scroll", function () {
    if (scrolled) return;
    var h = document.documentElement;
    if ((h.scrollTop + window.innerHeight) / h.scrollHeight >= 0.5) { scrolled = true; track("scroll_50"); }
  }, { passive: true });
})();
