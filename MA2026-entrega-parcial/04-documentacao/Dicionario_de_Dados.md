# Dicionário de Dados · Fato_Vendas_Ingressos

| Campo | Tipo | Descrição | Regra de tratamento |
|---|---|---|---|
| ID_Venda | texto | Identificador da venda (prefixo da praça) | linhas vazias e IDs repetidos são descartados |
| Data_Venda | data | Dia da compra | 3 formatos convertidos para data |
| Data_Evento | data | Dia do evento (cinema: dia da sessão) | idem |
| Evento | texto | Nome do evento | espaços removidos |
| Categoria | texto | Show, Festival ou Cinema | De-Para (várias grafias → 3) |
| Cidade_Evento | texto | Praça: São Paulo, Rio de Janeiro ou Belo Horizonte | De-Para |
| Tipo_Ingresso | texto | Inteira, Meia ou VIP | espaços removidos |
| Qtd | inteiro | Ingressos na venda | vazio ou 0 descarta a linha |
| Valor_Unitario | moeda | Preço por ingresso | texto "R$ 1.250,00" vira número; vazio descarta |
| Valor_Total | moeda | Qtd × Valor_Unitario | calculado |
| Canal | texto | Site, App, Bilheteria ou Parceiro | |
| Comprador_ID | texto | Identificador do comprador | |
| Cidade_Comprador | texto | Cidade onde o comprador mora | De-Para (sem acento, maiúsculas etc.) |
| UF_Comprador | texto | UF (EX = exterior) | MAIÚSCULA |
| Pais_Comprador | texto | País do comprador | De-Para (BR, brasil → Brasil) |
| Origem_Publico | texto | Local, Turista Nacional ou Turista Internacional | país ≠ Brasil → Internacional; cidade ≠ sede → Nacional |
| Arquivo_Origem | texto | Arquivo bruto de onde veio a linha | rastreabilidade |

## Dimensões

| Tabela | Chave | Campos |
|---|---|---|
| Dim_Evento | Evento | Categoria, Cidade_Evento, Local, Ao_Ar_Livre, Data_Evento |
| Dim_Praca | Cidade | UF, Regiao, Latitude, Longitude (usadas na API de clima) |
| Dim_Comprador | Comprador_ID | Cidade, UF, País, Tipo_Comprador (Nacional/Estrangeiro) |
| Dim_Calendario | Data | Ano, Mes, Nome_Mes, Ano_Mes, Trimestre, Dia_Semana, Fim_de_Semana |
