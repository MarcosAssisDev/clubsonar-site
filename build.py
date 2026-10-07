#!/usr/bin/env python3
"""Gera o site estático a partir do site.json.

Uso:  python3 build.py
Gera: index.html, <nicho>/index.html, <nicho>/entrar/index.html, privacidade/index.html e config.js.
Os arquivos gerados são versionados (o GitHub Pages serve o repositório como está).
Para trocar o link de um grupo (ex.: #101 → #102), edite só o groupUrl no site.json e rode o build.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
DOMAIN = SITE["domain"].rstrip("/")
NICHES = [n for n in SITE["niches"] if n["active"]]

WA_ICON = ('<svg class="wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>')
LOGO = '<div class="hero-logo"><img src="/assets/img/logo.webp" alt="Sonar Ofertas" width="220" height="80"></div>'
E = html.escape


def cf_beacon():
    """Cloudflare Web Analytics: grátis, sem cookies. Só entra se houver token no site.json."""
    t = SITE.get("cfAnalyticsToken")
    if not t:
        return ""
    return ("<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
            f"data-cf-beacon='{json.dumps({'token': t})}'></script>\n")
CUR = ' aria-current="page"'


def head(title, desc, path, og_desc=None, extra="", og_image="/assets/img/og.jpg"):
    url = DOMAIN + path
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(og_desc or desc)}">
<meta property="og:image" content="{DOMAIN}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#1b3b62">
<link rel="stylesheet" href="/assets/site.css">
{extra}{cf_beacon()}</head>
<body>
"""


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False) + "\n</script>\n"


def header(current, menu=True, icon="/assets/img/icon-64.png", name="CLUB SONAR"):
    """Topo: marca pequena; o menu de grupos é <details>, sem JavaScript."""
    links = [("/", "🏠 Início · todos os grupos")] + [("/" + n["key"], f'{n["emoji"]} {n["title"]}') for n in NICHES]
    items = "".join(
        f'<a href="{p}"{CUR if p == current else ""}>{E(t)}</a>' + ("<hr>" if p == "/" else "")
        for p, t in links)
    nav = f'<details class="menu"><summary>☰ Grupos</summary><nav aria-label="Grupos">{items}</nav></details>' if menu else ""
    # Sem menu, a marca também não é link: a única saída da página é o CTA.
    tag = 'a class="logo" href="/"' if menu else 'span class="logo"'
    end = "a" if menu else "span"
    return f"""<header class="site-header"><div class="wrap">
  <{tag}><img src="{icon}" alt="" width="30" height="30">{E(name)}</{end}>
  {nav}
</div></header>
"""


def footer(niche=None, links=True):
    ig = (niche or {}).get("instagram") or SITE["contact"].get("instagram")
    email = SITE["contact"].get("email")
    contact = []
    if ig:
        contact.append(f'Instagram <a href="https://instagram.com/{E(ig)}" rel="noopener">@{E(ig)}</a>')
    if email:
        contact.append(f'<a href="mailto:{E(email)}">{E(email)}</a>')
    phone = SITE["contact"].get("phone")
    if phone:
        digits = "".join(ch for ch in phone if ch.isdigit())
        contact.append(f'<a href="tel:+55{digits}">{E(phone)}</a>')
    stores = ", ".join(SITE["stores"])
    nav = " ".join(([f'<a href="/">Início</a>'] + [f'<a href="/{n["key"]}">{E(n["title"])}</a>' for n in NICHES] if links else [])
                   + ([] if links else ['<a href="/">Ver outros grupos de ofertas</a>'])
                   + ['<a href="/privacidade">Política de Privacidade</a>']
                   # Só existe banner de consentimento quando o pixel está ligado (o tracking.js trata o clique)
                   + (['<button type="button" class="link-btn" data-consent-open>Preferências de privacidade</button>'] if SITE["metaPixelId"] else []))
    return f"""<footer class="site-footer"><div class="wrap">
  <nav aria-label="Rodapé">{nav}</nav>
  <p><strong>Aviso de afiliado:</strong> alguns links são de afiliado. Podemos receber comissão pelas compras, sem custo extra para você. Preços e estoque podem mudar a qualquer momento.</p>
  <p>Não temos vínculo com {E(stores)} nem com o WhatsApp. As marcas citadas pertencem aos seus donos.</p>
  {"<p>Contato: " + " · ".join(contact) + "</p>" if contact else ""}
</div></footer>
<script src="/config.js"></script>
<script src="/tracking.js"></script>
</body>
</html>
"""


