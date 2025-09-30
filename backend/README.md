# 🚀 Email Classifier - Backend

API REST construída com **FastAPI** para classificação inteligente de emails usando **sistema híbrido NLP + Gemini AI**.

## 📋 Funcionalidades

- **🤖 Classificação Híbrida**: Combina NLP tradicional com Gemini AI para maior precisão
- **📊 Análise Comparativa**: Mostra resultados de ambos os métodos e critério de decisão
- **📧 Múltiplos Formatos**: Aceita texto direto e arquivos (.txt, .pdf)
- **🔍 Transparência Total**: Justificativas detalhadas para cada classificação
- **⚡ Alta Performance**: Respostas otimizadas com cache e processamento assíncrono

## 🏗️ Arquitetura

```
backend/
├── app/
│   ├── main.py                 # Servidor FastAPI + configuração CORS
│   ├── classifier.py           # Endpoints da API
│   ├── nlp_preprocessor.py     # Sistema NLP tradicional (NLTK)
│   ├── gemini_classifier.py    # Sistema híbrido + análise comparativa
│   └── nlp_utils.py           # Utilitários para processamento de texto
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente (GOOGLE_API_KEY)
├── Dockerfile                 # Container para deploy
└── render.yaml               # Configuração para deploy no Render
```

## 🛠️ Tecnologias

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| **Framework** | FastAPI | 0.104+ |
| **IA Generativa** | Gemini 2.5-flash | Latest |
| **NLP Tradicional** | NLTK | 3.8+ |
| **HTTP Client** | httpx | 0.25+ |
| **Servidor** | uvicorn | 0.24+ |
| **Processamento** | PyPDF2, python-multipart | Latest |

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.9+
- Chave API do Google Gemini

### 1. Configuração do Ambiente
```bash
# Clone e acesse o backend
cd backend

# Instale as dependências
pip install -r requirements.txt

# Configure a variável de ambiente
echo "GOOGLE_API_KEY=sua_chave_gemini_aqui" > .env
```

### 2. Execução Local
```bash
# Desenvolvimento (com hot reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Produção
python -m app.main
```

A API estará disponível em: `http://localhost:8000`

### 3. Documentação da API
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📡 Endpoints da API

### `POST /classify-text`
Classifica texto de email diretamente.

**Request:**
```json
{
  "text": "Preciso urgentemente do relatório mensal. Pode me enviar até amanhã?"
}
```

**Response:**
```json
{
  "categoria": "Produtivo",
  "confidence": 0.92,
  "metodo_usado": "gemini",
  "resposta_sugerida": "Claro! Vou preparar o relatório e enviar até amanhã.",
  "detalhes": {
    "justificativa": "Email produtivo com solicitação clara e prazo definido",
    "tempo_processamento": "1.2s",
    "modelo": "gemini-2.5-flash",
    "versao": "v4.0",
    "analise_comparativa": {
      "nlp_resultado": {
        "classificacao": "Produtivo",
        "confianca": 0.85,
        "features": {
          "productive_keywords": 2,
          "unproductive_keywords": 0,
          "has_urgency": true,
          "has_questions": true
        },
        "raciocinio": "Detectadas palavras-chave produtivas e indicadores de urgência"
      },
      "gemini_resultado": {
        "classificacao": "Produtivo",
        "confianca": 0.92,
        "raciocinio": "Email com solicitação específica e prazo definido"
      },
      "concordancia": {
        "concordam": true,
        "status": "Métodos concordam na classificação",
        "criterio_decisao": "maior_confianca"
      }
    }
  }
}
```

### `POST /classify-file`
Classifica email a partir de arquivo (.txt ou .pdf).

**Request:**
```bash
curl -X POST "http://localhost:8000/classify-file" \
  -F "file=@email.txt"
```

### `GET /health`
Verifica saúde da API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-29T10:30:00Z",
  "services": {
    "nlp": "✅ ativo",
    "gemini": "✅ ativo"
  }
}
```

## 🧠 Sistema de Classificação Híbrido

### NLP Tradicional
- **Features**: Palavras-chave, indicadores de urgência, perguntas
- **Algoritmo**: Sistema baseado em regras + análise léxica
- **Vantagens**: Rápido, interpretável, sem dependência externa

### Gemini AI
- **Modelo**: Google Gemini 2.5-flash
- **Capacidades**: Análise contextual, compreensão semântica
- **Vantagens**: Maior precisão em casos complexos

### Lógica de Decisão
```python
if nlp.categoria == gemini.categoria:
    escolher_maior_confianca()
