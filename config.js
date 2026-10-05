// Configuração central da Page Ponte — sem segredos aqui (repositório público).
window.SONAR_CONFIG = {
  campaignTypes: {
    GROUP_ACQUISITION: { enabled: true },
    PRODUCT_PROMOTION: { enabled: false } // bloqueado nesta fase
  },
  // Cada nicho vira uma página (/<chave>) e um card na home, na ordem abaixo.
  // Para tirar um grupo da home sem apagar, use active: false.
  niches: {
    ofertas: {
      active: true,
      groupName: "Sonar Ofertas",
      groupUrl: "https://chat.whatsapp.com/CEigO4SLme22yDmi2NaxD6",
      path: "/ofertas",
      emoji: "🔥",
      title: "Ofertas Gerais",
      description: "As melhores promoções do dia em eletrônicos, casa, moda, beleza e mais.",
      badges: ["⏳ Vagas limitadas", "🎟️ Cupons exclusivos"]
    },
    pet: {
      active: true,
      groupName: "Sonar Pet #101",
      // Link oficial do grupo. Se o grupo mudar, troque so esta linha.
      groupUrl: "https://chat.whatsapp.com/EWmhSfdhhT06imZ0Y5zDYD",
      path: "/pet",
      emoji: "🐾",
      title: "Ofertas Pet",
      description: "Ração, petiscos, brinquedos e acessórios com desconto para quem cuida de pets.",
      badges: ["⏳ Vagas limitadas", "🦴 Achados do dia"]
    }
  },
  // Opcionais — preencher quando existirem. IDs de pixel/GA são públicos por natureza.
  metaPixelId: "",
  ga4Id: ""
};
