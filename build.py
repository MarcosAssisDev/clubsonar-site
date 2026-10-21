#!/usr/bin/env python3
"""Gera o site estático a partir do site.json.

Uso:  python3 build.py
Gera: index.html, <nicho>/index.html, <nicho>/entrar/index.html, privacidade/index.html, exclusao-de-dados/index.html e config.js.
Os arquivos gerados são versionados (o GitHub Pages serve o repositório como está).
Para trocar o link de um grupo (ex.: #101 → #102), edite só o groupUrl no site.json e rode o build.
"""
import hashlib
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
DOMAIN = SITE["domain"].rstrip("/")
NICHES = [n for n in SITE["niches"] if n["active"]]
# Versão dos arquivos estáticos (muda quando o CSS, o JS ou o site.json mudam): o navegador baixa a versão nova
# em vez de usar a do cache depois de cada publicação.
V = "?v=" + hashlib.sha1(b"".join(open(os.path.join(ROOT, f), "rb").read()
                                  for f in ("assets/site.css", "tracking.js", "site.json"))).hexdigest()[:8]

WA_ICON = ('<svg class="wa" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>')
E = html.escape


def cf_beacon():
    """Cloudflare Web Analytics: grátis, sem cookies. Só entra se houver token no site.json."""
    t = SITE.get("cfAnalyticsToken")
    if not t:
        return ""
    return ("<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
            f"data-cf-beacon='{json.dumps({'token': t})}'></script>\n")


def head(title, desc, path, og_desc=None, extra="", og_image="/assets/img/og.jpg", theme="t-ofertas"):
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
<meta name="theme-color" content="#120c07">
<link rel="stylesheet" href="/assets/site.css{V}">
{extra}{cf_beacon()}</head>
<body class="{theme}">
"""


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False) + "\n</script>\n"


def topline(text, link=False):
    """Faixa do topo: marca do canal em uma linha, sem menu (nas páginas de grupo a única saída é o CTA)."""
    inner = f'<a href="/">{E(text)}</a>' if link else E(text)
    return f'<p class="topline">{inner}</p>\n'


def footer(niche=None, links=True):
    ig = (niche or {}).get("instagram") or SITE["contact"].get("instagram")
    email = SITE["contact"].get("email")
    contact = []
    if ig:
        contact.append(f'Instagram <a href="https://instagram.com/{E(ig)}" rel="noopener">@{E(ig)}</a>')
    if email:
        contact.append(f'<a href="mailto:{E(email)}">{E(email)}</a>')
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
<script src="/config.js{V}"></script>
<script src="/tracking.js{V}"></script>
</body>
</html>
"""


SPIN = '<span class="spin" aria-hidden="true"></span>'


def cta(key, position, label):
    # data-loading-text: o tracking.js troca o texto e mostra o loading depois de registrar o clique (cta_click + Lead)
    return (f'<a class="cta" href="/{key}/entrar" data-cta data-niche="{key}" data-position="{position}" '
            f'data-loading-text="Abrindo o WhatsApp…">{WA_ICON}{SPIN}<span class="cta-label">{E(label)}</span></a>')


def badge_logo(n):
    """Logo central no círculo com brilho. Logo quadrado (Sonar Pet) preenche o círculo; o horizontal (Sonar Ofertas) fica dentro."""
    logo = n.get("logo") or {}
    if logo.get("hero"):
        return f'<div class="logo-ring"><div class="badge-logo"><img src="{logo["hero"]}" alt="{E(n["brand"])}" width="148" height="148" fetchpriority="high"></div></div>'
    return '<div class="logo-ring"><div class="badge-logo wide"><img src="/assets/img/logo.webp" alt="Sonar Ofertas" width="124" height="45" fetchpriority="high"></div></div>'


def niche_footer():
    """Sem rodapé nas páginas de grupo: só um link discreto para a /privacidade (LGPD), que traz o
    aviso de afiliado, o não-vínculo com as lojas, o contato e as preferências de privacidade."""
    return """<a class="priv-link" href="/privacidade">Privacidade</a>
<script src="/config.js{V}"></script>
<script src="/tracking.js{V}"></script>
</body>
</html>
""".replace("{V}", V)