elif gemini.confianca >= 0.8:
    escolher_gemini()  # AI prevalece com alta confiança
else:
    escolher_maior_confianca()
```

## 📊 Métricas e Monitoramento

### Logs Estruturados
```python
# Exemplo de log de classificação
{
  "timestamp": "2025-09-29T10:30:00Z",
  "method": "POST",
  "endpoint": "/classify-text",
  "input_size": 128,
  "processing_time": 1.2,
  "nlp_confidence": 0.85,
  "gemini_confidence": 0.92,
  "chosen_method": "gemini",
  "classification": "Produtivo"
}
```

### Validação de Entrada
- **Texto**: 10-5000 caracteres
- **Arquivo**: Máximo 10MB, formatos .txt/.pdf
- **Rate Limiting**: 100 requests/minuto por IP

## 🐳 Deploy com Docker

### Build da Imagem
```bash
docker build -t email-classifier-backend .
```

### Execução
```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=sua_chave \
  email-classifier-backend
```

## ☁️ Deploy no Render

### Configuração Automática
O arquivo `render.yaml` já está configurado:

```yaml
services:
  - type: web
    name: email-classifier-api
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GOOGLE_API_KEY
        sync: false  # Configurar manualmente no dashboard
```

### Deploy Manual
1. Conecte seu repositório no [Render](https://render.com)
2. Configure a variável `GOOGLE_API_KEY` no dashboard
3. Deploy automático a cada push

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
```bash
# Obrigatórias
GOOGLE_API_KEY=your_gemini_api_key

# Opcionais
NLP_CONFIDENCE_THRESHOLD=0.7
GEMINI_CONFIDENCE_THRESHOLD=0.8
MAX_FILE_SIZE_MB=10
ENABLE_CORS=true
```

### Performance Tuning
```python
# app/main.py
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    workers=4,          # Múltiplos workers
    access_log=False,   # Desabilitar logs de acesso
    reload=False        # Produção
)
```

## 🧪 Testes e Validação

### Teste de Saúde
```bash
curl http://localhost:8000/health
```

### Teste de Classificação
```bash
# Texto produtivo
curl -X POST "http://localhost:8000/classify-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Reunião importante às 14h sobre projeto"}'

# Texto improdutivo  
curl -X POST "http://localhost:8000/classify-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Oi, tudo bem? Como foi o fim de semana?"}'
```

## 📈 Análise de Performance

### Benchmarks Típicos
- **Classificação simples**: ~500-800ms
- **Análise comparativa**: ~1000-1500ms
- **Processamento de arquivo**: ~2000-3000ms
- **Throughput**: ~50-80 requests/segundo

### Otimizações Implementadas
- ✅ Cache de modelos NLP
- ✅ Processamento assíncrono
- ✅ Validação rápida de entrada
- ✅ Compressão de respostas
- ✅ Pool de conexões HTTP

## 🛡️ Segurança

### Práticas Implementadas
- **CORS** configurado para domínios específicos
- **Rate Limiting** por IP
- **Validação rigorosa** de entrada
- **Sanitização** de arquivos upload
- **Headers de segurança** HTTP

### Considerações
- Chave API do Gemini deve ser mantida segura
- Logs não devem conter dados sensíveis
- HTTPS obrigatório em produção

## 🤝 Contribuição

### Estrutura de Desenvolvimento
```bash
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point + configuração
│   ├── classifier.py        # Controllers/Endpoints
│   ├── nlp_preprocessor.py  # Serviço NLP
│   ├── gemini_classifier.py # Serviço Gemini + Híbrido
│   └── nlp_utils.py        # Utilitários
└── tests/                   # Testes unitários (futuro)
```

### Padrões de Código
- **PEP 8** para estilo Python
- **Type hints** obrigatórios
- **Docstrings** para funções públicas
- **Logs estruturados** para debugging

---

## 📞 Suporte

Para dúvidas sobre o backend:
- 📧 Logs detalhados em `/health`
- 🐛 Issues no repositório
- 📖 Documentação automática em `/docs`

**Versão**: v1.0 | **Status**: Produção | **Última atualização**: Set 2025