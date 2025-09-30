import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  Divider,
  Stack,
  Paper,
  Badge,
} from '@mui/material';
import {
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  Psychology as NlpIcon,
  AutoAwesome as GeminiIcon,
} from '@mui/icons-material';
import { ComparativeAnalysis } from '../types';

interface ComparisonAnalysisProps {
  analysis: ComparativeAnalysis;
  chosenMethod: 'nlp' | 'gemini';
}

const ComparisonAnalysis: React.FC<ComparisonAnalysisProps> = ({ 
  analysis, 
  chosenMethod 
}) => {
  const { nlp_resultado, gemini_resultado, concordancia } = analysis;
  
  // Função para obter cor baseada na categoria
  const getCategoryColor = (category: string): 'success' | 'warning' => {
    return category === 'Produtivo' ? 'success' : 'warning';
  };
  
  // Função para obter cor da confiança
  const getConfidenceColor = (confidence: number): 'success' | 'warning' | 'error' => {
    if (confidence >= 0.9) return 'success';
    if (confidence >= 0.7) return 'warning';
    return 'error';
  };
  
  // Função para formatar porcentagem
  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };
  
  return (
    <Card elevation={3} sx={{ mt: 3, border: '1px solid #e0e0e0' }}>
      <CardContent>
        {/* Cabeçalho da Análise Comparativa */}
        <Box display="flex" alignItems="center" mb={2}>
          <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="h6" component="h3" color="primary">
            Análise Comparativa: NLP vs Gemini
          </Typography>
        </Box>
        
        {/* Status de Concordância */}
        <Paper 
          elevation={1} 
          sx={{ 
            p: 2, 
            mb: 3, 
            backgroundColor: concordancia.concordam ? '#e8f5e8' : '#fff3e0',
            border: `1px solid ${concordancia.concordam ? '#4caf50' : '#ff9800'}`
          }}
        >
          <Box display="flex" alignItems="center" justifyContent="space-between" flexWrap="wrap" gap={1}>
            <Box display="flex" alignItems="center">
              {concordancia.concordam ? (
                <CheckIcon color="success" sx={{ mr: 1 }} />
              ) : (
                <WarningIcon color="warning" sx={{ mr: 1 }} />
              )}
              <Typography variant="body1" fontWeight="bold">
                {concordancia.status}
              </Typography>
            </Box>
            <Chip
              label={`Método Escolhido: ${chosenMethod.toUpperCase()}`}
              color={chosenMethod === 'gemini' ? 'primary' : 'secondary'}
              variant="filled"
              size="small"
            />
          </Box>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Critério: {concordancia.criterio_decisao.replace(/_/g, ' ')}
          </Typography>
        </Paper>
        
        {/* Comparação lado a lado */}
        <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
          {/* Resultado NLP */}
          <Box flex={1}>
            <Paper 
              elevation={2} 
              sx={{ 
                p: 2, 
                height: '100%',
                border: chosenMethod === 'nlp' ? '2px solid #9c27b0' : '1px solid #e0e0e0',
                position: 'relative'
              }}
            >
              {chosenMethod === 'nlp' && (
                <Badge
                  badgeContent="ESCOLHIDO"
                  color="secondary"
                  sx={{
                    position: 'absolute',
                    top: -8,
                    right: 8,
                    '& .MuiBadge-badge': {
                      fontSize: '0.6rem',
                      fontWeight: 'bold'
                    }
                  }}
                />
              )}
              
              <Box display="flex" alignItems="center" mb={2}>
                <NlpIcon color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="secondary">
                  NLP Tradicional
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                {/* Classificação NLP */}
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Classificação
                  </Typography>
                  <Chip
                    label={nlp_resultado.classificacao}
                    color={getCategoryColor(nlp_resultado.classificacao)}
                    variant="filled"
                    size="medium"
                  />
                </Box>
                
                {/* Confiança NLP */}
                <Box>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2" color="text.secondary">
                      Confiança
                    </Typography>
                    <Typography 
                      variant="body2" 
                      fontWeight="bold"
                      color={getConfidenceColor(nlp_resultado.confianca)}
                    >
                      {formatPercentage(nlp_resultado.confianca)}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={nlp_resultado.confianca * 100}
                    color={getConfidenceColor(nlp_resultado.confianca)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                
                {/* Features NLP */}
                <Box>
                  <Typography variant="body2" color="text.secondary" mb={1}>
                    Features Detectadas
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={0.5}>
                    <Typography variant="caption">
                      Palavras Produtivas: {nlp_resultado.features.productive_keywords}
                    </Typography>
                    <Typography variant="caption">
                      Palavras Improdutivas: {nlp_resultado.features.unproductive_keywords}
                    </Typography>
                    <Typography variant="caption">
                      Urgência: {nlp_resultado.features.has_urgency ? 'Sim' : 'Não'}
                    </Typography>
                    <Typography variant="caption">
                      Perguntas: {nlp_resultado.features.has_questions ? 'Sim' : 'Não'}
                    </Typography>
                  </Box>
                </Box>
                
                {/* Raciocínio NLP */}
                <Box>
                  <Typography variant="body2" color="text.secondary" mb={1}>
                    Raciocínio
                  </Typography>
                  <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                    {nlp_resultado.raciocinio}
                  </Typography>
                </Box>
              </Stack>
            </Paper>
          </Box>
          
          {/* Resultado Gemini */}
          <Box flex={1}>
            <Paper 
              elevation={2} 
              sx={{ 
                p: 2, 
                height: '100%',
                border: chosenMethod === 'gemini' ? '2px solid #2196f3' : '1px solid #e0e0e0',
                position: 'relative'
              }}
            >
              {chosenMethod === 'gemini' && (
                <Badge
                  badgeContent="ESCOLHIDO"
                  color="primary"
                  sx={{
                    position: 'absolute',
                    top: -8,
                    right: 8,
                    '& .MuiBadge-badge': {
                      fontSize: '0.6rem',
                      fontWeight: 'bold'
                    }
                  }}
                />
              )}
              
              <Box display="flex" alignItems="center" mb={2}>
                <GeminiIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="primary">
                  Gemini AI
                </Typography>
              </Box>
              
              <Stack spacing={2}>
                {/* Classificação Gemini */}
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Classificação
                  </Typography>
                  <Chip
                    label={gemini_resultado.classificacao}
                    color={getCategoryColor(gemini_resultado.classificacao)}
                    variant="filled"
                    size="medium"
                  />
                </Box>
                
                {/* Confiança Gemini */}
                <Box>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2" color="text.secondary">
                      Confiança
                    </Typography>
                    <Typography 
                      variant="body2" 
                      fontWeight="bold"
                      color={getConfidenceColor(gemini_resultado.confianca)}
                    >
                      {formatPercentage(gemini_resultado.confianca)}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={gemini_resultado.confianca * 100}
                    color={getConfidenceColor(gemini_resultado.confianca)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                
                {/* Análise Contextual */}
                <Box>
                  <Typography variant="body2" color="text.secondary" mb={1}>
                    Capacidades
                  </Typography>
                  <Stack spacing={0.5}>
                    <Typography variant="caption">
                      ✅ Análise contextual avançada
                    </Typography>
                    <Typography variant="caption">
                      ✅ Compreensão de nuances
                    </Typography>
                    <Typography variant="caption">
                      ✅ Raciocínio semântico
                    </Typography>
                    <Typography variant="caption">
                      ✅ Adaptação cultural (português)
                    </Typography>
                  </Stack>
                </Box>
                
                {/* Raciocínio Gemini */}
                <Box>
                  <Typography variant="body2" color="text.secondary" mb={1}>
                    Raciocínio
                  </Typography>
                  <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                    {gemini_resultado.raciocinio}
                  </Typography>
                </Box>
              </Stack>
            </Paper>
          </Box>
        </Box>
        
        {/* Resumo da Decisão */}
        <Divider sx={{ my: 3 }} />
        <Box 
          sx={{ 
            p: 2, 
            backgroundColor: '#f5f5f5', 
            borderRadius: 2,
            border: '1px solid #e0e0e0'
          }}
        >
          <Typography variant="subtitle2" color="text.primary" gutterBottom>
            🎯 Resumo da Decisão Final
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {concordancia.concordam 
              ? `Ambos os métodos concordaram na classificação. O método ${chosenMethod.toUpperCase()} foi escolhido por ter maior confiança (${formatPercentage(chosenMethod === 'nlp' ? nlp_resultado.confianca : gemini_resultado.confianca)}).`
              : `Os métodos divergiram na classificação. O método ${chosenMethod.toUpperCase()} foi escolhido baseado nos critérios de decisão do sistema (${concordancia.criterio_decisao.replace(/_/g, ' ')}).`
            }
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ComparisonAnalysis;