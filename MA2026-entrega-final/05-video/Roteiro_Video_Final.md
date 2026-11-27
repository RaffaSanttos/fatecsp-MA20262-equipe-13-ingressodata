# Roteiro do vídeo da entrega final (≈ 8 min 51 s)

Vídeo base (sem áudio): `IngressoData_Entrega_Final_sem_audio.mp4` (gravado com a Ferramenta de Captura do Windows, 1920×1080). A narração abaixo já está cortada nos tempos do vídeo; a mesma narração está em `legenda_video_final.srt` para usar como legenda.

**Como montar:** gere o áudio de cada bloco numa IA de voz (sugestões no fim), importe o vídeo e os áudios no Clipchamp (vem no Windows) e alinhe cada áudio no tempo de início do bloco. Se algum áudio ficar mais longo que a cena, aumente a velocidade da voz para 1,1× ou corte uma frase.

| Início | Fim | Tela | Narração |
|---|---|---|---|
| 0:00 | 0:14 | Excel, aba Leia_me com os botões | Olá! Este é o IngressoData Brasil, o projeto da equipe 13 de Microinformática Aplicada. Nesta entrega final mostramos a planilha, as macros, o banco de dados, as APIs e o painel no Power BI. |
| 0:14 | 0:40 | Resumo_KPIs | Começando pelo Excel: a aba Resumo_KPIs reúne faturamento, ticket médio e participação dos turistas, com barras de dados e escala de cores feitas por formatação condicional. |
| 0:40 | 1:04 | Consulta de evento | Mais abaixo, a consulta de evento usa ÍNDICE com CORRESP duplo. Escolhemos o evento na lista suspensa e a planilha busca categoria, cidade, local e data no cadastro, além do faturamento e do percentual de turistas daquele evento. |
| 1:04 | 1:40 | Aba Tratamento | Na aba Tratamento, cada coluna é uma fórmula de limpeza. A formatação condicional destaca em vermelho as linhas descartadas, como duplicadas e vendas sem quantidade, e em amarelo qualquer valor que ficou sem padronização. |
| 1:40 | 1:49 | Auditoria | A Auditoria confere que nenhuma linha some: duas mil e noventa e uma linhas brutas viram duas mil vendas válidas, com status aprovado. |
| 1:49 | 2:16 | DePara_Categoria | As tabelas de padronização têm validação de dados: listas suspensas, valores sem espaços sobrando e sem duplicidade. Assim ninguém digita uma categoria errada. |
| 2:16 | 2:46 | Leia_me → Relatório semanal | Agora a automação em VBA. Os botões da aba Leia_me chamam as macros. O relatório semanal percorre a base com laços e condicionais e cria uma aba nova com pedidos, ingressos, faturamento e percentual de turistas por evento e praça. |
| 2:46 | 3:19 | Editor VBA, mdlRelatorioVendas | No editor do VBA ficam os módulos. Aqui estão as variáveis, os laços For e as condições If que montam o relatório, e as rotinas de relatório diário, semanal e por período. |
| 3:19 | 3:35 | Editor VBA, mdlMacroGravada | Esta outra macro foi gravada com o Gravador de Macros: repare no código gerado automaticamente, com Application.Goto e AutoAjuste das colunas. |
| 3:35 | 3:52 | Power Pivot, aba Conferencia | No Power Pivot montamos o modelo de dados com cinco tabelas, quatro relacionamentos e catorze medidas em DAX. A tabela dinâmica do modelo bate com o gabarito: dois milhões e trinta e sete mil reais de faturamento. |
| 3:52 | 4:01 | Terminal: carga do banco | Passando para o banco de dados: o script cria as tabelas com chaves primárias e estrangeiras e carrega as duas mil vendas, sem nenhuma violação de chave. |
| 4:01 | 4:09 | Terminal: Q1 | A primeira consulta usa SELECT, GROUP BY e ORDER BY para calcular os indicadores por categoria. |
| 4:09 | 4:17 | Terminal: Q3 | A segunda junta a fato com a dimensão de eventos usando JOIN e filtra com WHERE só os eventos ao ar livre. |
| 4:17 | 4:22 | Terminal: view | A view de KPIs gerais confirma os mesmos números do Excel. |
| 4:22 | 4:58 | Terminal: APIs | Para enriquecer os dados, consumimos duas APIs REST gratuitas: a do Banco Central, com a cotação do dólar de cada dia, e a Open-Meteo, com temperatura e chuva das três praças. Foram seiscentos e oitenta e três dias de câmbio e mais de duas mil linhas de clima. |
| 4:58 | 5:14 | Power BI, Visão Geral | Tudo isso termina no dashboard do Power BI. A Visão Geral mostra os principais números: dois milhões de reais em ingressos, ticket médio de quinhentos e trinta e cinco reais e quarenta e dois vírgula sete por cento do faturamento vindo de turistas. |
| 5:14 | 5:30 | Clique em Festival | Os visuais são interativos: ao clicar em Festival, todo o painel filtra. Os festivais concentram a maior parte da receita e do público turista. |
| 5:30 | 5:42 | Público Turista | A página Público Turista detalha cada evento, compara compradores nacionais e estrangeiros e traz os visitantes internacionais que chegam ao Brasil por país. |
| 5:42 | 6:02 | Fatores Externos | Em Fatores Externos cruzamos as vendas com o dólar no dia da compra e com o clima no dia do evento, que vieram das APIs. |
| 6:02 | 6:32 | Exibição de modelo | Na exibição de modelo aparece o esquema estrela: a fato de vendas no centro, ligada às dimensões de evento, praça, comprador e calendário. |
| 6:32 | 6:59 | Editor do Power Query | No Power Query estão todas as consultas: leitura dos arquivos, limpeza, padronização e as fontes da web. |
| 6:59 | 7:25 | Web_Visitantes_Pais | Esta consulta faz web scraping de uma tabela da Wikipédia com os visitantes internacionais por país. Ela vem em formato largo, com uma coluna para cada ano. |
| 7:25 | 7:44 | Fato_Visitantes_Internacionais | A consulta seguinte aplica o unpivot: as colunas de ano viram linhas, com país, ano e número de visitantes. |
| 7:44 | 8:24 | Passos aplicados | Depois disso ela limpa os números, padroniza o nome dos países com a mesma tabela de-para das vendas e marca quais países também aparecem entre os nossos compradores. |
| 8:24 | 8:51 | Power BI, Visão Geral | Concluindo: partimos de três planilhas bagunçadas e chegamos a um painel que responde à pergunta central. Quarenta e dois vírgula sete por cento do faturamento vem de turistas, e nos festivais esse número chega a quarenta e cinco por cento. Obrigado! |

## IAs gratuitas para a narração (voz natural em português do Brasil)

| Ferramenta | Grátis? | Observação |
|---|---|---|
| **Clipchamp** (já vem no Windows) | Sim, na função Texto para fala | Tem vozes neurais da Microsoft em pt-BR (Francisca, Antônio etc.). Gera o áudio direto na linha do tempo do vídeo, então dá para narrar e montar no mesmo lugar. Dividir textos longos em vários blocos. |
| **ElevenLabs** | Plano gratuito de 10 mil créditos por mês | Considerada uma das vozes mais naturais. O plano grátis é só para uso não comercial e com atribuição (serve para trabalho acadêmico). O roteiro acima tem cerca de 6 mil caracteres. |
| **Google AI Studio (Gemini TTS)** | Testes no AI Studio | Suporta pt-BR e aceita instruções de estilo ("fale de forma calma e didática"). Precisa de conta Google. |
| **Amazon Polly / Google Cloud TTS** | Cotas gratuitas | Vozes neurais boas, mas exigem configurar conta de nuvem. |

Dica: teste o primeiro bloco em duas ferramentas e escolha a voz que soar melhor antes de gerar o resto.
