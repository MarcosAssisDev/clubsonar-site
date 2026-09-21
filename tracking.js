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

  // Meta Pixel (só carrega se configurado)
  if (C.metaPixelId) {
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq("init", C.metaPixelId);
    window.fbq("track", "PageView");
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
  track("page_view_ponte");
})();