def cta(key, position, label):
    return (f'<a class="cta" href="/{key}/entrar" data-cta data-niche="{key}" data-position="{position}">'
            f'{WA_ICON}<span>{E(label)}</span></a>')


def badges(items, align=""):
    out = "".join(f'<span class="badge{" hot" if "vaga" in b.lower() else (" info" if "grátis" in b.lower() else "")}">{E(b)}</span>' for b in items)
    return f'<div class="badges{align}">{out}</div>'


def faq_for(n):
    return [
        ("É grátis?", "Sim. Entrar e participar do grupo é 100% gratuito."),
        ("Quantas mensagens vou receber?", "Depende das promoções do dia. Mandamos só o que vale a pena e, se preferir, você pode silenciar o grupo e conferir quando quiser."),
        ("É seguro?", "Sim. Você entra pelo convite oficial do WhatsApp e não pedimos nenhum dado. Os links levam para as próprias lojas, onde a compra acontece normalmente. Nunca pedimos pagamento, senha ou código por mensagem."),
        ("Como sair do grupo?", "Abra o grupo no WhatsApp, toque no nome dele e escolha “Sair do grupo”. Pronto, sem complicação."),
        tuple(n["page"]["faqTopic"]),
    ]


def niche_page(n):
    p, key = n["page"], n["key"]
    faq = faq_for(n)
    schema = ld([
        {"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "url": f"{DOMAIN}/{key}",
         "inLanguage": "pt-BR", "description": p["description"],
         "isPartOf": {"@type": "WebSite", "name": SITE["siteName"], "url": DOMAIN + "/"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ])
    logo = n.get("logo") or {}
    if logo.get("hero"):
        top = f'<div class="hero-logo square"><img src="{logo["hero"]}" alt="{E(n["brand"])}" width="160" height="160"></div>'
    elif n.get("heroLogo"):
        top = LOGO
    else:
        top = f'<div class="icon" aria-hidden="true">{n["emoji"]}</div>'
    perks = "\n".join(f'      <li><span class="p-icon" aria-hidden="true">{i}</span><div><strong>{E(h)}</strong><span>{E(t)}</span></div></li>'
                      for i, h, t in p["perks"])
    proofs = n.get("proofs") or []
    proof_html = ""
    if proofs:
        total = len(proofs)
        imgs = "\n".join(
            f'      <figure class="slide"><img src="{x["src"]}" alt="{E(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async">'
            f'<figcaption>{i} de {total}</figcaption></figure>' for i, x in enumerate(proofs, 1))
        proof_html = f"""
  <section class="block">
    <h2>Ofertas reais do grupo</h2>
    <div class="proofs" tabindex="0" aria-label="Prints de ofertas postadas no grupo (deslize para o lado)">
{imgs}
    </div>
    <p class="swipe-hint" aria-hidden="true">Deslize para o lado para ver mais ofertas →</p>
    <p class="note">Prints de ofertas postadas no grupo {E(n["groupName"])}. Preços da data do post; podem ter mudado.</p>
  </section>
"""
    video = n.get("video")
    if video:
        # Vídeo mudo em loop no lugar dos prints; sem som, o navegador permite tocar sozinho.
        proof_html = f"""
  <section class="block">
    <h2>Achados reais do grupo</h2>
    <video class="proof-video" poster="{video["poster"]}" width="{video["width"]}" height="{video["height"]}"
           autoplay muted loop playsinline preload="metadata" aria-label="{E(video["label"])}">
      <source src="{video["src"]}" type="video/mp4">
      <source src="{video["src"].replace(".mp4", ".webm")}" type="video/webm">
    </video>
    <p class="note">{E(video["note"])}</p>
  </section>
"""
    faq_html = "\n".join(f"    <details class=\"faq\"><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    return (head(p["title"], p["description"], f"/{key}", p["ogDescription"], schema, logo.get("og", "/assets/img/og.jpg"))
            + header(f"/{key}", SITE.get("menuOnNichePages", True),
                     logo.get("icon", "/assets/img/icon-64.png"), logo.get("headerName", "CLUB SONAR"))
            + f"""<main class="wrap">
  <div class="hero">
    {top}
    <p class="brand-line">{E(n["brand"])} · grupo no WhatsApp</p>
    <h1>{p["h1"]}</h1>
    <p class="lead">{E(p["lead"])}</p>
    {cta(key, "hero", "Entrar no grupo grátis")}
    <p class="reassure">Grátis, sem spam, saia quando quiser.</p>
    {badges(p["badges"])}
  </div>
{proof_html}
  <section class="block">
    <h2>Como funciona</h2>
    <ol class="steps card">
      <li>Toque em “Entrar no grupo grátis”.</li>
      <li>O WhatsApp abre com o convite. Toque em “Entrar”.</li>
      <li>Pronto! As ofertas chegam direto no seu celular.</li>
    </ol>
  </section>

  <section class="block">
    <h2>O que você recebe</h2>
    <ul class="perks">
{perks}
    </ul>
  </section>

  <section class="block card center">
    <h2>{E(p["final"])}</h2>
    {cta(key, "meio", "Entrar no grupo grátis")}
    <p class="urgency">Os grupos do WhatsApp têm limite de participantes.</p>
  </section>

  <section class="block">
    <h2>Perguntas frequentes</h2>
{faq_html}
  </section>
</main>
""" + footer(n, links=SITE.get("menuOnNichePages", True)))


def home_page():
    cards = []
    for n in NICHES:
        k = n["key"]
        cards.append(f"""    <article class="group">
      <div class="group-head"><div class="group-icon" aria-hidden="true">{n["emoji"]}</div><h3><a href="/{k}">{E(n["title"])}</a></h3></div>
      <p>{E(n["description"])}</p>
      {badges(n["badges"], " left")}
      {cta(k, "home", "Entrar no grupo")}
      <a class="more" href="/{k}">Saiba mais sobre o grupo →</a>
    </article>""")
    schema = ld({"@context": "https://schema.org", "@type": "WebSite", "name": SITE["siteName"], "url": DOMAIN + "/",
                 "inLanguage": "pt-BR", "description": "Grupos de ofertas e cupons no WhatsApp."})
    return (head("Club Sonar · Grupos de Ofertas e Cupons no WhatsApp",
                 "Escolha seu grupo de ofertas no WhatsApp: promoções do dia, cupons e achados selecionados. Grátis, sem spam e com vagas limitadas.",
                 "/", "Promoções do dia e cupons direto no seu WhatsApp.", schema)
            + header("/")
            + f"""<main class="wrap">
  <div class="hero">
    {LOGO}
    <h1>As melhores ofertas do dia, <span class="hl">direto no seu WhatsApp</span></h1>
    <p class="lead">Escolha o grupo com a sua cara e entre grátis. Sem spam, saia quando quiser.</p>
  </div>

  <section class="block" aria-labelledby="grupos">
    <h2 id="grupos">Escolha seu grupo</h2>
    <div class="groups">
{chr(10).join(cards)}
    </div>
  </section>
</main>
""" + footer())


def enter_page(n):
    """Redirecionador interno: o CTA aponta para cá, nunca direto para o convite."""
    url = E(n["groupUrl"])
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Abrindo o grupo no WhatsApp…</title>
<meta http-equiv="refresh" content="{3 if SITE.get("cfAnalyticsToken") else 0}; url={url}">
<link rel="stylesheet" href="/assets/site.css">
{cf_beacon()}<script>
  // Espera o analytics carregar para a visita a /entrar contar como clique no botão; o refresh acima é o plano B.
  var go = function () {{ location.replace({json.dumps(n["groupUrl"])}); }};
  {"window.addEventListener('load', function () { setTimeout(go, 150); });" if SITE.get("cfAnalyticsToken") else "go();"}
</script>
</head>
<body>
<main class="wrap center" style="padding-top:64px">
  <h1>Abrindo o grupo {E(n["groupName"])}…</h1>
  <p class="lead">Se o WhatsApp não abrir sozinho, toque no botão abaixo.</p>
  <a class="cta" href="{url}" rel="noopener">{WA_ICON}<span>Abrir o grupo no WhatsApp</span></a>
</main>
</body>
</html>
"""


def privacy_page():
    ig = SITE["contact"].get("instagram")
    email = SITE["contact"].get("email")
    contact = (f'pelo e-mail <a href="mailto:{E(email)}">{E(email)}</a>' if email
               else f'pelo Instagram <a href="https://instagram.com/{E(ig)}" rel="noopener">@{E(ig)}</a>' if ig else "pelos nossos canais")
    return (head("Política de Privacidade · Club Sonar", "Como o Club Sonar trata dados pessoais, de acordo com a LGPD.", "/privacidade")
            + header("/privacidade")
            + f"""<main class="wrap prose">
  <h1>Política de Privacidade</h1>
  <p>Última atualização: 7 de outubro de 2026.</p>
  <p>O Club Sonar mantém este site para apresentar seus grupos gratuitos de ofertas no WhatsApp. Esta política explica, de acordo com a Lei Geral de Proteção de Dados (Lei 13.709/2018), quais dados tratamos e por quê.</p>

  <h2>1. Dados que coletamos</h2>
  <p>Não temos formulários e não pedimos nome, e-mail ou telefone. Ao visitar o site, podem ser registrados:</p>
  <ul>
    <li><strong>Parâmetros de campanha</strong> (como utm_source e fbclid) presentes no link que você abriu. Eles ficam guardados apenas no seu navegador durante a visita, para sabermos de onde veio o acesso.</li>
    <li><strong>Registros técnicos do servidor</strong> (como IP e navegador), mantidos pelo provedor de hospedagem para segurança e funcionamento do site.</li>
  </ul>
  <p><strong>Estatísticas de visita:</strong> usamos o Cloudflare Web Analytics para contar visitas e cliques de forma agregada (páginas vistas, origem e tipo de aparelho). Ele não usa cookies, não guarda dados no seu navegador e não identifica você.</p>
  <p><strong>Pixel da Meta:</strong> usamos o Pixel da Meta (Facebook e Instagram) para medir a eficácia dos nossos anúncios. Ele coleta dados de navegação, como as páginas visitadas e os cliques nos botões de entrada no grupo, e os envia à Meta, que os trata conforme a política dela. Tratamos esses dados conforme a LGPD e você pode limitar esse rastreamento nas configurações de anúncios da sua conta da Meta ou nas configurações de privacidade do seu navegador. O Pixel só é ativado se você aceitar no aviso de cookies, e você pode mudar sua escolha a qualquer momento em “Preferências de privacidade”, no rodapé do site. A Meta pode tratar esses dados fora do Brasil.</p>

  <h2>2. Grupo no WhatsApp</h2>
  <p>Ao entrar em um grupo, o WhatsApp (Meta) trata seus dados conforme a política dele. Seu número e nome de perfil ficam visíveis para os administradores e, conforme a configuração do grupo, para outros participantes. Não usamos seu número para outra finalidade e você pode sair do grupo quando quiser.</p>

  <h2>3. Links de afiliado</h2>
  <p>Ao clicar em uma oferta, você vai para o site da loja, que pode usar cookies próprios para identificar a indicação e calcular nossa comissão, sem custo extra para você. Esse tratamento segue a política de privacidade de cada loja.</p>

  <h2>4. Compartilhamento</h2>
  <p>Não vendemos nem compartilhamos dados pessoais, exceto com os provedores citados acima, que são necessários para o site e os grupos funcionarem.</p>

  <h2>5. Seus direitos</h2>
  <p>Você pode pedir acesso, correção ou exclusão de dados e tirar dúvidas sobre esta política {contact}.</p>
</main>
""" + footer())


def config_js():
    cfg = {
        "campaignTypes": SITE["campaignTypes"],
        "niches": {n["key"]: {"groupName": n["groupName"]} for n in SITE["niches"]},
        "metaPixelId": SITE["metaPixelId"],
        "ga4Id": SITE["ga4Id"],
    }
    return ("// Gerado pelo build.py a partir do site.json — não edite à mão.\n"
            "window.SONAR_CONFIG = " + json.dumps(cfg, ensure_ascii=False, indent=2) + ";\n")


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("gerado:", rel)


if __name__ == "__main__":
    write("index.html", home_page())
    write("privacidade/index.html", privacy_page())
    write("config.js", config_js())
    for n in NICHES:
        write(f"{n['key']}/index.html", niche_page(n))
        write(f"{n['key']}/entrar/index.html", enter_page(n))
