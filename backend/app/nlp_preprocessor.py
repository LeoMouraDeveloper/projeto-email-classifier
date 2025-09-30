# app/nlp_preprocessor.py
import re
import string
from typing import Dict, List

# Tentar importar NLTK, mas funcionar sem ele se necessário
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    
    # Download necessário (executar uma vez)
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        NLTK_AVAILABLE = True
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            NLTK_AVAILABLE = True
        except:
            print("⚠️ NLTK não disponível, usando fallback simples")
            NLTK_AVAILABLE = False
except ImportError:
    print("⚠️ NLTK não instalado, usando fallback simples")
    NLTK_AVAILABLE = False

class EmailNLPPreprocessor:
    """
    Pré-processador NLP para emails - COMPLEMENTA o Gemini
    Não substitui, apenas enriquece a análise
    """
    
    def __init__(self):
        # Configurar stop words com fallback
        if NLTK_AVAILABLE:
            try:
                self.stop_words = set(stopwords.words('portuguese'))
                self.stop_words.update(stopwords.words('english'))
            except:
                self.stop_words = self._get_fallback_stopwords()
        else:
            self.stop_words = self._get_fallback_stopwords()
        
        # Palavras-chave para classificação rápida
        self.productive_keywords = {
            'urgente', 'prazo', 'solicitação', 'dúvida', 'problema', 
            'erro', 'ajuda', 'suporte', 'necessário', 'importante',
            'relatório', 'reunião', 'projeto', 'status', 'atualização',
            'confirmar', 'autorizar', 'aprovar', 'revisar', 'verificar'
        }
        
        self.unproductive_keywords = {
            'obrigado', 'parabéns', 'feliz', 'aniversário', 'natal', 
            'ano novo', 'feriado', 'desculpa', 'agradecimento', 'elogio',
            'congratulações', 'felicitações', 'sucesso', 'conquista'
        }
    
    def _get_fallback_stopwords(self) -> set:
        """Stopwords básicas em português e inglês"""
        return {
            'a', 'o', 'e', 'de', 'da', 'do', 'que', 'em', 'um', 'uma', 'para', 'com', 'não', 'se', 'na', 'por', 'mais', 'as', 'os', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas', 'porque', 'assim', 'pode', 'foram', 'estar', 'sobre', 'então', 'outro', 'outro', 'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from'
        }
    
    def _simple_tokenize(self, text: str) -> List[str]:
        """Tokenização simples sem NLTK"""
        # Remover pontuação e converter para minúsculas
        text = re.sub(r'[^\w\s\u00C0-\u017F]', ' ', text.lower())
        return text.split()

    def clean_text(self, text: str) -> str:
        """Limpa e normaliza o texto"""
        if not text:
            return ""
        
        # Remover HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Remover caracteres especiais mantendo acentos
        text = re.sub(r'[^\w\s\u00C0-\u017F]', ' ', text)
        
        # Normalizar espaços
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip().lower()

    def extract_features(self, text: str) -> Dict:
        """Extrai features do texto para análise complementar"""
        cleaned = self.clean_text(text)
        
        # Tokenização com ou sem NLTK
        if NLTK_AVAILABLE:
            try:
                tokens = word_tokenize(cleaned, language='portuguese')
            except:
                tokens = self._simple_tokenize(cleaned)
        else:
            tokens = self._simple_tokenize(cleaned)
        
        # Remover stop words
        meaningful_words = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        
        # Calcular features
        features = {
            'word_count': len(tokens),
            'char_count': len(text),
            'meaningful_words': len(meaningful_words),
            'avg_word_length': sum(len(word) for word in meaningful_words) / max(len(meaningful_words), 1),
            'has_urgent_indicators': any(word in cleaned for word in ['urgente', 'importante', 'prazo']),
            'has_question_marks': '?' in text,
            'has_exclamation': '!' in text,
            'productive_score': 0,
            'unproductive_score': 0
        }
        
        # Score baseado em palavras-chave
        for word in meaningful_words:
            if word in self.productive_keywords:
                features['productive_score'] += 1
            if word in self.unproductive_keywords:
                features['unproductive_score'] += 1
        
        return features

    def classify_with_nlp(self, text: str) -> Dict:
        """
        Classificação completa NLP com confiança calculada
        Agora retorna classificação real, não apenas hint
        """
        features = self.extract_features(text)
        
        # Calcular scores normalizados
        productive_indicators = features['productive_score']
        unproductive_indicators = features['unproductive_score']
        total_indicators = productive_indicators + unproductive_indicators
        
        # Regras de classificação NLP melhoradas
        base_confidence = 0.6  # Confiança base do NLP
        
        # Casos claros
        if features['has_urgent_indicators'] or features['has_question_marks']:
            classification = "Produtivo"
            confidence = min(0.85, base_confidence + 0.2 + (productive_indicators * 0.05))
        elif productive_indicators >= 2 and unproductive_indicators == 0:
            classification = "Produtivo"
            confidence = min(0.80, base_confidence + (productive_indicators * 0.05))
        elif unproductive_indicators >= 2 and productive_indicators == 0:
            classification = "Improdutivo"
            confidence = min(0.80, base_confidence + (unproductive_indicators * 0.05))
        elif productive_indicators > unproductive_indicators and productive_indicators > 0:
            classification = "Produtivo"
            confidence = min(0.75, base_confidence + ((productive_indicators - unproductive_indicators) * 0.05))
        elif unproductive_indicators > productive_indicators and unproductive_indicators > 0:
            classification = "Improdutivo"
            confidence = min(0.75, base_confidence + ((unproductive_indicators - productive_indicators) * 0.05))
        else:
            # Caso ambíguo - usar comprimento e estrutura
            if features['word_count'] < 10 and not features['has_question_marks']:
                classification = "Improdutivo"
                confidence = 0.65
            elif features['word_count'] > 20 and features['has_question_marks']:
                classification = "Produtivo"
                confidence = 0.70
            else:
                classification = "Improdutivo"  # Default conservador
                confidence = 0.55
        
        return {
            'nlp_classification': classification,
            'nlp_confidence': round(confidence, 3),
            'nlp_reasoning': self._generate_nlp_reasoning(features, classification),
            'features_detected': {
                'productive_keywords': productive_indicators,
                'unproductive_keywords': unproductive_indicators,
                'has_urgency': features['has_urgent_indicators'],
                'has_questions': features['has_question_marks'],
                'word_count': features['word_count']
            }
        }
    
    def _generate_nlp_reasoning(self, features: Dict, classification: str) -> str:
        """Gera explicação da decisão NLP"""
        reasons = []
        
        if features['has_urgent_indicators']:
            reasons.append("detectou indicadores de urgência")
        if features['has_question_marks']:
            reasons.append("contém perguntas diretas")
        if features['productive_score'] > 0:
            reasons.append(f"encontrou {features['productive_score']} palavras-chave produtivas")
        if features['unproductive_score'] > 0:
            reasons.append(f"encontrou {features['unproductive_score']} palavras-chave improdutivas")
        
        if not reasons:
            reasons.append("baseado na análise estrutural do texto")
        
        return f"NLP classificou como {classification} porque " + " e ".join(reasons)

    def preprocess_for_gemini(self, text: str) -> Dict:
        """
        Prepara texto para envio ao Gemini com classificação NLP completa
        """
        cleaned_text = self.clean_text(text)
        features = self.extract_features(text)
        nlp_result = self.classify_with_nlp(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'features': features,
            'nlp_classification': nlp_result,
            'ready_for_gemini': True
        }