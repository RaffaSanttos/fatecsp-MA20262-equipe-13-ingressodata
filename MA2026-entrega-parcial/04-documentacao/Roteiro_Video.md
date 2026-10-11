# Roteiro do vídeo: extração, limpeza e tabela dinâmica (≈ 6 min)

Gravar a tela em 1080p (Win + G no Windows ou Cmd + Shift + 5 no Mac). A legenda já está pronta em `legenda_video.srt`: no editor (CapCut, Clipchamp, YouTube Studio) basta importar o arquivo. Se o tempo de alguma cena mudar, ajuste só os horários do .srt.

| Tempo | Tela | O que mostrar |
|---|---|---|
| 0:00–0:20 | Leia_me | Apresentar o projeto e a pergunta central |
| 0:20–0:50 | Pasta dados-brutos | Abrir os 3 arquivos e mostrar as diferenças de data, valor e grafia |
| 0:50–1:20 | Base_Bruta | Base empilhada, filtrar Categoria para mostrar as grafias diferentes |
| 1:20–2:10 | Tratamento | Clicar nas colunas Data_Venda, Valor_Unitario e Categoria e ler a fórmula (DATA, VALORNUMERO, PROCX) |
| 2:10–2:40 | Tratamento | Origem_Publico, Duplicado e Status |
| 2:40–3:10 | Auditoria | 2.091 = 12 + 49 + 30 + 2.000 e status APROVADO |
| 3:10–4:20 | Power Query | Mostrar as consultas, o passo a passo aplicado na Fato e o total de 2.000 linhas |
| 4:20–5:30 | Tabela dinâmica | Inserir > Tabela Dinâmica sobre tbVendasTratadas: Categoria nas linhas, Origem_Publico nas colunas, Soma de Valor_Total nos valores, Status = OK no filtro |
| 5:30–6:00 | Resumo_KPIs | Fechar com os números: 42,7% do faturamento vem de turistas |
