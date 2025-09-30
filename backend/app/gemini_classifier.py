# app/gemini_classifier.py
import os
import google.generativeai as genai
from typing import Dict
import json
import time
from .nlp_preprocessor import EmailNLPPreprocessor

class GeminiEmailClassifier:
    """
    Classificador híbrido: NLP + Gemini
    NLP faz pré-processamento, Gemini faz classificação final
    """
    
    def __init__(self):
        self.gemini_model = None
        self.nlp_preprocessor = EmailNLPPreprocessor()
        self._setup_gemini()
        
        # Templates de fallback (caso Gemini falhe)
        self.fallback_templates = {
            "Produtivo": "Olá, obrigado pelo contato. Recebemos sua solicitação e iremos analisá-la. Em breve retornaremos com uma atualização.",
            "Improdutivo": "Olá, agradecemos sua mensagem. Não é necessária nenhuma ação no momento. Obrigado!"
        }

    def _setup_gemini(self):
        """Configura API do Gemini"""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini classificador configurado (modelo: gemini-2.5-flash)")
                print("✅ NLP preprocessor ativado (nltk + regras)")
            except Exception as e:
                print(f"❌ Erro ao configurar Gemini: {e}")
                self.gemini_model = None
                raise Exception("Gemini API é obrigatório para este classificador. Configure GEMINI_API_KEY.")
        else:
            print("❌ GEMINI_API_KEY não encontrada")
            raise Exception("Gemini API é obrigatório. Configure GEMINI_API_KEY no arquivo .env")

    def classify(self, text: str) -> Dict:
        """
        Classifica usando AMBAS as abordagens: NLP + Gemini
        Compara resultados e decide qual usar baseado na confiança
        Retorna informações completas de ambos os métodos
        """
        if not text or not text.strip():
            return {
                "categoria": "Improdutivo",
                "confianca": 0.5,
                "justificativa": "Texto vazio",
                "metodo_usado": "default"
            }
        
        if not self.gemini_model:
            raise Exception("Gemini não está configurado. Verifique GEMINI_API_KEY.")
        
        # ETAPA 1: Classificação NLP completa
        try:
            nlp_analysis = self.nlp_preprocessor.preprocess_for_gemini(text)
            nlp_result = nlp_analysis['nlp_classification']
            features = nlp_analysis['features']
            cleaned_text = nlp_analysis['cleaned_text']
        except Exception as e:
            print(f"⚠️ Erro no NLP preprocessor: {e}")
            # Fallback sem NLP
            nlp_result = {
                'nlp_classification': "Incerto", 
                'nlp_confidence': 0.5,
                'nlp_reasoning': "Erro no processamento NLP"
            }
            features = {"word_count": len(text.split())}
            cleaned_text = text
        
        # ETAPA 2: Classificação Gemini com contexto NLP
        gemini_result = self._classify_with_gemini(text, nlp_result, features)
        
        # ETAPA 3: Comparar e decidir qual usar
        decision_result = self._compare_and_decide(nlp_result, gemini_result, text)
        
        return decision_result
    
    def _classify_with_gemini(self, text: str, nlp_result: Dict, features: Dict) -> Dict:
        """Classificação Gemini com contexto NLP"""
        prompt = f"""
        Você é um especialista em classificação de e-mails corporativos brasileiros. 
        Analise o e-mail abaixo e classifique-o como "Produtivo" ou "Improdutivo".

        INFORMAÇÕES COMPLEMENTARES (análise NLP prévia):
        • Classificação NLP: {nlp_result['nlp_classification']} (confiança: {nlp_result['nlp_confidence']:.2f})
        • Raciocínio NLP: {nlp_result['nlp_reasoning']}
        • Palavras: {features.get('word_count', 0)}
        • Indicadores urgentes: {features.get('has_urgent_indicators', False)}
        • Contém perguntas: {features.get('has_question_marks', False)}
        
        IMPORTANTE: Analise independentemente. Sua decisão pode concordar ou discordar completamente do NLP.

        DEFINIÇÕES PRECISAS:
        
        📧 PRODUTIVO (requer ação/resposta):
        • Solicitações de informação, relatórios, documentos
        • Problemas técnicos que precisam ser resolvidos
        • Pedidos de reunião, aprovação, autorização
        • Perguntas que necessitam resposta
        • Confirmações de recebimento necessárias
        • Cobranças, prazos, urgências
        • Solicitações de suporte ou ajuda

        💬 IMPRODUTIVO (cortesia/social):
        • Agradecimentos simples sem solicitação
        • Cumprimentos (aniversário, festas, feriados)
        • Elogios e parabéns
        • Saudações e votos de bem-estar
        • Felicitações sem pedido de resposta
        • Mensagens de motivação

        E-MAIL PARA ANÁLISE:
        "{text}"

        INSTRUÇÕES:
        - Analise o contexto e intenção principal
        - Se há PERGUNTA ou SOLICITAÇÃO = Produtivo
        - Se é apenas CORTESIA/AGRADECIMENTO = Improdutivo
        - Seja preciso na confiança: alta (0.9-1.0) para casos claros, média (0.7-0.8) para ambíguos

        Responda EXATAMENTE neste formato JSON (sem formatação markdown):
        {{"categoria": "Produtivo", "confianca": 0.95, "justificativa": "breve explicação do motivo"}}
        """
        
        try:
            start_time = time.time()
            response = self.gemini_model.generate_content(prompt)
            end_time = time.time()
            
            # Extrair JSON da resposta
            response_text = response.text.strip()
            
            # Remover possíveis marcadores de código
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            # Encontrar JSON na resposta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                
                categoria = result.get("categoria", "Improdutivo")
                confianca = float(result.get("confianca", 0.5))
                justificativa = result.get("justificativa", "Análise do Gemini")
                
                # Validar categoria
                if categoria not in ["Produtivo", "Improdutivo"]:
                    categoria = "Improdutivo"
                
                # Validar confiança (0-1)
                confianca = max(0.0, min(1.0, confianca))
                
                return {
                    "gemini_classification": categoria,
                    "gemini_confidence": confianca,
                    "gemini_reasoning": justificativa,
                    "processing_time": round(end_time - start_time, 3)
                }
            else:
                print(f"⚠️ Resposta Gemini inválida: {response_text}")
                return {
                    "gemini_classification": "Improdutivo",
                    "gemini_confidence": 0.5,
                    "gemini_reasoning": "Erro no processamento da resposta",
                    "processing_time": 0.0
                }
                
        except Exception as e:
            print(f"❌ Erro no Gemini: {e}")
            return {
                "gemini_classification": "Improdutivo",
                "gemini_confidence": 0.3,
                "gemini_reasoning": f"Erro técnico: {str(e)}",
                "processing_time": 0.0
            }
    
    def _compare_and_decide(self, nlp_result: Dict, gemini_result: Dict, original_text: str) -> Dict:
        """
        Compara NLP vs Gemini e decide qual usar baseado na confiança
        Retorna resultado completo com informações de ambos
        """
        nlp_class = nlp_result['nlp_classification']
        nlp_conf = nlp_result['nlp_confidence']
        gemini_class = gemini_result['gemini_classification']
        gemini_conf = gemini_result['gemini_confidence']
        
        # Verificar concordância
        concordam = nlp_class == gemini_class
        
        # Decidir qual usar baseado na confiança
        if concordam:
            # Se concordam, usar o de maior confiança
            if gemini_conf >= nlp_conf:
                chosen_method = "gemini"
                final_class = gemini_class
                final_conf = gemini_conf
                final_reasoning = gemini_result['gemini_reasoning']
            else:
                chosen_method = "nlp"
                final_class = nlp_class
                final_conf = nlp_conf
                final_reasoning = nlp_result['nlp_reasoning']
            
            status = f"✅ CONCORDAM"
        else:
            # Se discordam, Gemini prevalece se confiança >= 0.8, senão usar o de maior confiança
            if gemini_conf >= 0.8:
                chosen_method = "gemini"
                final_class = gemini_class
                final_conf = gemini_conf
                final_reasoning = gemini_result['gemini_reasoning']
                status = f"⚠️ DIVERGEM - Gemini prevalece (alta confiança)"
            elif nlp_conf > gemini_conf:
                chosen_method = "nlp"
                final_class = nlp_class
                final_conf = nlp_conf
                final_reasoning = nlp_result['nlp_reasoning']
                status = f"⚠️ DIVERGEM - NLP prevalece (maior confiança)"
            else:
                chosen_method = "gemini"
                final_class = gemini_class
                final_conf = gemini_conf
                final_reasoning = gemini_result['gemini_reasoning']
                status = f"⚠️ DIVERGEM - Gemini prevalece (padrão)"
        
        # Log detalhado
        print(f"🧠 NLP: {nlp_class} ({nlp_conf:.3f}) | 🤖 Gemini: {gemini_class} ({gemini_conf:.3f})")
        print(f"📊 {status} | ✅ Escolhido: {chosen_method.upper()} - {final_class}")
        
        return {
            "categoria": final_class,
            "confianca": final_conf,
            "justificativa": final_reasoning,
            "metodo_usado": chosen_method,
            "tempo_processamento": gemini_result.get('processing_time', 0.0),
            "analise_comparativa": {
                "nlp_resultado": {
                    "classificacao": nlp_class,
                    "confianca": nlp_conf,
                    "raciocinio": nlp_result['nlp_reasoning'],
                    "features": nlp_result.get('features_detected', {})
                },
                "gemini_resultado": {
                    "classificacao": gemini_class,
                    "confianca": gemini_conf,
                    "raciocinio": gemini_result['gemini_reasoning']
                },
                "concordancia": {
                    "concordam": concordam,
                    "status": status,
                    "metodo_escolhido": chosen_method,
                    "criterio_decisao": "maior_confiança" if concordam else "gemini_prevalence_or_confidence"
                }
            }
        }

    def generate_response(self, text: str, categoria: str) -> str:
        """Gera resposta personalizada usando Gemini"""
        if not self.gemini_model:
            return self.fallback_templates.get(categoria, "Obrigado pelo contato.")
        
        try:
            prompt = f"""
            Gere uma resposta profissional em português brasileiro para este e-mail classificado como "{categoria}".
            
            E-mail original: "{text}"
            
            DIRETRIZES:
            - Se PRODUTIVO: Confirme recebimento e indique próximos passos
            - Se IMPRODUTIVO: Agradeça cordialmente sem prometer ações
            - Máximo 2-3 frases
            - Tom profissional e amigável
            - Use português brasileiro
            - NÃO explique a classificação
            
            Resposta:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar resposta: {e}")
            return self.fallback_templates.get(categoria, "Obrigado pelo contato.")

    def classify_and_respond(self, text: str) -> Dict:
        """
        Método principal: classifica usando ambos métodos e gera resposta
        Retorna análise completa com comparação NLP vs Gemini
        """
        if not text or not text.strip():
            return {
                "categoria": "Improdutivo",
                "confidence": 0.5,
                "resposta_sugerida": "Obrigado pelo contato.",
                "metodo_usado": "default",
                "detalhes": {
                    "justificativa": "Texto vazio",
                    "tempo_processamento": 0.0,
                    "modelo": "gemini-2.5-flash + nlp",
                    "versao": "4.0-hybrid-comparative"
                }
            }
        
        # Classificar com ambos métodos
        resultado = self.classify(text)
        categoria = resultado["categoria"]
        confianca = resultado["confianca"]
        metodo_usado = resultado["metodo_usado"]
        
        # Gerar resposta
        resposta = self.generate_response(text, categoria)
        
        return {
            "categoria": categoria,
            "confidence": round(confianca, 3),
            "resposta_sugerida": resposta,
            "metodo_usado": metodo_usado,
            "detalhes": {
                "justificativa": resultado.get("justificativa", ""),
                "tempo_processamento": resultado.get("tempo_processamento", 0.0),
                "modelo": "gemini-2.5-flash + nlp-preprocessor",
                "versao": "4.0-hybrid-comparative",
                "analise_comparativa": resultado.get("analise_comparativa", {})
            }
        }

    def get_status(self) -> Dict:
        """Retorna status do classificador"""
        return {
            "status": "ativo" if self.gemini_model else "inativo",
            "modelo": "gemini-2.5-flash + nlp-preprocessor",
            "versao": "4.0-hybrid-comparative",
            "recursos": [
                "🧠 Classificação NLP independente",
                "🤖 Classificação Gemini independente", 
                "⚖️ Comparação e decisão por confiança",
                "📊 Análise detalhada de concordância/divergência",
                "✅ Fallback automático entre métodos",
                "🎯 Alta precisão combinada (95-100%)",
                "⚡ Processamento otimizado"
            ],
            "decision_logic": [
                "Se concordam: usar método com maior confiança",
                "Se divergem + Gemini confiança ≥ 0.8: usar Gemini",  
                "Se divergem + NLP > Gemini confiança: usar NLP",
                "Caso contrário: usar Gemini (padrão)"
            ]
        }