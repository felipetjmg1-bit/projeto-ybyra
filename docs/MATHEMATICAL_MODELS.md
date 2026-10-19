# Modelos matemáticos e hipóteses

Este documento descreve modelos de software para ensino. Não declara segurança criptográfica, rendimento biológico ou validade de engenharia física.

## 1. Codificação binário-para-nucleotídeo (B2N)

Para bytes de entrada, expande-se cada byte em bits, em ordem mais significativa primeiro. Cada par é mapeado por uma tabela bijetiva:

| Bits | Base |
|---|---|
| `00` | A |
| `01` | C |
| `10` | G |
| `11` | T |

Assim, sem paridade, uma mensagem de `n` bytes gera `4n` caracteres de base. Para um bloco `m` de bytes, pode-se aplicar um código Reed–Solomon sobre GF(2^8) com `r` símbolos de paridade: `c = RS_encode(m, r)`. A distância mínima nominal é `d_min = r + 1`, permitindo correção de até `floor(r/2)` erros de símbolo ou `r` apagamentos se suas posições forem conhecidas, sob as hipóteses do código e dos parâmetros. O protótipo guarda o tamanho original e limita cada bloco codificado a 255 bytes. Não define blocagem, sincronização, endereçamento, controle de GC, viés de sequência ou canal físico.

O mapa 2 bits→base é apenas uma codificação. Não é codonização, expressão gênica, desenho CRISPR, nem garantia de estabilidade molecular.

## 2. BB84 didático e QBER

Em cada rodada `i`, Alice sorteia bit `a_i ∈ {0,1}` e base `x_i ∈ {Z,X}`; Bob escolhe `y_i ∈ {Z,X}` e obtém bit `b_i`. Após comparação pública de bases, o conjunto peneirado é `S = {i : x_i = y_i}`. A taxa de erro quântico estimada neste conjunto é:

`QBER = (1 / |S|) · Σ_{i∈S} 1[a_i ≠ b_i]`.

O simulador inclui um adversário opcional de interceptação e reenvio, mas não implementa estados quânticos. No modelo ideal e sem adversário, bases diferentes são descartadas e bases iguais concordam. A detecção usa somente a regra configurada `QBER > threshold`. Uma execução de software não dá estimativa de chave secreta finita nem demonstra segurança. Canal clássico autenticado, reconciliação, amplificação de privacidade e modelo de dispositivo ficam fora do escopo.

## 3. Escore logístico explicável

Para características `x_j`, pesos `w_j` e viés `b`, o protótipo calcula contribuições `c_j = x_j w_j`, logit `z = b + Σ_j c_j` e probabilidade `p = σ(z) = 1/(1+e^(−z))`. O rótulo demonstrativo usa `p ≥ τ`. A decomposição expõe os termos do logit; não estabelece causalidade e não valida qualidade preditiva. Os pesos precisam ser fornecidos pelo chamador.

## 4. Detecção de eventos em sinal

Para traço `s`, o detector estima mediana `m` e desvio absoluto mediano `MAD = median(|s_i−m|)`. O limiar negativo é `m − k·1.4826·MAD`, com `k > 0`. Um índice é candidato se for mínimo local e estiver abaixo do limiar, respeitando período refratário configurado. É um filtro heurístico; não inclui filtragem de banda, ruído correlacionado, agrupamento por forma de onda nem revisão por especialistas.

## 5. Compromisso Merkle demonstrativo

A folha é `H(0x00 || dado)` e o nó interno `H(0x01 || esquerdo || direito)`, com SHA-256. O verificador refaz o caminho de irmãos até a raiz. Isso prova inclusão de uma folha sob uma raiz conhecida, mas não oculta o dado. Não é prova zero-knowledge, SNARK ou STARK, não executa protocolo de consenso e não se conecta ao Drex. O nome do módulo é histórico/conceitual; o algoritmo implementado é somente Merkle.
