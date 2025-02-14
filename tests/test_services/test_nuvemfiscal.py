import pytest
from unittest.mock import patch, Mock
from backend.app.services.nuvem_fiscal.client import NuvemFiscalClient

@pytest.fixture
def client():
    return NuvemFiscalClient()

@pytest.fixture
def mock_response():
    return {
        "cnpj": "12345678000199",
        "razao_social": "EMPRESA TESTE LTDA",
        "nome_fantasia": "EMPRESA TESTE",
        "email": "contato@empresa.com",
        "telefone": {
            "numero": "11999999999"
        },
        "endereco": {
            "cep": "01001000",
            "logradouro": "Rua Teste",
            "numero": "123",
            "complemento": "Sala 1",
            "bairro": "Centro",
            "municipio": {
                "nome": "São Paulo"
            },
            "uf": "SP"
        }
    }

def test_authenticate_success(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'access_token': 'token123'}
        mock_post.return_value.raise_for_status = Mock()
        
        client.authenticate()
        assert client.access_token == 'token123'

def test_authenticate_failure(client):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Erro de autenticação")
        
        with pytest.raises(Exception) as exc_info:
            client.authenticate()
        assert "Falha na autenticação" in str(exc_info.value)

def test_consultar_cnpj_success(client, mock_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = Mock()
        
        result = client.consultar_cnpj("12.345.678/0001-99")
        assert result == mock_response

def test_consultar_cnpj_invalid(client):
    result = client.consultar_cnpj("123")
    assert result is None

def test_formatar_dados_empresa(client, mock_response):
    formatted = client.formatar_dados_empresa(mock_response)
    
    assert formatted == {
        'cnpj': '12345678000199',
        'razao_social': 'EMPRESA TESTE LTDA',
        'nome_fantasia': 'EMPRESA TESTE',
        'email': 'contato@empresa.com',
        'telefone': '11999999999',
        'endereco': {
            'cep': '01001000',
            'logradouro': 'Rua Teste',
            'numero': '123',
            'complemento': 'Sala 1',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'uf': 'SP'
        }
    }

def test_consultar_cnpj_retry_on_401(client, mock_response):
    with patch('requests.get') as mock_get:
        # Primeira chamada retorna 401
        mock_get.return_value.status_code = 401
        # Segunda chamada retorna sucesso
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = Mock()
        
        with patch.object(client, 'authenticate') as mock_auth:
            result = client.consultar_cnpj("12.345.678/0001-99")
            
            # Verifica se authenticate foi chamado
            mock_auth.assert_called_once()
            assert result == mock_response