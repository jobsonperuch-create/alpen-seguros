#!/usr/bin/env python3
"""
Gera as páginas estáticas do site da Alpen Seguros.

Uso (na raiz do repositório):
    python3 _build/gerar.py

O conteúdo de cada página está nos dicionários abaixo (PAGINAS e HOME).
Edite o texto aqui e rode o script de novo: ele reescreve index.html,
as pastas de cada seguro e o sitemap.xml. A pasta _build/ não é publicada
pelo GitHub Pages (o Jekyll ignora pastas que começam com "_").

Fotos: coloque arquivos em img/fotos/<slug>.jpg (ex.: img/fotos/seguro-auto.jpg).
Enquanto a foto não existir, o site mostra o ícone do seguro no lugar.
Foto da equipe: img/equipe/jobson.jpg (sem ela, aparecem as iniciais).
"""
import json
import os
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://alpenseguros.com.br"
WA = "5527999857302"
FONE_FMT = "(27) 99985-7302"
HOJE = date.today().isoformat()


def versao(rel):
    """Hash curto do arquivo: muda a URL quando o conteúdo muda (evita cache antigo)."""
    import hashlib
    with open(os.path.join(RAIZ, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


# ---------------------------------------------------------------- ícones
ICONES = {
    "car": '<path d="M5 17h14M3 13l2-5.5A2 2 0 0 1 6.9 6h10.2a2 2 0 0 1 1.9 1.5L21 13v4h-2.5M5.5 17H3v-4h18"/><circle cx="7.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "life": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>',
    "biz": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 12h18"/>',
    "health": '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/>',
    "dental": '<path d="M7 3.5c-2.5 0-4 2-4 4.5 0 3 1.5 4.5 2 7 .5 3 1 5.5 2.5 5.5S9.5 17 10 15c.4-1.4 1-2 2-2s1.6.6 2 2c.5 2 1 5.5 2.5 5.5S18.5 18 19 15c.5-2.5 2-4 2-7 0-2.5-1.5-4.5-4-4.5-2 0-3 1-5 1s-3-1-5-1Z"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2 2M15 8l2 2"/>',
    "pro": '<rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="9" cy="12" r="2.2"/><path d="M5.5 17.5c.6-1.6 2-2.5 3.5-2.5s2.9.9 3.5 2.5M15 11h3M15 14h3M9 6V4h6v2"/>',
    "water": '<path d="M12 3s-5 5.6-5 9.2A5 5 0 0 0 12 17a5 5 0 0 0 5-4.8C17 8.6 12 3 12 3Z"/><path d="M3 20c1.5 0 1.5-1 3-1s1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1"/>',
    "next": '<path d="m9 6 6 6-6 6"/>',
    "shield": '<path d="M12 3 5 6v5c0 4.4 3 8.3 7 10 4-1.7 7-5.6 7-10V6Z"/><path d="M12 8v4M12 15.5v.5"/>',
    "refresh": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8M4 4v4h4M4 13a8 8 0 0 0 14.3 4.9L20 16M20 20v-4h-4"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2Z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4Z"/><path d="M8 9.5h8M8 12.5h5"/>',
}
WA_PATH = '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.6-.3Z"/>'


def ic(nome, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONES[nome]}</svg>'


# ---------------------------------------------------------------- conteúdo
# Ordem = ordem dos cards na home, dos chips do formulário e dos links do rodapé.
PAGINAS = [
    {
        "slug": "seguro-auto", "nome": "Seguro Auto", "icone": "car", "chip": "Carro",
        "curto": "Colisão, roubo, alagamento e assistência 24h.",
        "title": "Seguro Auto em Vila Velha e Vitória (ES) | Alpen Seguros",
        "desc": "Cotação de seguro de automóvel em Vila Velha, Vitória e Serra. Colisão, roubo, alagamento e assistência 24h. Proposta pelo WhatsApp em até 2 horas.",
        "h1": "Seguro auto em Vila Velha e Vitória",
        "lead": "Seguro de automóvel com cobertura para colisão, roubo, alagamento e danos a terceiros, mais guincho e carro reserva. Para carro próprio ou financiado, em toda a Grande Vitória.",
        "destaques": ["Assistência 24h: guincho, chaveiro e pane seca", "Carro reserva enquanto o seu está na oficina", "Proposta em até 2 horas pelo WhatsApp"],
        "foto_alt": "Carro estacionado em rua de Vila Velha",
        "cobre_titulo": "O que o seguro auto cobre",
        "cobre": ["Colisão, roubo, furto e incêndio", "Alagamento e inundação, na cobertura compreensiva", "Danos a terceiros: carro, moto e pedestre", "Guincho, chaveiro, pane seca, troca de pneu e vidros", "Carro reserva enquanto o seu está na oficina", "Cobertura em todo o Brasil"],
        "dado": {"titulo": "980 vítimas no trânsito do ES em 2024", "texto": "Mais de duas por dia. E cerca de 70% dos veículos circulam sem seguro, pela estimativa da CNseg.", "fonte": "Fontes: Detran-ES e CNseg"},
        "casos_titulo": "Quando o seguro auto faz diferença",
        "casos": [
            ("Bateu em outro carro", "Sem seguro, o conserto sai do seu bolso: de R$ 3 mil a R$ 8 mil num carro popular, e muito mais num carro de luxo."),
            ("Carro financiado e roubado", "O banco continua cobrando as parcelas. Com seguro, a indenização quita o financiamento."),
            ("Rua alagou com o carro estacionado", "Com a cobertura compreensiva, a perda por alagamento é indenizada. Sem ela, o prejuízo é todo seu."),
            ("Pane na estrada às 22h", "Guincho, chaveiro, pane seca e troca de pneu a qualquer hora. Você não fica sozinho na estrada."),
        ],
        "faq": [
            ("Quanto custa o seguro auto em Vila Velha?", "Depende do perfil de quem dirige, do modelo do carro, do CEP e do histórico de sinistros. Mande o modelo e o ano pelo WhatsApp e você recebe o valor exato em até 2 horas."),
            ("O seguro auto cobre carro financiado?", "Sim. Em caso de perda total ou roubo, a indenização pode quitar o saldo do financiamento com o banco."),
            ("O seguro auto cobre alagamento?", "Sim, quando a apólice tem cobertura compreensiva, que é a mais contratada. Ela cobre perda parcial ou total por alagamento e inundação."),
            ("Vocês atendem em outras cidades além de Vila Velha?", "Sim. Atendemos toda a Grande Vitória (Vila Velha, Vitória, Serra, Cariacica, Viana) e o restante do Espírito Santo."),
        ],
        "relacionados": ["seguro-alagamento", "consorcio", "seguro-residencial", "seguro-de-vida"],
    },
    {
        "slug": "seguro-residencial", "nome": "Seguro Residencial", "icone": "home", "chip": "Casa",
        "curto": "Casa ou apartamento, próprio ou alugado.",
        "title": "Seguro Residencial em Vila Velha e Vitória | Alpen Seguros",
        "desc": "Seguro para casa e apartamento, próprio ou alugado, em Vila Velha e Vitória. Incêndio, roubo, danos elétricos e assistência 24h, a partir de menos de R$ 50/mês.",
        "h1": "Seguro residencial para casa e apartamento",
        "lead": "Proteção para sua residência contra incêndio, roubo, danos elétricos e vendaval, com encanador, eletricista e chaveiro 24h. Vale para imóvel próprio ou alugado.",
        "destaques": ["A partir de menos de R$ 50 por mês", "Casa ou apartamento, próprio ou alugado", "Assistência 24h para emergências"],
        "foto_alt": "Sala de estar de um apartamento",
        "cobre_titulo": "O que o seguro residencial cobre",
        "cobre": ["Incêndio, explosão e queda de raio", "Roubo e furto qualificado de bens", "Danos elétricos em eletrodomésticos", "Vendaval, granizo e impacto de veículos", "Alagamento, como cobertura adicional", "Responsabilidade civil: dano causado ao vizinho", "Encanador, eletricista e chaveiro 24h"],
        "dado": {"titulo": "663 casas pegaram fogo no ES em um ano", "texto": "Foram 1.662 incêndios em imóveis entre abril de 2024 e abril de 2025. A causa mais comum é falha elétrica: fiação antiga, aparelho travado, ferro esquecido.", "fonte": "Fonte: Corpo de Bombeiros Militar do ES (CBMES)"},
        "casos_titulo": "Quando o seguro residencial faz diferença",
        "casos": [
            ("Curto queimou a geladeira", "Danos elétricos são o sinistro residencial mais comum. Uma geladeira nova custa de R$ 3 mil a R$ 8 mil, e o seguro cobre."),
            ("Cano estourou no fim de semana", "Você chama um encanador credenciado a qualquer hora, sem pagar plantão de emergência."),
            ("Casa arrombada durante a viagem", "TV, notebook e outros bens roubados com arrombamento são indenizados."),
            ("Apartamento com seguro do condomínio", "O seguro do prédio não cobre o que está dentro da sua unidade. Móveis e eletrônicos precisam de seguro próprio."),
        ],
        "faq": [
            ("O seguro residencial cobre imóvel alugado?", "Sim. Inquilino e proprietário podem contratar. Basta informar na cotação para ajustarmos a cobertura."),
            ("Apartamento precisa de seguro residencial?", "Sim. O seguro do condomínio não cobre seus bens dentro da unidade, como móveis, eletrônicos e objetos de valor."),
            ("O seguro residencial cobre alagamento?", "Pode cobrir, como cobertura adicional. Nem todo plano inclui, por isso peça na cotação, principalmente se você mora em área que alaga."),
            ("Quanto custa o seguro residencial em Vila Velha?", "Depende do valor do imóvel e dos bens. Os planos básicos começam abaixo de R$ 50 por mês."),
        ],
        "relacionados": ["seguro-alagamento", "seguro-auto", "consorcio", "seguro-de-vida"],
    },
    {
        "slug": "seguro-de-vida", "nome": "Seguro de Vida", "icone": "life", "chip": "Vida",
        "curto": "Renda para a família, com opção de resgate.",
        "title": "Seguro de Vida em Vila Velha e Vitória | Alpen Seguros",
        "desc": "Seguro de vida com resgate para você, sua família e sua empresa. Morte, invalidez e doenças graves, fora do inventário e isento de IR. Vila Velha e Vitória.",
        "h1": "Seguro de vida com resgate",
        "lead": "Proteção para a sua família hoje, que também pode devolver parte do valor pago se você nunca precisar usar. Para pessoa física, autônomos, MEI e empresas.",
        "destaques": ["Morte, invalidez e doenças graves", "Fora do inventário e isento de Imposto de Renda", "Opção com resgate do valor investido"],
        "foto_alt": "Família reunida em casa",
        "cobre_titulo": "O que o seguro de vida cobre",
        "cobre": ["Morte natural ou acidental", "Invalidez e incapacidade para trabalhar", "Diagnóstico de doenças graves, em vida", "Assistência funeral", "Resgate do valor investido, no Viva Mais Resgatável", "Proteção entre sócios e sucessão na empresa"],
        "dado": {"titulo": "Inventário pode levar anos", "texto": "Imóveis, investimentos e cotas de empresa ficam bloqueados até a partilha, e ITCMD e custos levam parte do patrimônio. O seguro de vida chega à família em dias, fora do inventário.", "fonte": ""},
        "casos_titulo": "Quando o seguro de vida faz diferença",
        "casos": [
            ("Se eu faltar, minha família mantém a casa?", "Financiamento, escola, mercado e contas continuam. O seguro garante renda enquanto a família se reorganiza."),
            ("Autônomo sem CLT", "Sem auxílio-doença nem FGTS, a renda para junto com você. A cobertura de invalidez é a sua rede de proteção."),
            ("E se um sócio morrer?", "Herdeiros podem exigir a parte deles de imediato. O seguro entre sócios garante dinheiro para a empresa continuar."),
            ("Planejamento sucessório", "O valor vai direto aos beneficiários, sem esperar o inventário e sem Imposto de Renda."),
        ],
        "faq": [
            ("Como funciona o seguro de vida com resgate?", "No Bradesco Viva Mais Resgatável, se você não usar o seguro, pode resgatar parte do valor investido. Funciona como proteção e como reserva financeira."),
            ("MEI e autônomo precisam de seguro de vida?", "Sim, talvez mais do que quem tem carteira assinada. Sem FGTS e sem auxílio-doença garantido, a cobertura de invalidez é a principal proteção de renda."),
            ("Seguro de vida ajuda no planejamento sucessório?", "Sim. O valor pago aos beneficiários não entra em inventário e é isento de Imposto de Renda."),
        ],
        "relacionados": ["seguro-para-profissionais", "plano-de-saude-empresarial", "consorcio", "seguro-residencial"],
    },
    {
        "slug": "consorcio", "nome": "Consórcio", "icone": "key", "chip": "Consórcio",
        "curto": "Imóvel ou automóvel sem juros de financiamento.",
        "title": "Consórcio de Imóvel e Automóvel no ES | Alpen Seguros",
        "desc": "Consórcio para comprar casa, apartamento ou carro sem juros de financiamento. Entenda lance, sorteio e carta de crédito. Atendimento em Vila Velha e Vitória.",
        "h1": "Consórcio de imóvel e automóvel",
        "lead": "Para quem quer comprar casa, apartamento ou carro sem pagar juros de financiamento. Você paga parcelas mensais e recebe a carta de crédito por sorteio ou lance.",
        "destaques": ["Sem juros, só taxa de administração", "Carta de crédito para imóvel ou veículo", "Simulação de parcela pelo WhatsApp"],
        "foto_alt": "Chaves de um imóvel novo",
        "cobre_titulo": "Como o consórcio funciona",
        "cobre": ["Você escolhe o valor da carta de crédito e o prazo", "Paga parcelas mensais sem juros, com taxa de administração", "Todo mês há sorteio e lance para contemplação", "Contemplado, você compra o bem à vista com a carta", "No consórcio de imóvel, o FGTS pode ser usado, conforme as regras do fundo", "Serve também para trocar de carro ou comprar imóvel para alugar"],
        "dado": {"titulo": "Consórcio ou financiamento?", "texto": "No financiamento você recebe o bem na hora e paga juros. No consórcio não há juros, mas você recebe quando é contemplado. Para quem pode planejar, o custo total costuma ser menor.", "fonte": ""},
        "casos_titulo": "Para quem o consórcio faz sentido",
        "casos": [
            ("Primeiro imóvel sem juros", "Você planeja a compra e paga parcelas menores do que as de um financiamento do mesmo valor."),
            ("Trocar de carro em 2 ou 3 anos", "Com o lance, dá para antecipar a contemplação e chegar à troca no prazo que você quer."),
            ("Imóvel para alugar", "Quem já tem casa usa o consórcio para formar patrimônio e renda de aluguel."),
            ("Frota e equipamentos da empresa", "Empresas usam o consórcio para renovar veículos e máquinas sem comprometer o caixa com juros."),
        ],
        "faq": [
            ("Consórcio ou financiamento: qual compensa mais?", "Se você precisa do bem agora, o financiamento resolve, mas com juros. Se pode esperar a contemplação, o consórcio costuma sair mais barato no total."),
            ("Como funciona o lance no consórcio?", "Lance é um valor que você oferece adiantado para ser contemplado antes. Todo mês, além dos sorteados, é contemplado quem oferece o maior lance."),
            ("Posso usar o FGTS no consórcio de imóvel?", "Sim, para dar lance, amortizar ou completar a carta, desde que você cumpra as regras do FGTS para compra de imóvel residencial."),
        ],
        "relacionados": ["seguro-residencial", "seguro-auto", "seguro-de-vida", "seguro-empresarial"],
    },
    {
        "slug": "seguro-empresarial", "nome": "Seguro Empresarial", "icone": "biz", "chip": "Empresa",
        "curto": "Estoque, equipamentos e responsabilidade civil.",
        "title": "Seguro Empresarial em Vitória e Vila Velha | Alpen Seguros",
        "desc": "Seguro empresarial para pequenas e médias empresas na Grande Vitória: incêndio, roubo, danos elétricos, responsabilidade civil e lucros cessantes.",
        "h1": "Seguro empresarial para pequenas e médias empresas",
        "lead": "Proteja estoque, equipamentos e o faturamento do seu negócio. Para lojas, escritórios, consultórios, restaurantes e indústrias na Grande Vitória.",
        "destaques": ["Incêndio, roubo e danos elétricos", "Responsabilidade civil com clientes", "Lucros cessantes durante a reconstrução"],
        "foto_alt": "Pequeno comércio com a dona no balcão",
        "cobre_titulo": "O que o seguro empresarial cobre",
        "cobre": ["Incêndio, explosão e queda de raio no estabelecimento", "Roubo de estoque, equipamentos e caixa", "Danos elétricos em máquinas e equipamentos", "Responsabilidade civil: cliente que se machuca no local", "Lucros cessantes: renda enquanto a empresa está parada", "Eletricista, encanador, chaveiro e vidraceiro 24h"],
        "dado": {"titulo": "345 empresas pegaram fogo no ES em um ano", "texto": "De 1.662 incêndios em imóveis registrados entre 2024 e 2025, 345 foram em estabelecimentos comerciais. A principal causa foi falha elétrica.", "fonte": "Fonte: Corpo de Bombeiros Militar do ES (CBMES)"},
        "casos_titulo": "Quando o seguro empresarial faz diferença",
        "casos": [
            ("Incêndio destruiu o estoque", "O seguro repõe estoque e equipamentos e paga renda enquanto você reconstrói."),
            ("Cliente caiu na loja e processou", "A responsabilidade civil cobre a defesa e a indenização."),
            ("Computadores roubados no fim de semana", "Você repõe os equipamentos e a operação volta em dias, não em meses."),
            ("Curto queimou três máquinas", "A cobertura de danos elétricos repõe os equipamentos danificados."),
        ],
        "faq": [
            ("Seguro empresarial serve para pequenas empresas?", "Sim, e é para elas que ele faz mais diferença: um sinistro grave pode fechar um negócio pequeno."),
            ("O que é lucros cessantes?", "É a cobertura que paga uma renda para a empresa enquanto ela está parada se recuperando de um sinistro, além do prejuízo material."),
            ("Como fazer a cotação do seguro empresarial?", "Preencha o formulário desta página e informe pelo WhatsApp a razão social, o CNPJ e o CEP. A cotação é gratuita."),
        ],
        "relacionados": ["seguro-para-profissionais", "plano-de-saude-empresarial", "plano-dental", "seguro-de-vida"],
    },
    {
        "slug": "plano-de-saude-empresarial", "nome": "Plano de Saúde Empresarial", "icone": "health", "chip": "Saúde PJ",
        "curto": "Bradesco Saúde a partir de 3 vidas.",
        "title": "Plano de Saúde Empresarial em Vitória (ES) | Alpen Seguros",
        "desc": "Plano de saúde empresarial Bradesco a partir de 3 vidas, com reembolso e rede nacional. Para empresas, consultórios e escritórios em Vila Velha e Vitória.",
        "h1": "Plano de saúde empresarial a partir de 3 vidas",
        "lead": "Bradesco Saúde pelo CNPJ da sua empresa, com reembolso para médico fora da rede e cobertura em todo o Brasil. Costuma custar menos que o plano individual.",
        "destaques": ["A partir de 3 vidas, entre sócios e funcionários", "Reembolso com prévia antes do procedimento", "Rede referenciada no ES e em todo o Brasil"],
        "foto_alt": "Médica conversando com paciente em consultório",
        "cobre_titulo": "O que o plano de saúde empresarial oferece",
        "cobre": ["Consultas e exames direto na rede, sem autorização prévia na maioria dos casos", "Reembolso para médico fora da rede, com prévia do valor", "Internação, cirurgia e UTI", "Tratamento oncológico, quimioterapia e radioterapia", "Cobertura em todo o Brasil", "Programas de saúde preventiva para a equipe"],
        "dado": {"titulo": "Plano empresarial costuma custar menos", "texto": "Como o risco é dividido entre o grupo, a mensalidade por pessoa tende a ser menor que a do plano individual.", "fonte": ""},
        "casos_titulo": "Quando o plano empresarial faz diferença",
        "casos": [
            ("Cirurgia urgente", "Na rede referenciada, a maioria dos procedimentos é feita sem esperar dias por autorização."),
            ("Seu médico não é credenciado", "Você consulta com quem quiser e pede reembolso. A prévia mostra o valor antes."),
            ("Tratamento de alta complexidade", "Oncologia, UTI e procedimentos complexos cobertos, em qualquer estado."),
            ("Reter a equipe", "Plano de saúde é um dos benefícios que mais pesam na decisão de ficar na empresa."),
        ],
        "faq": [
            ("Qual o mínimo de vidas para o plano de saúde empresarial?", "A partir de 3 vidas, entre sócios e funcionários com vínculo comprovado."),
            ("Posso usar médico fora da rede credenciada?", "Sim. Na modalidade de livre escolha, você consulta com qualquer médico e pede reembolso, com prévia do valor antes do procedimento."),
            ("Plano de saúde empresarial é mais barato que o individual?", "Geralmente sim, porque o risco é dividido entre o grupo."),
        ],
        "relacionados": ["plano-dental", "seguro-empresarial", "seguro-para-profissionais", "seguro-de-vida"],
    },
    {
        "slug": "plano-dental", "nome": "Plano Dental", "icone": "dental", "chip": "Dental",
        "curto": "Canal, prótese e aparelho cobertos.",
        "title": "Plano Dental em Vila Velha e Vitória | Alpen Seguros",
        "desc": "Plano odontológico Bradesco para pessoa física e empresas em Vila Velha e Vitória. Canal, prótese e ortodontia cobertos, com 27 mil dentistas credenciados.",
        "h1": "Plano dental para você e para sua empresa",
        "lead": "Canal, restauração, prótese e aparelho pagos na mensalidade, sem susto no consultório. Pessoa física ou empresarial a partir de 3 vidas.",
        "destaques": ["Urgência liberada 24h após o 1º pagamento", "Ortodontia no plano Premium Top", "Empresarial sem reajuste por faixa etária"],
        "foto_alt": "Dentista atendendo paciente",
        "cobre_titulo": "O que o plano dental cobre",
        "cobre": ["Tratamento de canal e restaurações", "Próteses, nos planos completos", "Ortodontia (aparelho), no plano Premium Top", "Urgência 24h após o primeiro pagamento", "27 mil dentistas credenciados no Brasil", "Empresarial sem reajuste por faixa etária"],
        "dado": {"titulo": "Aparelho por R$ 1.725 nos 2 primeiros anos", "texto": "No particular, o mesmo período de tratamento custa cerca de R$ 4.020. A economia passa de R$ 2.200 só no começo.", "fonte": ""},
        "casos_titulo": "Quando o plano dental faz diferença",
        "casos": [
            ("Conta de R$ 3 mil no dentista", "Canal, restauração e retorno entram na mensalidade."),
            ("Gengiva sangrando", "Doença periodontal é comum e precisa de tratamento contínuo, que o plano cobre."),
            ("Benefício para a equipe", "Plano dental é um dos benefícios com melhor custo para a empresa."),
            ("Aparelho para os filhos", "A ortodontia sai por menos da metade do valor particular."),
        ],
        "faq": [
            ("Qual o mínimo de vidas para o plano dental empresarial?", "A partir de 3 vidas, entre sócios e funcionários, sem reajuste por faixa etária."),
            ("O plano dental cobre ortodontia?", "Sim, no plano Premium Top. A ortodontia custa cerca de R$ 1.725 nos 2 primeiros anos."),
            ("Quanto tempo até poder usar o plano dental?", "A urgência é liberada 24h após o primeiro pagamento. Os demais procedimentos seguem a tabela de carências."),
        ],
        "relacionados": ["plano-de-saude-empresarial", "seguro-empresarial", "seguro-de-vida", "seguro-para-profissionais"],
    },
    {
        "slug": "seguro-para-profissionais", "nome": "Advogados, médicos e contadores", "icone": "pro", "chip": "Profissional",
        "valor_chip": "Seguro para Profissional Liberal",
        "curto": "Responsabilidade civil profissional, vida e saúde.",
        "title": "Seguro para Advogado, Médico e Contador no ES | Alpen Seguros",
        "desc": "Seguros para advogados, médicos e contadores em Vila Velha e Vitória: responsabilidade civil profissional, vida e invalidez, escritório e plano de saúde.",
        "h1": "Seguros para advogados, médicos e contadores",
        "lead": "Profissional liberal responde pelo próprio trabalho e não tem CLT. Montamos a proteção certa: responsabilidade civil profissional, seguro de vida com renda e plano de saúde pelo CNPJ.",
        "destaques": ["Responsabilidade civil profissional (RC)", "Vida e invalidez para quem não tem CLT", "Escritório, consultório e plano de saúde PJ"],
        "foto_alt": "Profissional em reunião com cliente no escritório",
        "perfis": [
            ("Seguro para advogados", "Um prazo perdido ou uma orientação errada pode virar processo do próprio cliente.",
             ["Responsabilidade civil profissional", "Seguro de vida com cobertura de invalidez", "Seguro empresarial para o escritório", "Plano de saúde e dental pelo CNPJ"]),
            ("Seguro para médicos", "Processo por erro médico custa caro mesmo quando o médico tem razão. E sem atender, a renda para.",
             ["Responsabilidade civil profissional médica", "Seguro de vida com diária por incapacidade", "Seguro do consultório e dos equipamentos", "Plano de saúde empresarial"]),
            ("Seguro para contadores", "Um erro em guia, declaração ou prazo fiscal gera multa ao cliente, e a cobrança volta para o escritório.",
             ["Responsabilidade civil profissional", "Seguro do escritório: incêndio, roubo e danos elétricos", "Seguro de vida e invalidez", "Plano dental para a equipe"]),
        ],
        "perfis_nota": "Também atendemos dentistas, engenheiros, arquitetos, psicólogos e outros profissionais liberais.",
        "faq": [
            ("O que é seguro de responsabilidade civil profissional?", "É o seguro que paga a defesa e as indenizações quando um cliente processa você por erro ou omissão no trabalho. Vale para advogados, médicos, contadores, dentistas, engenheiros e outros profissionais."),
            ("Médico que trabalha em hospital precisa de seguro próprio?", "Em geral, sim. O seguro do hospital protege o hospital, e o processo pode ser movido contra o médico pessoalmente. Um seguro de RC profissional em seu nome cobre a sua defesa."),
            ("Posso contratar plano de saúde pelo CNPJ do escritório ou consultório?", "Sim. O plano de saúde empresarial Bradesco aceita a partir de 3 vidas, entre sócios e funcionários, e costuma custar menos que o individual."),
        ],
        "relacionados": ["seguro-de-vida", "seguro-empresarial", "plano-de-saude-empresarial", "plano-dental"],
    },
]

# Página temática (não aparece como card nem chip; ligada pela faixa da home e pelas páginas de auto e residencial)
ALAGAMENTO = {
    "slug": "seguro-alagamento", "nome": "Seguro contra alagamento", "icone": "water", "chip_padrao": "seguro-auto",
    "title": "Seguro contra Alagamento em Vila Velha (ES) | Alpen Seguros",
    "desc": "Carro alagado ou casa invadida pela água? Veja o que o seguro auto e o residencial cobrem em caso de alagamento e enchente em Vila Velha e Vitória.",
    "h1": "Seguro contra alagamento em Vila Velha",
    "lead": "Chuva forte alaga ruas e garagens em Vila Velha e na Grande Vitória. Veja o que o seguro do carro e o da casa cobrem, e o que conferir antes de contratar.",
    "destaques": ["Carro alagado: cobertura compreensiva", "Casa: cobertura adicional de alagamento", "Ajuda no sinistro pelo WhatsApp"],
    "foto_alt": "Rua alagada depois de chuva forte",
    "cobre_titulo": "O que conferir na apólice",
    "cobre": ["Seguro auto com cobertura compreensiva, que inclui alagamento e inundação", "Assistência 24h com guincho para tirar o carro da água", "Seguro residencial com cobertura adicional de alagamento", "Danos elétricos, para aparelhos queimados por curto", "Valor de indenização compatível com seus bens", "Franquia e carência, para não ter surpresa na hora de usar"],
    "dado": {"titulo": "Entrar na água de propósito pode anular a cobertura", "texto": "Se o motorista avança por uma rua alagada e o motor puxa água (calço hidráulico), muitas seguradoras negam o pagamento. Na dúvida, não entre: estacione em local alto e chame a assistência.", "fonte": ""},
    "casos_titulo": "Situações que mais acontecem",
    "casos": [
        ("Carro estacionado ficou submerso", "Com a cobertura compreensiva, o reparo ou a perda total é indenizada."),
        ("Água entrou em casa", "Móveis e eletrodomésticos danificados são cobertos quando a apólice inclui alagamento."),
        ("Garagem do prédio alagou à noite", "Vale o seguro de cada carro. O seguro do condomínio não cobre os veículos dos moradores."),
        ("Curto depois da chuva", "A cobertura de danos elétricos repõe geladeira, TV e outros aparelhos queimados."),
    ],
    "faq": [
        ("Seguro auto cobre carro alagado?", "Sim, quando a apólice tem cobertura compreensiva, que é a mais contratada. Ela cobre perda parcial ou total por alagamento e inundação."),
        ("O que é calço hidráulico e o seguro cobre?", "É quando entra água no motor e ele trava. Se aconteceu porque o motorista entrou numa rua alagada, a seguradora pode negar. Com o carro parado e atingido pela água, a cobertura costuma valer."),
        ("Seguro residencial cobre enchente?", "Nem sempre. Alagamento e inundação costumam ser coberturas adicionais no seguro residencial. Peça para incluir na cotação se você mora em área que alaga."),
    ],
    "relacionados": ["seguro-auto", "seguro-residencial", "seguro-de-vida", "consorcio"],
}

HOME_FAQ = [
    ("Quanto custa um seguro auto em Vila Velha?", "Depende do carro, do CEP e do perfil de quem dirige. Mande o modelo e o ano pelo WhatsApp e você recebe o valor exato em até 2 horas."),
    ("Preciso ser cliente do banco Bradesco?", "Não. Qualquer pessoa ou empresa pode contratar. Correntistas Bradesco podem ter condições especiais."),
    ("O seguro cobre alagamento?", "No carro, sim, na cobertura compreensiva. Na casa, alagamento costuma ser cobertura adicional. Veja os detalhes na página de seguro contra alagamento."),
    ("Como aciono o seguro se acontecer algo?", "Chame a Alpen no WhatsApp. A gente orienta o que fazer na hora, abre o aviso de sinistro com a seguradora e acompanha até a indenização."),
    ("Vocês atendem fora de Vila Velha e Vitória?", "Sim. Atendemos todo o Espírito Santo, e a maior parte do processo é feita pelo WhatsApp."),
    ("O seguro de vida tem resgate?", "Sim, no Bradesco Viva Mais Resgatável. Se você não usar o seguro, pode resgatar parte do valor pago. O dinheiro vai direto aos beneficiários, sem inventário e sem Imposto de Renda."),
]
# Respostas da home que ganham link no texto visível (o schema usa o texto puro)
HOME_FAQ_LINKS = {"O seguro cobre alagamento?": ("página de seguro contra alagamento", "/seguro-alagamento/")}

POR_SLUG = {p["slug"]: p for p in PAGINAS + [ALAGAMENTO]}

# Cards da home: (segmentos para as abas, selo sobre a foto)
CARDS = {
    "seguro-auto": ("casa", "Assistência 24h"),
    "seguro-residencial": ("casa", "Menos de R$ 50/mês"),
    "seguro-de-vida": ("familia", "Com resgate"),
    "consorcio": ("casa familia", "Sem juros"),
    "seguro-empresarial": ("empresa", "Para PMEs"),
    "plano-de-saude-empresarial": ("empresa familia", "A partir de 3 vidas"),
    "plano-dental": ("familia empresa", "Urgência em 24h"),
    "seguro-para-profissionais": ("empresa", "RC profissional"),
}
ABAS = [("todos", "Todos"), ("casa", "Carro e casa"), ("familia", "Família e futuro"), ("empresa", "Empresa e profissão")]

# Atalhos para quem já é cliente: abrem o WhatsApp com a mensagem pronta
ATALHOS = [
    ("shield", "Acionar o seguro", "Bateu o carro, foi roubado ou algo aconteceu em casa? Abrimos o sinistro com você.", "Olá! Sou cliente da Alpen e preciso acionar meu seguro."),
    ("refresh", "Renovar ou alterar", "Trocou de carro, de endereço ou quer revisar a cobertura.", "Olá! Sou cliente da Alpen e quero renovar ou alterar meu seguro."),
    ("receipt", "Boleto e pagamento", "Segunda via, data de vencimento ou forma de pagamento.", "Olá! Sou cliente da Alpen e preciso de ajuda com boleto ou pagamento."),
    ("chat", "Falar com o corretor", "Qualquer outra dúvida sobre a sua apólice.", "Olá! Sou cliente da Alpen e quero falar com o corretor."),
]


# ---------------------------------------------------------------- blocos comuns
def head(title, desc, path, ld, og_title=None):
    url = SITE + path
    blocos_ld = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>' for x in ld)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="KwMUnPhEpfxivuKFeh3EmDZfdwKrWBm_-2yaFCS8dkA">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="BR-ES">
<meta name="geo.placename" content="Vitória, Vila Velha, Espírito Santo">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Alpen Seguros">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/og-alpen-seguros.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Newsreader:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={versao('assets/site.css')}">
<script>document.documentElement.classList.add('js')</script>
{blocos_ld}
<!-- Google Ads: conversão "Clique no WhatsApp" (criada em 24/06/2026) -->
<script>
// Carrega o Google Ads depois que a página abriu (os eventos ficam na fila até lá)
window.addEventListener('load',function(){{var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=AW-18230041101';document.head.appendChild(s);}});
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());
gtag('config','AW-18230041101');
window.alpenConversao=function(){{gtag('event','conversion',{{'send_to':'AW-18230041101/6PaYCPKf7MQcEI204fRD'}});}};
document.addEventListener('click',function(e){{if(e.target.closest('a[href*="wa.me"]'))window.alpenConversao();}});
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
"""


def header(atual=""):
    def item(href, txt):
        cur = ' aria-current="page"' if href == atual else ""
        return f'<li><a href="{href}"{cur}>{txt}</a></li>'
    return f"""<header class="top">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Alpen Seguros, página inicial">
      <img class="brand-mark" src="/img/alpen-simbolo.webp" alt="" width="74" height="92">
      <img class="brand-name" src="/img/alpen-nome.webp" alt="Alpen Seguros" width="236" height="60">
    </a>
    <ul>
      {item("/#seguros", "Seguros")}
      {item("/seguro-para-profissionais/", "Para profissionais")}
      {item("/#sobre", "Sobre nós")}
      {item("/#cliente", "Já sou cliente")}
    </ul>
    <a class="btn btn-gold" href="#cotacao" data-focus>Pedir cotação</a>
  </div>
</header>
"""


def ridge():
    return """    <svg class="ridge" viewBox="0 0 1440 110" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 110V86l120-34 70 22 150-62 110 48 90-28 160 66 120-40 140 30 170-80 130 54 90-24 90 44V110Z" fill="#fff"/>
      <path d="M0 86l120-34 70 22 150-62 110 48 90-28 160 66 120-40 140 30 170-80 130 54 90-24 90 44" fill="none" stroke="#C9A84C" stroke-width="1.5" vector-effect="non-scaling-stroke"/>
    </svg>"""


def form(pre="seguro-auto"):
    chips = []
    for p in PAGINAS:
        valor = p.get("valor_chip", p["nome"])
        chk = " checked" if p["slug"] == pre else ""
        chips.append(f'<label class="chip"><input type="radio" name="produto" value="{valor}"{chk}><span>{ic(p["icone"])}{p["chip"]}</span></label>')
    chips_html = "\n            ".join(chips)
    return f"""      <form class="quote" id="cotacao" novalidate>
        <h2>Peça sua cotação</h2>
        <p class="sub">Grátis e sem compromisso. Leva 30 segundos.</p>
        <fieldset>
          <legend>O que você quer proteger?</legend>
          <div class="chips">
            {chips_html}
          </div>
        </fieldset>
        <div class="field">
          <label for="nome">Seu nome</label>
          <input id="nome" name="nome" autocomplete="given-name" placeholder="Como podemos te chamar?">
        </div>
        <div class="field">
          <label for="cidade">Cidade <small>(opcional)</small></label>
          <input id="cidade" name="cidade" autocomplete="address-level2" placeholder="Vila Velha, Vitória, Serra…">
        </div>
        <p class="err" id="err" role="alert"></p>
        <button class="btn btn-gold" type="submit"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg>Receber proposta no WhatsApp</button>
        <p class="fine">Abre uma conversa com o corretor. Seus dados não são compartilhados.</p>
      </form>"""


def foto(slug, alt, icone, cls="shot", sizes="(max-width: 960px) 100vw, 560px"):
    # Fotos geradas por _build/otimizar_fotos.py em duas larguras (WebP leve).
    # Se o arquivo ainda não existir, a imagem some e o ícone do seguro aparece no lugar.
    if os.path.exists(os.path.join(RAIZ, "img", "fotos", f"{slug}-800.webp")):
        img = (f'<img src="/img/fotos/{slug}-800.webp" srcset="/img/fotos/{slug}-480.webp 480w, /img/fotos/{slug}-800.webp 800w, /img/fotos/{slug}-1200.webp 1200w" '
               f'sizes="{sizes}" alt="{alt}" loading="lazy" decoding="async" '
               f'onerror="this.parentNode.classList.add(\'nofoto\')">')
        extra = ""
    else:
        img, extra = "", " nofoto"
    return f'<figure class="{cls} reveal{extra}">{img}{ic(icone, "fallback")}</figure>'


def faq_html(itens, links=None):
    out = []
    for q, a in itens:
        if links and q in links:
            txt, href = links[q]
            a = a.replace(txt, f'<a href="{href}">{txt}</a>')
        out.append(f"        <details><summary>{q}</summary><p>{a}</p></details>")
    return "\n".join(out)


def faq_ld(itens):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in itens]}


def final_cta():
    return f"""  <section class="final">
    <div class="wrap">
      <h2>Quer saber quanto custa? Pergunte, é grátis.</h2>
      <p>Uma conversa rápida no WhatsApp e você recebe a proposta explicada, sem compromisso.</p>
      <div class="actions">
        <a class="btn btn-gold" href="#cotacao" data-focus>Pedir cotação</a>
        <a class="btn btn-ghost" href="tel:+{WA}">Ligar {FONE_FMT}</a>
      </div>
    </div>
  </section>"""


def footer():
    links = "\n".join(f'          <li><a href="/{p["slug"]}/">{p["nome"]}</a></li>' for p in PAGINAS + [ALAGAMENTO])
    return f"""<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <img class="foot-logo" src="/img/alpen-logo.webp" alt="Alpen Seguros" width="300" height="279" loading="lazy">
        <address>
          Alpen Seguros, corretora de seguros na Grande Vitória (ES)<br>
          R. Neves Armond, 174, Vitória, ES, 29052-280<br>
          Segunda a sexta, 8h às 18h
        </address>
        <p style="margin-top:10px"><a href="https://share.google/4tzNJm3uzbHY8INDY">Avalie a Alpen Seguros no Google</a></p>
      </div>
      <div>
        <h2>Contato</h2>
        <ul class="contact">
          <li><a href="https://wa.me/{WA}"><svg viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg><span><span class="sr">WhatsApp </span>{FONE_FMT}</span></a></li>
          <li><a href="mailto:jobson.azevedo@alpenseguros.com.br"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg><span><span class="sr">E-mail </span>jobson.azevedo@alpenseguros.com.br</span></a></li>
          <li><a href="https://www.instagram.com/alpenseguros"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".8" fill="currentColor" stroke="none"/></svg><span><span class="sr">Instagram </span>@alpenseguros</span></a></li>
        </ul>
      </div>
      <div>
        <h2>Seguros</h2>
        <ul>
{links}
        </ul>
      </div>
    </div>
    <p class="legal">Alpen Seguros, corretora independente credenciada. SUSEP nº 262180897. Bradesco Seguros é marca registrada de seus titulares. Fontes dos dados: Detran-ES, CBMES, CNseg.</p>
  </div>
</footer>
<div class="mbar">
  <a class="btn btn-gold" href="#cotacao" data-focus>Pedir cotação</a>
  <a class="btn btn-ghost" href="tel:+{WA}" aria-label="Ligar para a Alpen Seguros">Ligar</a>
</div>
<script src="/assets/site.js?v={versao('assets/site.js')}" defer></script>
</body>
</html>
"""


EMPRESA_ID = SITE + "/#empresa"


def empresa_ld():
    return {
        "@context": "https://schema.org",
        "@type": "InsuranceAgency",
        "@id": EMPRESA_ID,
        "name": "Alpen Seguros",
        "description": "Corretora de seguros em Vila Velha e Vitória (ES). Seguro auto, residencial, de vida, consórcio, seguro empresarial, plano de saúde, plano dental e seguros para profissionais liberais.",
        "url": SITE + "/",
        "logo": SITE + "/img/og-alpen-seguros.jpg",
        "image": SITE + "/img/og-alpen-seguros.jpg",
        "telephone": "+55-27-99985-7302",
        "email": "jobson.azevedo@alpenseguros.com.br",
        "founder": {"@type": "Person", "name": "Jobson Azevedo", "jobTitle": "Corretor de seguros"},
        "foundingDate": "2025",
        "address": {"@type": "PostalAddress", "streetAddress": "R. Neves Armond, 174", "addressLocality": "Vitória",
                    "addressRegion": "ES", "postalCode": "29052-280", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -20.3010, "longitude": -40.2917},
        "areaServed": ["Vila Velha", "Vitória", "Serra", "Cariacica", "Viana", "Guarapari", "Espírito Santo"],
        "sameAs": ["https://www.instagram.com/alpenseguros"],
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                      "opens": "08:00", "closes": "18:00"},
        "priceRange": "$$",
        "identifier": {"@type": "PropertyValue", "propertyID": "SUSEP", "value": "262180897"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Seguros", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": p["nome"], "url": f"{SITE}/{p['slug']}/"}}
            for p in PAGINAS + [ALAGAMENTO]]},
    }


# ---------------------------------------------------------------- home
def home():
    cards = []
    for p in PAGINAS:
        seg, selo = CARDS[p["slug"]]
        cards.append(f"""        <li data-seg="{seg}">
          <a href="/{p['slug']}/">
            {foto(p['slug'], p['foto_alt'], p['icone'], 'card-img', '(max-width: 600px) 50vw, (max-width: 960px) 50vw, 280px')}
            <span class="selo">{selo}</span>
            <span class="card-body"><h3>{p['nome']}</h3><span class="one">{p['curto']}</span><span class="more">Ver coberturas</span></span>
          </a>
        </li>""")
    abas = "\n".join(
        f'        <button type="button" data-seg="{k}" aria-pressed="{"true" if k == "todos" else "false"}">{t}</button>'
        for k, t in ABAS)
    from urllib.parse import quote
    atalhos = "\n".join(
        f"""        <li><a href="https://wa.me/{WA}?text={quote(msg)}">{ic(i)}<strong>{t}</strong><span>{d}</span></a></li>"""
        for i, t, d, msg in ATALHOS)
    ld = [empresa_ld(),
          {"@context": "https://schema.org", "@type": "WebSite", "name": "Alpen Seguros", "url": SITE + "/",
           "publisher": {"@id": EMPRESA_ID}},
          faq_ld(HOME_FAQ)]
    corpo = f"""{header()}
<main id="conteudo">
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <h1>Corretora de seguros em Vila Velha e Vitória</h1>
        <p class="lead">Na Alpen Seguros você entende o que está contratando antes de assinar. Seguro auto, residencial e de vida, consórcio, seguros para empresas e para profissionais liberais, com proposta pelo WhatsApp em até 2 horas.</p>
      </div>
{form()}
    </div>
{ridge()}
  </section>

  <div class="trust">
    <ul class="wrap">
      <li><strong>Corretora credenciada</strong>SUSEP nº 262180897</li>
      <li><strong>Parceira Bradesco Seguros</strong>Agência 1200, condições para correntistas</li>
      <li><strong>Resposta em até 2 horas</strong>Em dias úteis, pelo WhatsApp</li>
      <li><strong>Atendimento local</strong>Vila Velha, Vitória, Serra e Cariacica</li>
    </ul>
  </div>

  <section class="block" id="seguros">
    <div class="wrap">
      <div class="head">
        <h2>Seguros para você, sua família e sua empresa</h2>
        <p class="lead">Escolha um seguro para ver o que cobre, exemplos reais e perguntas frequentes.</p>
      </div>
      <div class="tabs" role="group" aria-label="Filtrar seguros">
{abas}
      </div>
      <ul class="cards">
{chr(10).join(cards)}
      </ul>
    </div>
  </section>

  <section class="flood">
    <div class="wrap flood-grid">
      {foto('seguro-alagamento', ALAGAMENTO['foto_alt'], 'water', 'flood-img')}
      <div>
        <h2>Choveu forte em Vila Velha. Seu carro e sua casa estão cobertos?</h2>
        <p>Alagamento não é coberto em todo seguro. Veja o que conferir na apólice e o que fazer quando a rua enche.</p>
        <a class="btn btn-ghost" href="/seguro-alagamento/">Entender o seguro contra alagamento</a>
      </div>
    </div>
  </section>

  <section class="block" id="como-funciona">
    <div class="wrap">
      <div class="head"><h2>Como funciona</h2></div>
      <ol class="steps">
        <li><h3>Você conta o que precisa</h3><p>Pelo WhatsApp, em poucas mensagens. Sem formulário longo e sem robô.</p></li>
        <li><h3>Recebe a proposta explicada</h3><p>Em até 2 horas, com o que cobre e o que não cobre, em linguagem clara.</p></li>
        <li><h3>Conta com a gente depois</h3><p>Avisamos antes de vencer, revisamos quando sua vida muda e abrimos o sinistro com você.</p></li>
      </ol>
    </div>
  </section>

  <section class="block alt" id="sobre">
    <div class="wrap about">
      <div>
        <h2>Sobre a Alpen Seguros</h2>
        <blockquote>Criamos a Alpen depois de ver muitas famílias descobrirem, na hora do sinistro, que o seguro não cobria o que elas achavam.</blockquote>
        <p class="lead">A Alpen Seguros é uma corretora independente credenciada na SUSEP, fundada em 2025 na Grande Vitória. Trabalhamos com seguros Bradesco e atendemos pessoas, famílias, empresas e profissionais liberais de todo o Espírito Santo.</p>
        <p class="lead">Nosso jeito de trabalhar: explicar cada cobertura antes da assinatura, avisar antes do vencimento e acompanhar o cliente no sinistro até a indenização.</p>
      </div>
      <div class="team">
        <h3>Equipe</h3>
        <div class="person">
          <span class="ph" aria-hidden="true"><img src="/img/equipe/jobson.jpg" alt="" loading="lazy" onerror="this.remove()">JA</span>
          <div>
            <strong>Jobson Azevedo</strong>
            <span class="role">Fundador e corretor responsável</span>
            <p>Foi gerente comercial na Bradesco Seguros por 8 anos, com destaques regionais em seguro auto e residencial.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="block" id="cliente">
    <div class="wrap">
      <div class="head">
        <h2>Já é cliente da Alpen?</h2>
        <p class="lead">Fale direto com o corretor pelo WhatsApp. A mensagem já vai pronta.</p>
      </div>
      <ul class="quick">
{atalhos}
      </ul>
    </div>
  </section>

  <section class="block alt" id="duvidas">
    <div class="wrap">
      <div class="head"><h2>Dúvidas frequentes</h2></div>
      <div class="faq">
{faq_html(HOME_FAQ, HOME_FAQ_LINKS)}
      </div>
    </div>
  </section>

{final_cta()}
</main>
"""
    return head("Alpen Seguros | Corretora de Seguros em Vila Velha e Vitória",
                "Alpen Seguros, corretora em Vila Velha e Vitória (ES). Seguro auto, residencial, de vida, consórcio, empresarial, saúde e dental. Proposta em até 2 horas.",
                "/", ld, og_title="Alpen Seguros, corretora em Vila Velha e Vitória (ES)") + corpo + footer()


# ---------------------------------------------------------------- páginas de seguro
def pagina(p):
    path = f"/{p['slug']}/"
    pre = p.get("chip_padrao", p["slug"])
    destaques = "\n".join(f"          <li>{d}</li>" for d in p["destaques"])

    blocos = []
    if "cobre" in p:
        itens = "\n".join(f"          <li>{c}</li>" for c in p["cobre"])
        dado = ""
        if p.get("dado"):
            d = p["dado"]
            fonte = f"<small>{d['fonte']}</small>" if d["fonte"] else ""
            dado = f'\n        <div class="fact"><strong>{d["titulo"]}</strong><p>{d["texto"]}</p>{fonte}</div>'
        blocos.append(f"""  <section class="block">
    <div class="wrap split">
      <div>
        <h2>{p['cobre_titulo']}</h2>
        <ul class="checks">
{itens}
        </ul>
      </div>
      <div class="side">
        {foto(p['slug'], p['foto_alt'], p['icone'])}{dado}
      </div>
    </div>
  </section>""")
    if "casos" in p:
        casos = "\n".join(f"        <div><h3>{h}</h3><p>{t}</p></div>" for h, t in p["casos"])
        blocos.append(f"""  <section class="block alt">
    <div class="wrap">
      <div class="head"><h2>{p['casos_titulo']}</h2></div>
      <div class="cases">
{casos}
      </div>
    </div>
  </section>""")
    if "perfis" in p:
        perfis = "\n".join(
            f"""        <section>
          <h2>{t}</h2>
          <p>{txt}</p>
          <ul>{''.join(f'<li>{i}</li>' for i in lst)}</ul>
        </section>""" for t, txt, lst in p["perfis"])
        blocos.append(f"""  <section class="block">
    <div class="wrap">
      {foto(p['slug'], p['foto_alt'], p['icone'], 'shot wide')}
      <div class="profiles">
{perfis}
      </div>
      <p class="note">{p['perfis_nota']}</p>
    </div>
  </section>""")

    rel = "\n".join(f'        <li><a href="/{s}/">{POR_SLUG[s]["nome"]}</a></li>' for s in p["relacionados"])
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["nome"],
         "description": p["desc"], "url": SITE + path, "provider": {"@id": EMPRESA_ID},
         "areaServed": ["Vila Velha", "Vitória", "Serra", "Cariacica", "Viana", "Espírito Santo"]},
        faq_ld(p["faq"]),
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Alpen Seguros", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["nome"], "item": SITE + path}]},
        empresa_ld(),
    ]
    corpo = f"""{header(path)}
<main id="conteudo">
  <section class="hero inner">
    <div class="wrap hero-grid">
      <div>
        <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">›</span>{p['nome']}</nav>
        <h1>{p['h1']}</h1>
        <p class="lead">{p['lead']}</p>
        <ul class="highlights">
{destaques}
        </ul>
      </div>
{form(pre)}
    </div>
{ridge()}
  </section>

{chr(10).join(blocos)}

  <section class="block">
    <div class="wrap">
      <div class="head"><h2>Dúvidas sobre {p['nome'].lower() if p['slug'] != 'seguro-para-profissionais' else 'seguros para profissionais'}</h2></div>
      <div class="faq">
{faq_html(p['faq'])}
      </div>
    </div>
  </section>

  <section class="block alt">
    <div class="wrap">
      <div class="head"><h2>Veja também</h2></div>
      <ul class="related">
{rel}
      </ul>
    </div>
  </section>

{final_cta()}
</main>
"""
    return head(p["title"], p["desc"], path, ld) + corpo + footer()


# ---------------------------------------------------------------- gravação
def gravar(rel, conteudo):
    caminho = os.path.join(RAIZ, rel)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("ok", rel)


def main():
    gravar("index.html", home())
    urls = ["/"]
    for p in PAGINAS + [ALAGAMENTO]:
        gravar(f"{p['slug']}/index.html", pagina(p))
        urls.append(f"/{p['slug']}/")
    sm = "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{HOJE}</lastmod>\n    <priority>{'1.0' if u == '/' else '0.8'}</priority>\n  </url>"
        for u in urls)
    gravar("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')


if __name__ == "__main__":
    main()
