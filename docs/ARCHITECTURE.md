# Arquitetura técnica — Projeto Ybyrá

**Estado do documento:** arquitetura de referência para um protótipo educacional. Não especifica sistema implantado nem interface certificada. “Aurora XAI” e “Malha Quântica Pindorama” são nomes de módulos/propostas deste repositório, não programas ou plataformas institucionais.

## Objetivos de desenho

O software deve permitir experimentos reproduzíveis em ambiente local, expor premissas e manter fronteiras explícitas entre simulação e hardware. Os módulos não fazem chamadas de rede, não têm credenciais externas e não processam material biológico real. A interface entre os subsistemas é por valores em memória e arquivos controlados pelo operador.

## Componentes

| Pacote | Responsabilidade implementada | Fora do escopo atual |
|---|---|---|
| `dna_storage` | Mapeamento 2 bits→base e paridade RS opcional para pequenos blocos | Síntese/leitura molecular, integração com plantas, CRISPR e fluxo de bancada |
| `hybrid_ai` | Sigmoide com decomposição de contribuições e detecção de picos numéricos | XAI validada, modelo treinado, classificação neural/organoide ou uso clínico |
| `quantum_mesh` | Simulação clássica BB84 com interceptação-resend e prova Merkle simples | Dispositivos quânticos, enlace LEO, QKD segura/certificada, STARK ou Drex |

## Fluxos

1. Um chamador fornece bytes a `encode_bytes`. A função acrescenta paridade opcional e converte cada par de bits em uma base. A saída é apenas uma representação textual e metadados de tamanho.
2. Uma coleção de candidatos declarativos pode ser ordenada por uma função de pontuação heurística. Ela não examina sequências e não recomenda intervenção experimental.
3. Um vetor de características pode ser transformado em probabilidade logística acompanhada das contribuições ponderadas. Um traço numérico pode ser usado para localizar picos negativos.
4. A simulação BB84 sorteia bits e bases em Python. A QBER é calculada somente no subconjunto em que as bases de Alice e Bob coincidem.
5. A demonstração Merkle calcula hash da folha e irmãos para provar inclusão sob uma raiz. Ela não oculta o conteúdo e não demonstra conhecimento zero.

## Diagrama de hardware/armazenamento (conceitual)

![Diagrama conceitual de armazenamento](ASSETS/dna-storage-architecture.png)

O diagrama inclui, como hipótese de pesquisa ainda não validada, uma etapa futura entre a representação digital e eventual avaliação de armazenamento biológico. Essa fronteira não equivale a protocolo, vetor funcional, alvo validado ou recomendação para transformar organismos. O código executável termina na string A/C/G/T.

## Diagrama da malha quântica (conceitual)

![Diagrama conceitual da malha quântica](ASSETS/pindorama-quantum-mesh.png)

O desenho distingue a simulação de software de qualquer enlace orbital e de sistemas bancários. Um adaptador futuro com DREX/BCB ou participação AEB seria dependente de aprovação, requisitos e interfaces oficiais. Nenhuma relação institucional é representada como existente.

## Segurança, privacidade e operação

O protótipo não coleta telemetria nem transmite dados. Inputs não confiáveis ainda devem ser validados pela aplicação que os integra. Não usar os módulos para gestão de chaves, liquidação financeira, decisões clínicas, edição genética ou operações críticas. Um emprego real exigiria threat modeling, revisão criptográfica independente, engenharia de confiabilidade, governança de dados, políticas de segurança e validações legais e regulatórias.

## CI

O workflow `.github/workflows/CI-CD-Deploy.yml` instala as dependências declaradas e executa os testes unitários em push e pull request. O pipeline valida o código; ele não publica um artefato de produção nem ativa integração com provedor externo. A ativação futura de Vercel, Netlify ou Hugging Face depende de conectar e autorizar os respectivos serviços.
