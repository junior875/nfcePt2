# backend/app/services/nfce/emissao_service.py
import json
import logging
from typing import Dict, List, Any, Optional
from backend.app import db
from backend.app.models.empresa import Empresa
from backend.app.models.nfce.nfce import NFCe, ItemNFCe
from backend.app.services.nfce.factory_service import NFCeFactory
from database.factory import RepositoryFactory

logger = logging.getLogger(__name__)

class NFCeEmissaoService:
    """Serviço para emissão de NFC-e"""
    
    def __init__(self):
        self.factory = NFCeFactory()
        self.empresa_repository = RepositoryFactory.get_empresa_repository()
        
    def buscar_empresa_por_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """
        Busca uma empresa pelo CNPJ
        
        Args:
            cnpj (str): CNPJ da empresa
            
        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        try:
            # Limpar CNPJ para busca
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            return self.empresa_repository.find_by_cnpj(cnpj_limpo)
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por CNPJ {cnpj}: {e}")
            raise
    
    # Modificação para o método processar_emissao no arquivo backend/app/services/nfce/emissao_service.py

    def processar_emissao(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa a emissão de uma NFC-e
        
        Args:
            dados (Dict[str, Any]): Dados da requisição
                
        Returns:
            Dict[str, Any]: Resposta da API da Nuvem Fiscal ou mensagem de erro
        """
        try:
            # Validar dados mínimos
            self._validar_dados(dados)
            
            # Buscar empresa no banco
            empresa = self.buscar_empresa_por_cnpj(dados["empresa_cnpj"])
            if not empresa:
                # Se não encontrar a empresa, retornar erro
                return {
                    "erro": f"Empresa com CNPJ {dados['empresa_cnpj']} não encontrada no sistema. É necessário cadastrar a empresa antes de emitir notas fiscais.",
                    "status": "erro"
                }
            
            # Preparar itens
            itens = []
            valor_total = 0
            
            for produto in dados["produtos"]:
                item = self.factory.criar_item_nfce(
                    codigo=produto["codigo"],
                    descricao=produto["descricao"],
                    ncm=produto["ncm"],
                    quantidade=produto["quantidade"],
                    valor_unitario=produto["valor_unitario"]
                )
                itens.append(item)
                valor_total += item["prod"]["vProd"]
            
            # Preparar cliente
            cliente_dados = dados.get("cliente", {})
            cliente = self.factory.criar_dados_cliente(
                cpf=cliente_dados.get("cpf"),
                nome=cliente_dados.get("nome", "Consumidor Final")
            )
            
            # Preparar pagamento
            pagamento_dados = dados.get("pagamento", {})
            pagamento = self.factory.criar_pagamento(
                valor_total=valor_total,
                forma_pagamento=pagamento_dados.get("forma", "dinheiro"),
                valor_recebido=pagamento_dados.get("valor_recebido")
            )
            
            # Criar payload NFC-e com a empresa encontrada no banco
            payload = self.factory.criar_nfce_payload(
                empresa=empresa,
                itens=itens,
                cliente=cliente,
                pagamento=pagamento
            )
            
            # Emitir NFC-e
            logger.info(f"Emitindo NFC-e para empresa {empresa.nome_razao_social}")
            resposta = self.factory.emitir_nfce(payload)
            
            # Salvar registro no banco de dados se a resposta for válida
            if resposta and "erro" not in resposta:
                try:
                    self._salvar_nfce(resposta, empresa.id, itens, payload)
                except Exception as e:
                    logger.error(f"Erro ao salvar NFC-e no banco: {e}")
                    # Não impede o fluxo se falhar ao salvar
            
            return resposta
            
        except Exception as e:
            logger.error(f"Erro ao processar emissão de NFC-e: {e}")
            return {"erro": str(e), "status": "erro"}
    
    def _validar_dados(self, dados: Dict[str, Any]) -> None:
        """
        Valida os dados da requisição
        
        Args:
            dados (Dict[str, Any]): Dados da requisição
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        # Validar CNPJ da empresa
        if not dados.get("empresa_cnpj"):
            raise ValueError("CNPJ da empresa é obrigatório")
        
        # Validar produtos
        if not dados.get("produtos") or not isinstance(dados["produtos"], list) or len(dados["produtos"]) == 0:
            raise ValueError("Pelo menos um produto é obrigatório")
        
        # Validar cada produto
        for i, produto in enumerate(dados["produtos"]):
            if not produto.get("codigo"):
                raise ValueError(f"Código do produto {i+1} é obrigatório")
            if not produto.get("descricao"):
                raise ValueError(f"Descrição do produto {i+1} é obrigatória")
            if not produto.get("ncm"):
                raise ValueError(f"NCM do produto {i+1} é obrigatório")
            if not produto.get("quantidade"):
                raise ValueError(f"Quantidade do produto {i+1} é obrigatória")
            if not produto.get("valor_unitario"):
                raise ValueError(f"Valor unitário do produto {i+1} é obrigatório")
    
    def _salvar_nfce(
        self, 
        resposta: Dict[str, Any], 
        empresa_id: int, 
        itens: List[Dict[str, Any]],
        payload: Dict[str, Any]
    ) -> NFCe:
        """
        Salva a NFC-e no banco de dados
        
        Args:
            resposta (Dict[str, Any]): Resposta da API da Nuvem Fiscal
            empresa_id (int): ID da empresa
            itens (List[Dict[str, Any]]): Itens da NFC-e
            payload (Dict[str, Any]): Payload enviado para a API
            
        Returns:
            NFCe: Objeto NFC-e salvo
        """
        try:
            # Criar objeto NFC-e
            nfce = NFCe(
                nuvem_fiscal_id=resposta.get("id"),
                ambiente=resposta.get("ambiente"),
                created_at=resposta.get("created_at"),
                status=resposta.get("status"),
                data_emissao=resposta.get("data_emissao"),
                serie=resposta.get("serie"),
                numero=resposta.get("numero"),
                valor_total=resposta.get("valor_total", 0),
                chave=resposta.get("chave"),
                empresa_id=empresa_id,
                payload_enviado=json.dumps(payload, ensure_ascii=False),
                resposta_completa=json.dumps(resposta, ensure_ascii=False)
            )
            
            # Adicionar dados da autorização se existir
            autorizacao = resposta.get("autorizacao", {})
            if autorizacao:
                nfce.autorizacao_id = autorizacao.get("id")
                nfce.autorizacao_status = autorizacao.get("status")
                nfce.autorizacao_data_evento = autorizacao.get("data_evento")
                nfce.autorizacao_numero_protocolo = autorizacao.get("numero_protocolo")
                nfce.autorizacao_codigo_status = autorizacao.get("codigo_status")
                nfce.autorizacao_motivo_status = autorizacao.get("motivo_status")
            
            # Adicionar itens
            for item_data in itens:
                item = ItemNFCe(
                    codigo=item_data["prod"]["cProd"],
                    descricao=item_data["prod"]["xProd"],
                    ncm=item_data["prod"]["NCM"],
                    cfop=item_data["prod"]["CFOP"],
                    unidade=item_data["prod"]["uCom"],
                    quantidade=item_data["prod"]["qCom"],
                    valor_unitario=item_data["prod"]["vUnCom"],
                    valor_total=item_data["prod"]["vProd"],
                    icms_csosn=item_data["imposto"]["ICMS"]["ICMSSN102"]["CSOSN"],
                    pis_cst=item_data["imposto"]["PIS"]["PISAliq"]["CST"],
                    pis_valor=item_data["imposto"]["PIS"]["PISAliq"]["vPIS"],
                    cofins_cst=item_data["imposto"]["COFINS"]["COFINSAliq"]["CST"],
                    cofins_valor=item_data["imposto"]["COFINS"]["COFINSAliq"]["vCOFINS"]
                )
                nfce.itens.append(item)
            
            # Salvar no banco
            db.session.add(nfce)
            db.session.commit()
            
            logger.info(f"NFC-e salva com sucesso. ID: {nfce.id}, Chave: {nfce.chave}")
            return nfce
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao salvar NFC-e no banco: {e}")
            raise