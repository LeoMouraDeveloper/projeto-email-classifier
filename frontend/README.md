# 🎨 Email Classifier - Frontend

Interface moderna em **React + TypeScript** com análise comparativa visual entre **NLP** e **Gemini AI**.

## 🎯 Funcionalidades

- **📝 Input Múltiplo**: Texto direto ou upload de arquivos (.txt/.pdf)
- ** Análise Dual**: Comparação visual NLP vs Gemini lado a lado
- **🏆 Decisão Transparente**: Indicação clara do método escolhido
- **� 100% Responsivo**: Mobile-first design
- **⚡ Tempo Real**: Feedback instantâneo com loading states

## 🏗️ Arquitetura

```
src/
├── components/
│   ├── EmailClassifier.tsx       # Interface principal
│   └── ComparisonAnalysis.tsx    # Análise comparativa
├── services/
│   └── emailClassifierService.ts # Cliente API
├── types/
│   └── index.ts                  # TypeScript interfaces
└── App.tsx                       # Root component
```

## 🚀 Quick Start

```bash
# 1. Instalar dependências
cd frontend
npm install

# 2. Configurar API (opcional)
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local

# 3. Executar aplicação
npm start

# 4. Acessar interface
# http://localhost:3000
```

**📋 Pré-requisito**: Backend rodando em `http://localhost:8000`

## 🎨 Interface Visual

### **Entrada de Dados**
- 📝 **Tab Texto**: Área para colar email (10-5000 chars)
- 📎 **Tab Arquivo**: Upload drag-and-drop (máx 10MB)
- ✅ **Validação**: Feedback em tempo real

### **Análise Comparativa**
```
┌─────────────────┬─────────────────┐
│   🧠 NLP        │   🤖 Gemini     │
├─────────────────┼─────────────────┤
│ 🏆 Escolhido se │ 🏆 Escolhido se │
│ ■■■■■■■ 85%     │ ■■■■■■■■ 92%    │
│ "Palavras-chave │ "Solicitação    │
│  produtivas"    │  específica"    │
└─────────────────┴─────────────────┘
```

### **Resultado Final**
- 🎯 **Classificação**: Produtivo (verde) / Improdutivo (laranja)
- 📊 **Confiança**: Barra colorida com percentual
- � **Justificativa**: Explicação do método escolhido
- 📝 **Resposta Sugerida**: Texto gerado automaticamente

## 🛠️ Stack Tecnológico

| Componente | Tecnologia |
|------------|------------|
| **Framework** | React 18.2+ |
| **Linguagem** | TypeScript 4.9+ |
| **UI Library** | Material-UI 5.14+ |
| **HTTP Client** | Axios 1.6+ |
| **Build Tool** | Create React App |
| **Deploy** | Vercel |

## 📱 Componentes

### **EmailClassifier.tsx**
```typescript
// Interface principal
- Estado de loading/erro
- Tabs texto/arquivo
- Validação de entrada
- Exibição de resultados
```

### **ComparisonAnalysis.tsx**
```typescript
// Análise comparativa
- Layout lado a lado
- Badges de método escolhido
- Barras de confiança
- Detalhes de raciocínio
```

### **emailClassifierService.ts**
```typescript
// Service layer
- Integração com API REST
- Tratamento de erros
- Tipagem completa
- Timeout 60s (Render cold start)
```

## 🎨 Design System

### **Cores**
```css
/* Classificação */
--produtivo: #4caf50    /* Verde */
--improdutivo: #ff9800  /* Laranja */

/* Métodos */
--gemini: #2196f3       /* Azul */
--nlp: #9c27b0          /* Roxo */

/* Confiança */
--alta: #4caf50         /* ≥90% */
--media: #ff9800        /* 70-89% */
--baixa: #f44336        /* <70% */
```

### **Componentes UI**
- **Material Cards**: Elevation e sombras
- **Progress Bars**: Indicadores de confiança
- **Chips**: Tags de classificação
- **Badges**: Método escolhido
- **Tabs**: Alternância input

## 🧪 Como Testar

### **Casos de Teste**

**✅ Produtivos:**
```
"Preciso urgentemente do relatório mensal"
"Podemos marcar reunião para segunda?"
"Qual o prazo para entrega?"
```

**❌ Improdutivos:**
```
"Obrigado pela ajuda de hoje!"
"Feliz aniversário! 🎉"
"Bom fim de semana!"
```

### **Validações**
- 📝 Texto: 10-5000 caracteres
- 📎 Arquivo: Máx 10MB, .txt/.pdf apenas
- ⚡ Loading: Spinner durante análise
- 🚨 Erro: Mensagens claras de falha

## 🚀 Deploy

### **Local**
```bash
npm install
npm start          # http://localhost:3000
npm run build      # Build produção
```

### **Vercel (Produção)**
1. Conecte repositório no [Vercel](https://vercel.com)
2. Configure `REACT_APP_API_URL` se necessário
3. Deploy automático via `vercel.json`

**🌐 Produção**: https://projeto-email-classifier-8poe.vercel.app

## 📊 Performance

### **Otimizações**
- ✅ **Code Splitting**: Divisão automática
- ✅ **Tree Shaking**: Remoção de código morto
- ✅ **React.memo**: Memoização de componentes
- ✅ **Lazy Loading**: Carregamento sob demanda

### **Métricas**
- **Bundle Size**: < 500KB gzipped
- **FCP**: < 1.5s
- **LCP**: < 2.5s
- **TTI**: < 3s

## 🔧 Configuração

### **Variáveis Ambiente**
```bash
# .env.local (opcional)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MAX_FILE_SIZE=10485760
REACT_APP_TIMEOUT=60000
```

### **Scripts NPM**
```bash
npm start          # Desenvolvimento
npm run build      # Build produção  
npm test           # Testes unitários
npm run eject      # Ejetar CRA (cuidado!)
```

## 📈 Monitoramento

### **Analytics Frontend**
- Tempo de resposta da API
- Taxa de sucesso nas classificações
- Uso de método (texto vs arquivo)
- Distribuição de classificações

### **Error Tracking**
- Falhas de rede
- Timeouts da API
- Erros de validação
- Problemas de upload

## 🧪 Testes

```bash
# Testes unitários
npm test

# Testes com cobertura
npm test -- --coverage

# Type checking
npx tsc --noEmit
```

### **Cobertura Target**
- Componentes: >80%
- Services: >90%
- Utils: >95%

---

## 📞 Suporte

- **🌐 Demo**: https://projeto-email-classifier-8poe.vercel.app
- **📖 Storybook**: Em desenvolvimento
- **🐛 Issues**: Repositório GitHub
- **📊 Analytics**: Vercel dashboard

**📅 Versão**: 1.0 | **🚀 Status**: Produção | **📱 Mobile**: 100% compatível
