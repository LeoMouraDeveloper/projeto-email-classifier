// Types para o Email Classifier Frontend

export interface EmailClassificationRequest {
  text: string;
  file?: File | null;
}

export interface NLPResult {
  classificacao: 'Produtivo' | 'Improdutivo';
  confianca: number;
  raciocinio: string;
  features: {
    productive_keywords: number;
    unproductive_keywords: number;
    has_urgency: boolean;
    has_questions: boolean;
    word_count: number;
  };
}

export interface GeminiResult {
  classificacao: 'Produtivo' | 'Improdutivo';
  confianca: number;
  raciocinio: string;
}

export interface ComparativeAnalysis {
  nlp_resultado: NLPResult;
  gemini_resultado: GeminiResult;
  concordancia: {
    concordam: boolean;
    status: string;
    metodo_escolhido: 'nlp' | 'gemini';
    criterio_decisao: string;
  };
}

export interface EmailClassificationResponse {
  categoria: 'Produtivo' | 'Improdutivo';
  confidence: number;
  resposta_sugerida: string;
  metodo_usado: 'nlp' | 'gemini' | 'default';
  detalhes: {
    justificativa: string;
    tempo_processamento: number;
    modelo: string;
    versao: string;
    analise_comparativa?: ComparativeAnalysis;
  };
}

export interface ApiError {
  message: string;
  detail?: string;
}

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

export interface ClassificationResult extends EmailClassificationResponse {
  timestamp: number;
  input_text: string;
}