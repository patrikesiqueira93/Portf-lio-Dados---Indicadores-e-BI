Detalhes Técnicos e Escopo do Projeto: Gestão de Frotas e Manutenção (Control Tower)
Este repositório contém uma solução completa (End-to-End) de Engenharia e Análise de Dados voltada para a gestão executiva de frotas, manutenção de equipamentos, acompanhamento de SLAs operacionais e controle de custos de OPEX.
1. Arquitetura da Solução & Pipeline de Dados
O projeto adota a Arquitetura Medallion (Bronze, Silver e Gold), garantindo governança, qualidade, rastreabilidade e alta performance no processamento e consumo analítico dos dados.
[Fontes / CSVs] ──> [Camada BRONZE (Raw)] ──> [Camada SILVER (Cleansed)] ──> [Camada GOLD (Star Schema)] ──> [Power BI]


Camada Bronze (Raw Data): Captura e ingestão dos dados brutos operacionais e de cadastros em formato Parquet, preservando a integridade e o histórico do dado de origem.
Camada Silver (Cleansed & Enriched): Limpeza, padronização de tipos de dados, tratamento de nulos, remoção de duplicidades e aplicação das regras de negócio (cálculo de tempos de atendimento em horas e criação de flags de estouro de SLA).
Camada Gold (Analytics & Star Schema): Modelagem dimensional otimizada em arquivos Parquet prontos para consumo de alto desempenho no Power BI.
2. Modelagem de Dados (Star Schema)
A camada analítica no Power BI foi modelada sob o padrão dimensional Star Schema (Esquema Estrela) com relacionamentos  unidirecionais de alta eficiência:
Tabela Fato:
fato_chamados: Registros operacionais das ordens de manutenção, contendo datas de abertura, início e fechamento, tempos totais de atendimento, custos operacionais e sinalizações de cumprimento de SLA.
Tabelas Dimensão:
dim_equipamento: Atributos detalhados dos ativos, cobrindo categorias (Caminhão Heavy Duty, Escavadeira, Trator, Utilitário, etc.) e filiais operacionais.
dim_tempo: Calendário dinâmico em português (PT-BR) para análises temporais por ano, trimestre, mês e dia da semana.
Tabela Técnica:
_Medidas: Tabela repositório para centralização exclusiva e organização de todas as fórmulas DAX.
3. Principais Medidas DAX Implementadas
As métricas calculadas combinam regras de negócio operacionais e financeiras:
Total de Chamados:

Custos Operacionais (OPEX):

Tempo Médio de Atendimento (MTTR):

Volume de Chamados em Atraso:

Taxa de Cumprimento de SLA:

Média de Tempo Excedido:

Custo Financeiro dos Atrasos:

4. Recursos Avançados de UI/UX & Customização Visual
Para garantir um acabamento executivo de nível Control Tower, o painel utiliza soluções avançadas de design:
Layouts de Fundo Customizados em SVG (16:9 - 1280x720):
Construção dos arquivos background_capa.svg e background_dashboard.svg utilizando gradientes escuros sóbrios (#0F172A, #1E293B), barras de molduras luminosas em azul executivo e ilustrações em baixa opacidade representando malhas logísticas e frotas de transporte.
KPI Cards Customizados via HTML Content (HTML/CSS):
Criação de cartões dinâmicos desenvolvidos diretamente com marcas HTML e CSS inline (através do suplemento HTML Content), garantindo sombras suaves, accent bars laterais com formatação condicional de cores e tipografia responsiva sem dependência dos visuais nativos.
Gráficos Declarativos em JSON / Vega-Lite via Deneb:
Implementação do visual customizado Deneb para construir gráficos empilhados em especificação JSON/Vega-Lite, permitindo total controle sobre eixos, tooltips customizados e esquemas condicionais de cor.
5. Estrutura e Objetivos das Páginas do Dashboard
Página 1: Capa (Abertura Executiva)
Objetivo: Ponto de entrada elegante para navegação executiva.
Componentes: Título principal (PAINEL DE PERFORMANCE DE FROTAS), subtítulo com foco em indicadores operacionais e análise financeira, background SVG com marca d'água logística corporativa e botão nativo interativo com ação de navegação de página.
Página 2: Visão Geral Operacional (Control Tower)
Objetivo: Acompanhamento diário macro da operação, volumetria de ordens, custos e níveis globais de serviço.
Componentes:
Sidebar: Filtros dinâmicos por Filial, Categoria e Ano, além de 3 Cards HTML para métricas globais (MTTR Horas, Custo Total e % SLA).
Gráfico de Custo por Categoria: Barras horizontais detalhando o impacto financeiro (OPEX) por tipo de ativo.
Matriz de Filiais: Tabela operacional enriquecida com formatação condicional em barras de dados e ícones de status de SLA.
Evolução Temporal: Gráfico de linhas combinando volume mensal de chamados e percentual de atendimento dentro da meta.
Página 3: Análise de SLA & Gargalos Operacionais (Diagnóstico Causa-Raiz)
Objetivo: Isolamento de ineficiências operacionais, identificação dos principais causadores de atrasos e impacto nos custos.
Componentes:
Sidebar: 3 Cards HTML com destaque focado em gargalos (Chamados em Atraso, Impacto Financeiro OPEX e Média de Tempo Excedido).
Matriz de Risco (Gráfico de Dispersão): Análise cruzada do tempo médio de atendimento (MTTR) contra o volume de chamados em atraso, contendo linhas de referência média que dividem o gráfico em 4 quadrantes operacionais.
Gráfico Customizado Deneb (JSON/Vega-Lite): Visual declarativo empilhado mostrando o volume e proporção de conformidade do SLA por filial com cores de destaque (#2563EB no prazo e #EF4444 em atraso).
Matriz Detalhada de Ofensores: Tabela analítica inferior com funcionalidade de drill-down hierárquico por Filial e Categoria de Equipamento.
