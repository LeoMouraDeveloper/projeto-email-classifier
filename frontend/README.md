# 🎨 Email Classifier - Frontend

Interface web moderna construída com **React + TypeScript** para classificação inteligente de emails com análise comparativa NLP vs Gemini AI.

## 📋 Funcionalidades

### 🔄 Entrada de Dados
- **📝 Entrada de Texto**: Interface para colar texto do email diretamente
- **📎 Upload de Arquivo**: Suporte para arquivos .txt e .pdf (até 10MB)
- **📱 Interface Responsiva**: Funciona em desktop, tablet e mobile

### 📊 Análise Comparativa
- **🤖 Visualização Dual**: Mostra resultados NLP e Gemini lado a lado
- **🏆 Indicador de Método Escolhido**: Destaque visual do método selecionado
- **📈 Barras de Confiança**: Indicadores coloridos por nível de certeza
- **💭 Justificativas Detalhadas**: Explicação do raciocínio de cada método

### 🎯 Feedback Visual
- **🔄 Estados de Loading**: Indicadores durante processamento
- **✅ Validação em Tempo Real**: Feedback instantâneo de entrada
- **🎨 Códigos de Cor**: Verde para produtivo, laranja para improdutivo
- **📋 Resumo da Decisão**: Explicação clara do critério usado

## 🛠️ Tecnologias

### Core
- **React** 19.1.1 - Framework JavaScript
- **TypeScript** - Tipagem estática
- **Material-UI (MUI)** 7.3.2 - Biblioteca de componentes
- **Axios** 1.12.2 - Cliente HTTP

### Ferramentas
- **Create React App** 5.0.1 - Setup e build
- **React Testing Library** - Testes de componentes
- **ESLint** - Linting de código

## 🏗️ Estrutura do Projeto

```
src/
├── components/
│   ├── EmailClassifier.tsx      # Componente principal
│   └── ComparisonAnalysis.tsx   # Análise comparativa
├── services/
│   └── emailClassifierService.ts # Cliente da API
├── types/
│   └── index.ts                # Interfaces TypeScript
├── App.tsx                     # Componente raiz
└── index.tsx                   # Entry point
```

## 📱 Componentes Principais

### `EmailClassifier.tsx`
**Componente principal** que gerencia toda a interface de classificação.

**Recursos:**
- 🔄 Sistema de tabs (texto/arquivo)
- ⚡ Estados de loading e erro
- 📊 Exibição de resultados com métricas
- 🎨 Layout responsivo com Material-UI

### `ComparisonAnalysis.tsx`
**Componente especializado** para análise comparativa entre métodos.

**Recursos:**
- 📊 Layout lado a lado NLP vs Gemini
- 🏆 Badges indicando método escolhido
- 📈 Barras de progresso para confiança
- 💡 Detalhamento de features e raciocínio

### `emailClassifierService.ts`
**Service layer** para comunicação com a API backend.

**Funcionalidades:**
- 🔗 Integração com endpoints REST
- ✅ Validação de entrada (texto/arquivo)
- 🛡️ Tratamento de erros
- 📝 Tipagem TypeScript completa

## 🎨 Design System

### Paleta de Cores
```css
/* Métodos */
--gemini-color: #2196f3        /* Azul - Gemini AI */
--nlp-color: #9c27b0           /* Roxo - NLP */

/* Classificação */
--productive-color: #4caf50     /* Verde - Produtivo */
--unproductive-color: #ff9800   /* Laranja - Improdutivo */

/* Confiança */
--high-confidence: #4caf50      /* Verde - ≥90% */
--medium-confidence: #ff9800    /* Laranja - 70-89% */
--low-confidence: #f44336       /* Vermelho - <70% */
```

### Componentes UI
- **Cards com Elevation**: Material Design
- **Linear Progress**: Barras de confiança
- **Chips**: Tags de classificação e método
- **Tabs**: Alternância texto/arquivo
- **Badges**: Indicadores de escolha

## 🚀 Como Executar

### Pré-requisitos
- Node.js 16 ou superior
- npm ou yarn
- Backend da API rodando em `http://localhost:8000`

### Instalação
```bash
# Clone o repositório e navegue para o frontend
cd frontend

# Instale as dependências
npm install
```

### Execução
```bash
# Desenvolvimento (com hot reload)
npm start
# Aplicação disponível em: http://localhost:3000

# Build de produção
npm run build

# Teste da build local
npx serve -s build
```

## 🧪 Como Testar

### Teste Manual
1. **Inicie o backend** (necessário para API)
2. **Execute `npm start`**
3. **Acesse http://localhost:3000**

### Casos de Teste

#### Emails Produtivos (devem aparecer em verde)
```
"Preciso urgentemente do relatório mensal. Pode me enviar até amanhã?"
"Podemos marcar uma reunião para discutir o projeto?"
"Qual é o prazo para entrega da proposta?"
```

#### Emails Improdutivos (devem aparecer em laranja)
```
"Muito obrigado pela ajuda de hoje!"
"Feliz aniversário! Desejo muito sucesso!"
"Bom fim de semana para todos!"
```

### Validação de Interface
- ✅ **Validação de Texto**: 10-5000 caracteres
- ✅ **Validação de Arquivo**: Máximo 10MB, apenas .txt/.pdf
- ✅ **Estados de Loading**: Spinner durante classificação
- ✅ **Tratamento de Erro**: Mensagens claras de erro
- ✅ **Responsividade**: Layout adaptativo mobile/desktop

## 🧪 Testes Automatizados

### Executar Testes
```bash
# Testes unitários
npm test

# Testes com cobertura
npm test -- --coverage

# Verificação de tipos TypeScript
npx tsc --noEmit
```

### Estrutura de Testes
- **Componentes**: Renderização e interação
- **Services**: Chamadas de API e validação
- **Types**: Verificação de interfaces

## 📊 Análise Comparativa - Como Funciona

### 1. Interface Dual
```
┌─────────────────┬─────────────────┐
│   NLP Method    │  Gemini Method  │
├─────────────────┼─────────────────┤
│ 🏆 Badge se     │ 🏆 Badge se     │
│    escolhido    │    escolhido    │
├─────────────────┼─────────────────┤
│ 📊 Confiança    │ 📊 Confiança    │
│ 💭 Raciocínio   │ 💭 Raciocínio   │
└─────────────────┴─────────────────┘
```

### 2. Indicadores Visuais
- **🟢 Borda Verde**: Método com maior confiança
- **🔵 Borda Azul**: Gemini escolhido
- **🟣 Borda Roxa**: NLP escolhido
- **📊 Barras**: Verde (>90%), Amarelo (70-90%), Vermelho (<70%)

### 3. Decisão Final
```
✅ Métodos concordam → Maior confiança
❌ Métodos divergem → Critério híbrido
📋 Resumo explicativo sempre visível
```

## ⚡ Performance

### Otimizações Implementadas
- **Lazy Loading**: Componentes carregados sob demanda
- **React.memo**: Memoização de componentes pesados
- **Bundle Splitting**: Divisão automática do código
- **Tree Shaking**: Remoção de código não utilizado

### Métricas Target
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **Bundle Size**: <500KB gzipped

## 🔧 Configuração

### Variáveis de Ambiente (opcional)
```bash
# .env.local
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MAX_FILE_SIZE=10485760  # 10MB
```

### Scripts Disponíveis
```bash
npm start          # Desenvolvimento
npm run build      # Build produção
npm test           # Testes
npm run eject      # Ejetar CRA (não recomendado)
```

---

**Versão**: v1.0 | **Última atualização**: Set 2025
