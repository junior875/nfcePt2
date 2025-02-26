// frontend/src/services/empresa.js
import api from './api';

const empresaService = {
  consultarCNPJ: async (cnpj) => {
    try {
      const response = await api.get(`/api/empresa/consultar-cnpj/${cnpj}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  cadastrarEmpresa: async (dados) => {
    try {
      const response = await api.post('/api/empresa', dados);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  listarEmpresas: async () => {
    try {
      const response = await api.get('/api/empresa');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  obterEmpresa: async (id) => {
    try {
      const response = await api.get(`/api/empresa/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  atualizarEmpresa: async (id, dados) => {
    try {
      const response = await api.put(`/api/empresa/${id}`, dados);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  excluirEmpresa: async (id) => {
    try {
      const response = await api.delete(`/api/empresa/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default empresaService;