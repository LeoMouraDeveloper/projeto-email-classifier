// Componente principal para classificação de emails

import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Chip,
  Card,
  CardContent,
  LinearProgress,
  Divider,
  Tab,
  Tabs,
} from '@mui/material';
import {
  Send as SendIcon,
  CloudUpload as UploadIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Schedule as TimeIcon,
  CompareArrows as CompareIcon,
} from '@mui/icons-material';
import EmailClassifierService from '../services/emailClassifierService';
import { ClassificationResult, LoadingState } from '../types';
import ComparisonAnalysis from './ComparisonAnalysis';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const EmailClassifier: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [emailText, setEmailText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [loading, setLoading] = useState<LoadingState>({
    isLoading: false,
    error: null,
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setResult(null);
    setLoading({ isLoading: false, error: null });
  };

  const handleTextSubmit = async () => {
    const validation = EmailClassifierService.validateText(emailText);
    if (!validation.isValid) {
      setLoading({ isLoading: false, error: validation.error || 'Texto inválido' });
      return;
    }

    setLoading({ isLoading: true, error: null });
    setResult(null);

    try {
      const response = await EmailClassifierService.classifyEmailText(emailText);
      const classificationResult: ClassificationResult = {
        ...response,
        timestamp: Date.now(),
        input_text: emailText,
      };
      setResult(classificationResult);
      setLoading({ isLoading: false, error: null });
    } catch (error: any) {
      setLoading({
        isLoading: false,
        error: error.message || 'Erro ao classificar email',
      });
    }
  };

  const handleFileSubmit = async () => {
    if (!selectedFile) {
      setLoading({ isLoading: false, error: 'Selecione um arquivo' });
      return;
    }

    const validation = EmailClassifierService.validateFile(selectedFile);
    if (!validation.isValid) {
      setLoading({ isLoading: false, error: validation.error || 'Arquivo inválido' });
      return;
    }

    setLoading({ isLoading: true, error: null });
    setResult(null);

    try {
      const response = await EmailClassifierService.classifyEmailFile(selectedFile);
      const classificationResult: ClassificationResult = {
        ...response,
        timestamp: Date.now(),
        input_text: `Arquivo: ${selectedFile.name}`,
      };
      setResult(classificationResult);
      setLoading({ isLoading: false, error: null });
    } catch (error: any) {
      setLoading({
        isLoading: false,
        error: error.message || 'Erro ao classificar arquivo',
      });
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
      setLoading({ isLoading: false, error: null });
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'success';
    if (confidence >= 0.7) return 'warning';
    return 'error';
  };

  const getConfidenceLabel = (confidence: number) => {
    if (confidence >= 0.9) return 'Alta Confiança';
    if (confidence >= 0.7) return 'Média Confiança';
    return 'Baixa Confiança';
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
        📧 Email Classifier
      </Typography>
      
      <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary" sx={{ mb: 4 }}>
        Classifique emails como <strong>Produtivos</strong> ou <strong>Improdutivos</strong> usando IA
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} centered>
          <Tab label="📝 Texto" />
          <Tab label="📎 Arquivo" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <TextField
            fullWidth
            multiline
            rows={8}
            variant="outlined"
            label="Cole o texto do email aqui..."
            placeholder="Exemplo: Olá, preciso urgentemente do relatório mensal. Pode me enviar até amanhã?"
            value={emailText}
            onChange={(e) => {
              setEmailText(e.target.value);
              setResult(null);
              setLoading({ isLoading: false, error: null });
            }}
            sx={{ mb: 3 }}
          />
          
          <Button
            variant="contained"
            size="large"
            fullWidth
            startIcon={<SendIcon />}
            onClick={handleTextSubmit}
            disabled={loading.isLoading || !emailText.trim()}
          >
            {loading.isLoading ? 'Classificando...' : 'Classificar Email'}
          </Button>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ mb: 3 }}>
            <input
              accept=".txt,.pdf"
              style={{ display: 'none' }}
              id="file-upload"
              type="file"
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload">
              <Button
                variant="outlined"
                component="span"
                fullWidth
                startIcon={<UploadIcon />}
                sx={{ mb: 2, py: 2 }}
              >
                Selecionar Arquivo (.txt ou .pdf)
              </Button>
            </label>
            
            {selectedFile && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <strong>Arquivo selecionado:</strong> {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
              </Alert>
            )}
          </Box>
          
          <Button
            variant="contained"
            size="large"
            fullWidth
            startIcon={<SendIcon />}
            onClick={handleFileSubmit}
            disabled={loading.isLoading || !selectedFile}
          >
            {loading.isLoading ? 'Classificando...' : 'Classificar Arquivo'}
          </Button>
        </TabPanel>
      </Paper>

      {loading.isLoading && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box display="flex" alignItems="center" justifyContent="center" flexDirection="column">
            <CircularProgress size={40} sx={{ mb: 2 }} />
            <Typography variant="body1">
              Analisando email com IA... Isso pode levar alguns segundos.
            </Typography>
          </Box>
        </Paper>
      )}

      {loading.error && (
        <Alert severity="error" sx={{ mb: 3 }} icon={<ErrorIcon />}>
          <strong>Erro:</strong> {loading.error}
        </Alert>
      )}

      {result && (
        <>
          <Card elevation={3} sx={{ mb: 3 }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h5" component="h3">
                  📊 Resultado da Classificação
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <Chip
                    label={`Método: ${result.metodo_usado?.toUpperCase() || 'HÍBRIDO'}`}
                    color={result.metodo_usado === 'gemini' ? 'primary' : 'secondary'}
                    variant="outlined"
                    size="small"
                  />
                  <Chip
                    icon={<CheckIcon />}
                    label={result.categoria}
                    color={result.categoria === 'Produtivo' ? 'primary' : 'secondary'}
                    variant="filled"
                    size="medium"
                  />
                </Box>
              </Box>

              <Box mb={3}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Nível de Confiança: {getConfidenceLabel(result.confidence)}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={result.confidence * 100}
                  color={getConfidenceColor(result.confidence)}
                  sx={{ height: 8, borderRadius: 4 }}
                />
                <Typography variant="caption" color="text.secondary">
                  {(result.confidence * 100).toFixed(1)}% de certeza
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                💭 Justificativa
              </Typography>
              <Typography variant="body1" paragraph>
                {result.detalhes.justificativa}
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                💬 Resposta Sugerida
              </Typography>
              <Paper elevation={1} sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <Typography variant="body1" style={{ fontStyle: 'italic' }}>
                  "{result.resposta_sugerida}"
                </Typography>
              </Paper>

              <Box mt={2} display="flex" alignItems="center" gap={2} flexWrap="wrap">
                <Chip
                  icon={<TimeIcon />}
                  label={`${result.detalhes.tempo_processamento}s`}
                  size="small"
                  variant="outlined"
                />
                <Chip
                  label={result.detalhes.modelo}
                  size="small"
                  variant="outlined"
                />
                <Chip
                  label={result.detalhes.versao}
                  size="small"
                  variant="outlined"
                />
                {result.detalhes.analise_comparativa && (
                  <Chip
                    icon={<CompareIcon />}
                    label="Análise Comparativa Disponível"
                    color="info"
                    size="small"
                    variant="outlined"
                  />
                )}
              </Box>
            </CardContent>
          </Card>

          {/* Componente de Análise Comparativa */}
          {result.detalhes.analise_comparativa && (
            <ComparisonAnalysis
              analysis={result.detalhes.analise_comparativa}
              chosenMethod={result.metodo_usado as 'nlp' | 'gemini'}
            />
          )}
        </>
      )}
    </Container>
  );
};

export default EmailClassifier;