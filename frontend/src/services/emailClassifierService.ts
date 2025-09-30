// Serviço para comunicação com a API de Classificação de Emails

import axios from 'axios';
import { EmailClassificationResponse, ApiError } from '../types';

// Configuração base da API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT || '60000', 10); // 60 segundos

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = error.response?.data?.detail || error.message || 'Erro desconhecido';
    let detail = error.response?.data?.message || error.response?.statusText;
    
    // Tratamento específico para timeout
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      message = 'O servidor está iniciando (cold start). Isso pode levar até 1 minuto no primeiro acesso.';
      detail = 'Tente novamente em alguns segundos. O Render free tier hiberna quando não há uso.';
    }
    
    const apiError: ApiError = {
      message,
      detail,
    };
    return Promise.reject(apiError);
  }
);

export class EmailClassifierService {
  
  // Classificar email por texto
  static async classifyEmailText(text: string): Promise<EmailClassificationResponse> {
    try {
      const formData = new FormData();
      formData.append('text', text.trim());
      
      const response = await apiClient.post('/process_email', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao classificar email por texto:', error);
      throw error;
    }
  }

  // Classificar email por arquivo
  static async classifyEmailFile(file: File): Promise<EmailClassificationResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await apiClient.post('/process_email', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao classificar email por arquivo:', error);
      throw error;
    }
  }

  // Verificar saúde da API
  static async checkHealth(): Promise<any> {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Erro ao verificar saúde da API:', error);
      throw error;
    }
  }

  // Obter informações do sistema
  static async getSystemInfo(): Promise<any> {
    try {
      const response = await apiClient.get('/system_info');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter informações do sistema:', error);
      throw error;
    }
  }

  // Validar arquivo (tamanho, tipo, etc.)
  static validateFile(file: File): { isValid: boolean; error?: string } {
    const maxSize = 10 * 1024 * 1024; // 10MB
    const allowedTypes = ['text/plain', 'application/pdf'];
    
    if (file.size > maxSize) {
      return {
        isValid: false,
        error: 'Arquivo muito grande. Máximo permitido: 10MB'
      };
    }
    
    if (!allowedTypes.includes(file.type)) {
      return {
        isValid: false,
        error: 'Tipo de arquivo não suportado. Use apenas .txt ou .pdf'
      };
    }
    
    return { isValid: true };
  }

  // Validar texto de entrada
  static validateText(text: string): { isValid: boolean; error?: string } {
    const trimmedText = text.trim();
    
    if (!trimmedText) {
      return {
        isValid: false,
        error: 'Por favor, insira um texto para classificar'
      };
    }
    
    if (trimmedText.length < 10) {
      return {
        isValid: false,
        error: 'Texto muito curto. Mínimo de 10 caracteres'
      };
    }
    
    if (trimmedText.length > 5000) {
      return {
        isValid: false,
        error: 'Texto muito longo. Máximo de 5000 caracteres'
      };
    }
    
    return { isValid: true };
  }
}

export default EmailClassifierService;