def niche_page(n):
    p, key = n["page"], n["key"]
    schema = ld({"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "url": f"{DOMAIN}/{key}",
                 "inLanguage": "pt-BR", "description": p["description"],
                 "isPartOf": {"@type": "WebSite", "name": SITE["siteName"], "url": DOMAIN + "/"}})
    logo = n.get("logo") or {}
    # Página única e limpa: logo, frase, botão e selo no centro da tela; rodapé numa caixa no fim da tela.
    return (head(p["title"], p["description"], f"/{key}", p["ogDescription"], schema, logo.get("og", "/assets/img/og.jpg"), f"t-{key} single")
            + topline(p.get("topline", n["brand"]))
            + f"""<main class="wrap stage">
  {badge_logo(n)}
  <span class="glow-line" aria-hidden="true"></span>
  <h1>{p["h1"]}</h1>
  {cta(key, "hero", "Entrar no grupo grátis")}
  <p class="pill"><span class="dot" aria-hidden="true"></span>Grátis, sem spam, saia quando quiser</p>
</main>
""" + niche_footer())


def home_page():
    rows = []
    for n in NICHES:
        k = n["key"]
        icon = (n.get("logo") or {}).get("icon")
        pic = f'<img src="{icon}" alt="" width="52" height="52">' if icon else f'<img src="/assets/img/icon-192.png" alt="" width="52" height="52">'
        # A linha inteira é o botão: vai direto ao /<nicho>/entrar (conta cta_click + Lead e mostra o loading)
        rows.append(f"""  <li><a class="group" href="/{k}/entrar" data-cta data-niche="{k}" data-position="home" data-loading-text="Abrindo…">
    <span class="group-icon" aria-hidden="true">{pic}</span>
    <span class="group-text"><strong>{E(n["title"])}</strong><span>{E(n["description"])}</span></span>
    <span class="go">{WA_ICON}{SPIN}<span class="cta-label">Entrar</span></span>
  </a></li>""")
    schema = ld({"@context": "https://schema.org", "@type": "WebSite", "name": SITE["siteName"], "url": DOMAIN + "/",
                 "inLanguage": "pt-BR", "description": "Grupos de ofertas e cupons no WhatsApp."})
    return (head("Club Sonar · Grupos de Ofertas e Cupons no WhatsApp",
                 "Escolha seu grupo de ofertas no WhatsApp: promoções do dia, cupons e achados selecionados. Grátis e sem spam.",
                 "/", "Promoções do dia e cupons direto no seu WhatsApp.", schema)
            + topline("Grupos de ofertas no WhatsApp")
            + f"""<main class="wrap">
<section class="stage home">
  <div class="logo-ring"><div class="badge-logo wide"><img src="/assets/img/logo.webp" alt="Sonar Ofertas" width="124" height="45" fetchpriority="high"></div></div>
  <span class="glow-line" aria-hidden="true"></span>
  <h1>Escolha seu <span class="hl">grupo de ofertas</span></h1>
  <p class="sub">Grátis, sem spam, saia quando quiser.</p>
</section>
<ul class="groups" aria-label="Grupos">
{chr(10).join(rows)}
</ul>
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
<link rel="stylesheet" href="/assets/site.css{V}">
{cf_beacon()}<script>
  // Espera o analytics carregar para a visita a /entrar contar como clique no botão; o refresh acima é o plano B.
  var go = function () {{ location.replace({json.dumps(n["groupUrl"])}); }};
  {"window.addEventListener('load', function () { setTimeout(go, 150); });" if SITE.get("cfAnalyticsToken") else "go();"}
</script>
</head>
<body class="t-{n["key"]}">
<main class="opening">
  <span class="spin" aria-hidden="true"></span>
  <h1>Abrindo o grupo {E(n["groupName"])}…</h1>
  <p>Se o WhatsApp não abrir sozinho, toque no botão abaixo.</p>
  <a class="cta" href="{url}" rel="noopener">{WA_ICON}<span>Abrir no WhatsApp</span></a>
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
            + topline("← Club Sonar · Grupos de ofertas", link=True)
            + f"""<main class="wrap prose">
  <h1>Política de Privacidade</h1>
  <p>Última atualização: 21 de outubro de 2026.</p>

  <h2 id="avisos">Avisos</h2>
  <p><strong>Aviso de afiliado:</strong> alguns links dos nossos grupos são de afiliado. Podemos receber comissão pelas compras, sem custo extra para você. Preços e estoque podem mudar a qualquer momento.</p>
  <p>Não temos vínculo com {E(", ".join(SITE["stores"]))} nem com o WhatsApp. As marcas citadas pertencem aos seus donos.</p>
  {'<p><button type="button" class="pref-btn" data-consent-open>Preferências de privacidade</button></p>' if SITE["metaPixelId"] else ""}
  <p>O Club Sonar mantém este site para apresentar seus grupos gratuitos de ofertas no WhatsApp. Esta política explica, de acordo com a Lei Geral de Proteção de Dados (Lei 13.709/2018), quais dados tratamos e por quê.</p>

  <h2>1. Dados que coletamos</h2>
  <p>Não temos formulários e não pedimos nome, e-mail ou telefone. Ao visitar o site, podem ser registrados:</p>
  <ul>
    <li><strong>Parâmetros de campanha</strong> (como utm_source e fbclid) presentes no link que você abriu. Eles ficam guardados apenas no seu navegador durante a visita, para sabermos de onde veio o acesso.</li>
    <li><strong>Registros técnicos do servidor</strong> (como IP e navegador), mantidos pelo provedor de hospedagem para segurança e funcionamento do site.</li>
  </ul>
  <p><strong>Estatísticas de visita:</strong> usamos o Cloudflare Web Analytics para contar visitas e cliques de forma agregada (páginas vistas, origem e tipo de aparelho). Ele não usa cookies, não guarda dados no seu navegador e não identifica você.</p>
  <p><strong>Pixel da Meta:</strong> usamos o Pixel da Meta (Facebook e Instagram) para medir a eficácia dos nossos anúncios. Ele coleta dados de navegação, como as páginas visitadas e os cliques nos botões de entrada no grupo, e os envia à Meta, que os trata conforme a política dela. Tratamos esses dados conforme a LGPD e você pode limitar esse rastreamento nas configurações de anúncios da sua conta da Meta ou nas configurações de privacidade do seu navegador. O Pixel só é ativado se você aceitar no aviso de cookies, e você pode mudar sua escolha a qualquer momento em “Preferências de privacidade”, no topo desta página. A Meta pode tratar esses dados fora do Brasil.</p>

  <h2>2. Instagram: comentários e mensagens</h2>
  <p>Quando você comenta em uma publicação dos nossos perfis no Instagram (como o @sonar_pet), usamos um sistema automatizado, operado por nós, para responder ao comentário e enviar uma mensagem direta apresentando o nosso grupo de ofertas e perguntando se você quer conhecê-lo. Se você responder, enviamos o link do grupo.</p>
  <p><strong>Dados tratados:</strong> o texto do seu comentário, seu nome de usuário público e o identificador da sua conta no Instagram, o horário, a publicação comentada e o histórico das mensagens trocadas com o nosso atendimento automático.</p>
  <p><strong>Finalidade e base legal:</strong> atender o seu comentário e entregar o link do grupo que você demonstrou interesse em conhecer (execução de procedimentos preliminares a pedido do titular e legítimo interesse, na forma da LGPD). Não usamos esses dados para outra finalidade.</p>
  <p><strong>Inteligência artificial:</strong> o texto do seu comentário pode ser enviado a um provedor de inteligência artificial para redigir a resposta pública. Pedimos que a resposta não inclua dados pessoais, e uma pessoa da nossa equipe pode revisar as respostas antes da publicação.</p>
  <p><strong>Com quem compartilhamos:</strong> a Meta (dona do Instagram), que intermedeia as mensagens e trata os dados conforme a política dela, e o provedor de inteligência artificial citado acima. Não vendemos esses dados.</p>
  <p><strong>Por quanto tempo:</strong> guardamos esses registros pelo tempo necessário para operar o atendimento e a segurança do sistema, e os apagamos quando você pedir. Para deixar de receber mensagens, responda “parar” a qualquer mensagem nossa. Para pedir a exclusão, veja a página <a href="/exclusao-de-dados">Exclusão de dados</a>.</p>

  <h2>3. Grupo no WhatsApp</h2>
  <p>Ao entrar em um grupo, o WhatsApp (Meta) trata seus dados conforme a política dele. Seu número e nome de perfil ficam visíveis para os administradores e, conforme a configuração do grupo, para outros participantes. Não usamos seu número para outra finalidade e você pode sair do grupo quando quiser.</p>

  <h2>4. Links de afiliado</h2>
  <p>Ao clicar em uma oferta, você vai para o site da loja, que pode usar cookies próprios para identificar a indicação e calcular nossa comissão, sem custo extra para você. Esse tratamento segue a política de privacidade de cada loja.</p>

  <h2>5. Compartilhamento</h2>
  <p>Não vendemos nem compartilhamos dados pessoais, exceto com os provedores citados acima (hospedagem, estatísticas, Meta e o provedor de inteligência artificial), que são necessários para o site, o atendimento no Instagram e os grupos funcionarem.</p>

  <h2>6. Seus direitos</h2>
  <p>Você pode pedir acesso, correção ou exclusão de dados e tirar dúvidas sobre esta política {contact}. Passo a passo para pedir a exclusão: <a href="/exclusao-de-dados">Exclusão de dados</a>.</p>
</main>
""" + footer())


def deletion_page():
    email = SITE["contact"].get("email")
    mail = (f'<a href="mailto:{E(email)}?subject=Exclus%C3%A3o%20de%20dados">{E(email)}</a>' if email
            else "o nosso e-mail de contato")
    return (head("Exclusão de dados · Club Sonar",
                 "Como pedir a exclusão dos seus dados tratados pelo Club Sonar, incluindo comentários e mensagens no Instagram.",
                 "/exclusao-de-dados")
            + topline("← Club Sonar · Grupos de ofertas", link=True)
            + f"""<main class="wrap prose">
  <h1>Exclusão de dados</h1>
  <p>Última atualização: 21 de outubro de 2026.</p>
  <p>Se você comentou em uma publicação dos nossos perfis no Instagram (como o @sonar_pet) ou conversou com o nosso atendimento automático, e quer que apaguemos os seus dados, siga os passos abaixo.</p>

  <h2>Como pedir</h2>
  <ol>
    <li>Envie um e-mail para {mail} com o assunto “Exclusão de dados”, informando o seu nome de usuário no Instagram (o @). Se tiver, inclua o link do comentário.</li>
    <li>Para evitar que outra pessoa apague os seus dados, podemos pedir que você confirme o pedido por mensagem direta, a partir da própria conta do Instagram.</li>
    <li>Apagamos os registros (comentários, nome de usuário, identificador da conta e histórico de mensagens do atendimento) em até 15 dias e respondemos confirmando.</li>
  </ol>

  <h2>Deixar de receber mensagens</h2>
  <p>Responda “parar” a qualquer mensagem nossa no Instagram e não enviaremos mais nada.</p>

  <h2>Dados que ficam com a Meta</h2>
  <p>Comentários e mensagens também ficam guardados pela Meta, dona do Instagram e do WhatsApp. Para apagá-los lá, use as configurações da sua conta ou a política de privacidade da Meta.</p>

  <p>Mais detalhes sobre como tratamos dados estão na <a href="/privacidade">Política de Privacidade</a>.</p>
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
    write("exclusao-de-dados/index.html", deletion_page())
    write("config.js", config_js())
    for n in NICHES:
        write(f"{n['key']}/index.html", niche_page(n))
        write(f"{n['key']}/entrar/index.html", enter_page(n))
