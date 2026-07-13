// Fonte: [SP] Fonte de dados Ecom (Meta) — atualizado 12/07/2026 (campanha ao vivo)
// METAD: [data'DD/MM', investimento, impressoes, cliques, visitas, add_carrinho, checkout, vendas, faturamento]
const METAD=[
['01/07',764.62,281320,628,228,15,6,20,2264.57],
['02/07',775.57,257110,582,233,15,10,10,3067.02],
['03/07',789.11,210295,576,194,28,16,12,3728.46],
['04/07',1567.13,387786,1108,401,58,26,16,4567.50],
['05/07',1223.17,370333,855,304,52,19,12,3521.42],
['06/07',940.49,316363,905,397,67,29,16,5098.91],
['07/07',1086.50,285644,878,341,49,24,20,6507.43],
['08/07',1075.54,275737,938,390,73,40,28,9300.07],
['09/07',725.35,182013,643,246,59,27,19,6985.51],
['10/07',487.72,100636,455,129,28,13,11,4009.41],
['11/07',500.90,108293,566,163,36,20,15,5385.15],
['12/07',531.17,148062,586,158,61,37,21,6296.93]
];
// Google ainda nao atualizado para 2026 — entra quando a fonte for atualizada
const GOOGC=[];
const DASH_ANO='2026';

// ===== Snapshot do periodo (jul 1-12/2026) transcrito do Looker =====
// CAMP: [nome, investido, cliques, cpc, ctr, carrinho, checkout, vendas, custo_venda, roas]
const CAMP=[
['SP_FB01_Vendas_Ferias_F',1132.26,639,1.77,1.01,164,86,51,22.20,13],
['SP_FB02_Vendas_Ferias_F',682.74,1008,0.68,1.28,62,34,25,27.31,11],
['lead_recuperacao-de-carrinho_br_20251017',385.74,605,0.64,1.81,70,35,23,16.77,16],
['SP_FB03_Vendas_Lookalike_BR',795.37,1077,0.74,2.70,39,17,20,39.77,6],
['SP_FB05_Vendas_Passaporte_Q_BR',275.19,598,0.46,2.24,61,23,17,16.19,24],
['SP_FB01_Leads_Combo_BR',290.19,1212,0.24,3.52,32,9,13,22.32,17],
['SP_FB04_Vendas_Remarketing_BR',531.44,258,2.06,1.32,23,17,13,40.88,8],
['consideracao_medio-funil_br_20260519',430.34,247,1.74,1.47,9,7,10,43.03,5],
['SP_FB02_Leads_Aniversariantes_SC',176.51,143,1.23,1.45,5,2,5,35.30,6],
['SP_FB02_Vendas_Ferias_Q',387.24,217,1.78,0.59,18,9,5,77.45,4],
['SP_FB01_Vendas_Curitiba_F',85.87,62,1.39,0.95,9,2,3,28.62,13],
['SP_FB01_Vendas_Joinville_F',88.69,69,1.29,0.72,7,3,2,44.35,7],
['SP_FB01_Vendas_Jaragua_F',102.61,72,1.43,0.45,6,3,2,51.31,7],
['SP_FB01_Vendas_Indaial_F',92.83,62,1.50,0.66,4,2,2,46.42,5]
];
// PUB: [nome, investido, cliques, cpc, ctr, carrinho, checkout, vendas, custo_venda, faturamento, roas]
const PUB=[
['RMKT_Carrinho',275.06,598,0.46,2.24,61,23,17,16.18,6613.48,24],
['lista-hub-carrinho-abandonado_menor-custo_20251017',385.74,605,0.64,1.81,70,35,23,16.77,6292.79,16],
['RMKT_VisitantesSite_30d',339.38,175,1.94,1.78,17,14,11,30.85,3604.53,11],
['ADVGT',2938.09,2319,1.27,0.92,264,135,88,33.39,26597.20,9],
['ig-engajamento-organico_90d_consideracao_20260519',175.45,125,1.40,1.60,8,6,5,35.09,1552.49,9],
['LAL_Compradores',511.71,704,0.73,2.64,28,14,16,31.98,3639.50,7],
['Aberto_200km_Pomerode_Aniversariantes',176.34,143,1.23,1.45,5,2,5,35.27,1141.83,6],
['Seguidores',386.46,215,1.80,0.59,18,9,5,77.29,1718.52,4],
['lookalike-1pct-compradores_conversao_20260519',283.50,373,0.76,2.81,11,3,4,70.88,1248.72,4],
['RMKT_Engaja_IG_90d',94.00,40,2.35,0.90,3,2,1,94.00,399.60,4],
['lista-hub-ecomerce_menor-custo_20251029',86.73,153,0.57,1.56,3,3,1,86.73,359.70,4],
['engajamento-video-anuncio_30d_consideracao_20260519',88.54,47,1.88,1.00,0,0,1,88.54,329.70,4]
];
// CRIA: [nome, investido, cliques, cpc, ctr, carrinho, checkout, vendas, ticket, custo_venda, faturamento, roas]
const CRIA=[
['AD02_IMG_Momentos_Leves_E_Inesqueciveis',525.72,249,2.11,0.83,66,37,23,267.31,22.86,6148.02,12],
['estatico_voce-esta-quase-la_saibamais_20251019',385.74,605,0.64,1.81,70,35,23,273.60,16.77,6292.79,16],
['AD06_IMG_Adrenalina',303.84,195,1.56,1.37,59,32,18,363.60,16.88,6544.83,22],
['video_compre-antecipado-passaporte_saibamais_20260127',270.71,589,0.46,2.24,61,23,17,389.03,15.92,6613.48,24],
['video_quanto-custa-um-dia_saibamais_lal-site_20260519',508.23,702,0.72,2.65,28,14,16,227.47,31.76,3639.50,7],
['video_combo-pomerode_saibamais_20262602',290.28,1212,0.24,3.51,32,9,13,379.50,22.33,4933.48,17]
];
// Campanhas de MARCA (avaliadas por alcance/CPM, nao por ROAS)
const BRAND={
  recon:{nome:'Reconhecimento — Aberto 200km Pomerode', inv:4982.96, alcance:1195936, cpmAlc:4.17, freq:2.81},
  seg:{nome:'Seguidores', inv:386.46, cliques:215, ctr:0.59, seguidores:6}
};
