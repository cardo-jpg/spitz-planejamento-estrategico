// Fonte: [SP] Fonte de dados Ecom (Meta) — atualizado 12/07/2026 (campanha ao vivo)
// METAD: [data'DD/MM', investimento, impressoes, cliques, visitas, add_carrinho, checkout, vendas, faturamento]
const METAD=[
["01/07", 764.62, 281320, 628, 228, 15, 6, 20, 2264.57],
["02/07", 775.57, 257110, 582, 233, 15, 10, 10, 3067.02],
["03/07", 789.11, 210295, 576, 194, 28, 16, 12, 3728.46],
["04/07", 1567.13, 387786, 1108, 401, 58, 26, 16, 4567.5],
["05/07", 1223.17, 370333, 855, 304, 52, 19, 12, 3521.42],
["06/07", 940.49, 316363, 905, 397, 67, 29, 16, 5098.91],
["07/07", 1086.5, 285644, 878, 341, 49, 24, 20, 6507.43],
["08/07", 1075.54, 275737, 938, 390, 73, 40, 28, 9300.07],
["09/07", 725.35, 182013, 643, 246, 59, 27, 19, 6985.51],
["10/07", 487.72, 100636, 455, 129, 28, 13, 11, 4009.41],
["11/07", 500.91, 108300, 566, 163, 36, 20, 15, 5385.15],
["12/07", 707.97, 190666, 821, 221, 78, 44, 25, 7718.66],
["13/07", 973.16, 189224, 791, 173, 94, 46, 27, 9410.97]
];
// Google ainda nao atualizado para 2026 — entra quando a fonte for atualizada
const GOOGC=[];
const DASH_ANO='2026';

// Campanhas de MARCA (avaliadas por alcance/CPM, nao por ROAS)
const BRAND={
  recon:{nome:'Reconhecimento — Aberto 200km Pomerode', inv:4982.96, alcance:1195936, cpmAlc:4.17, freq:2.81},
  seg:{nome:'Seguidores', inv:386.46, cliques:215, ctr:0.59, seguidores:6}
};
