# routers/Documentos_routers.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from schemas.Documento_schema import (
    TipoDocumentoResponse,
    DocumentoProdutorCreate,
    DocumentoProdutorUpdate,
    DocumentoProdutorResponse,
    WorkflowDocumentoCreate,
    WorkflowDocumentoUpdate,
    WorkflowDocumentoResponse,
    EtapaWorkflowUpdate,
    EtapaWorkflowResponse,
    DocumentoChecklistResponse,
    DocumentoChecklistItem,
    ProjetoVendaChecklist,
    ChecklistSecao
)
from models.Documento_model import (
    TipoDocumento,
    DocumentoProdutor,
    ArquivoDocumento,
    Arquivo,
    WorkflowDocumento,
    EtapaWorkflow
)
from models.Documentos_model import PROJETO_VENDA_MODELOS
from models.PerfilProdutor_model import PerfilProdutor
from models.User_model import User
from models.Documentos_model import DocumentoUsuario, DOCUMENTOS_REQUERIDOS
from security.security import get_current_user, get_db

router = APIRouter(tags=["Documentos"], prefix="/documentos")


# ===== TIPOS DE DOCUMENTOS =====

@router.get("/tipos", response_model=List[TipoDocumentoResponse])
async def listar_tipos_documentos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os tipos de documentos disponíveis"""
    tipos = db.query(TipoDocumento).all()
    return tipos


@router.get("/tipos/{tipo_id}", response_model=TipoDocumentoResponse)
async def obter_tipo_documento(
    tipo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um tipo de documento"""
    tipo = db.query(TipoDocumento).filter(TipoDocumento.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de documento não encontrado")
    return tipo


# ===== DOCUMENTOS DO PRODUTOR (RF-05) =====

@router.post("/produtor", status_code=status.HTTP_201_CREATED, response_model=DocumentoProdutorResponse)
async def criar_documento_produtor(
    documento_data: DocumentoProdutorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um registro de documento para o produtor.
    RF-05: Gestão de documentação (checklist e status)
    """
    # Valida produtor
    produtor = db.query(PerfilProdutor).filter(PerfilProdutor.id == documento_data.produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    # Valida tipo de documento
    tipo_doc = db.query(TipoDocumento).filter(TipoDocumento.id == documento_data.tipo_documento_id).first()
    if not tipo_doc:
        raise HTTPException(status_code=404, detail="Tipo de documento não encontrado")

    # Cria documento
    documento = DocumentoProdutor(
        produtor_id=documento_data.produtor_id,
        tipo_documento_id=documento_data.tipo_documento_id,
        status='pending'
    )

    # Calcula data de expiração se aplicável
    if tipo_doc.validade_dias:
        documento.expires_at = datetime.utcnow() + timedelta(days=tipo_doc.validade_dias)

    db.add(documento)
    db.commit()
    db.refresh(documento)

    return _build_documento_response(documento, db)


@router.get("/produtor/{produtor_id}", response_model=List[DocumentoProdutorResponse])
async def listar_documentos_produtor(
    produtor_id: int,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os documentos de um produtor"""
    query = db.query(DocumentoProdutor).filter(DocumentoProdutor.produtor_id == produtor_id)

    if status:
        query = query.filter(DocumentoProdutor.status == status)

    documentos = query.all()
    return [_build_documento_response(doc, db) for doc in documentos]


@router.get("/checklist", response_model=DocumentoChecklistResponse)
async def obter_checklist_documentos_usuario(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém checklist de documentos do usuário autenticado.

    Retorna apenas os documentos com status 'pending' - os que o usuário ainda precisa enviar.
    Busca na tabela documentos_usuario usando o user_id.

    RF-05: Gestão de documentação (checklist e status)
    """
    # Busca todos os documentos do usuário
    documentos_usuario = db.query(DocumentoUsuario).filter(
        DocumentoUsuario.user_id == current_user.id
    ).all()

    if not documentos_usuario:
        raise HTTPException(status_code=404, detail="Nenhum documento encontrado para este usuário")

    # Constrói mapa de documentos por nome para fácil acesso
    docs_map = {doc.nome_documento: doc for doc in documentos_usuario}

    # Conta documentos por status
    itens = []
    total_pendentes = 0
    total_enviados = 0
    total_aprovados = 0
    total_rejeitados = 0

    # Itera pelos documentos do usuário
    for documento in documentos_usuario:
        # Contadores
        if documento.status == 'pending':
            total_pendentes += 1
        elif documento.status == 'enviado':
            total_enviados += 1
        elif documento.status == 'aprovado':
            total_aprovados += 1
        elif documento.status == 'rejeitado':
            total_rejeitados += 1

        # Adiciona apenas documentos com status 'pending'
        if documento.status == 'pending':
            itens.append(DocumentoChecklistItem(
                tipo_documento_id=documento.id,
                tipo_documento_codigo=documento.nome_documento,
                tipo_documento_nome=documento.nome_documento,
                obrigatorio=True,
                status=documento.status,
                documento_id=documento.id,
                expires_at=None
            ))

    perfil_completo = total_pendentes == 0 and total_rejeitados == 0

    return DocumentoChecklistResponse(
        produtor_id=current_user.id,  # Usando user_id como produtor_id
        total_documentos=len(documentos_usuario),
        documentos_pendentes=total_pendentes,
        documentos_aprovados=total_aprovados,
        documentos_em_analise=total_enviados,  # 'enviado' é equivalente a 'in_review'
        documentos_reprovados=total_rejeitados,
        perfil_completo=perfil_completo,
        itens=itens
    )


@router.get("/produtor/{produtor_id}/checklist", response_model=DocumentoChecklistResponse)
async def obter_checklist_documentos(
    produtor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém checklist de documentos pendentes do produtor.
    RF-05: Gestão de documentação (checklist e status)
    """
    # Tenta buscar por PerfilProdutor.id primeiro
    produtor = db.query(PerfilProdutor).filter(PerfilProdutor.id == produtor_id).first()

    # Se não encontrar, tenta buscar por user_id
    if not produtor:
        produtor = db.query(PerfilProdutor).filter(PerfilProdutor.user_id == produtor_id).first()

    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    # Usa o id correto do PerfilProdutor para as queries seguintes
    perfil_produtor_id = produtor.id

    # Busca todos os tipos de documentos
    tipos_docs = db.query(TipoDocumento).all()

    # Busca documentos existentes do produtor
    documentos_existentes = db.query(DocumentoProdutor).filter(
        DocumentoProdutor.produtor_id == perfil_produtor_id
    ).all()

    # Cria mapa de documentos por tipo
    docs_map = {doc.tipo_documento_id: doc for doc in documentos_existentes}

    # Constrói checklist com apenas documentos pendentes
    itens = []
    total_pendentes = 0
    total_aprovados = 0
    total_em_analise = 0
    total_reprovados = 0

    for tipo_doc in tipos_docs:
        doc_existente = docs_map.get(tipo_doc.id)

        if doc_existente:
            status_doc = doc_existente.status
            documento_id = doc_existente.id
            expires_at = doc_existente.expires_at
        else:
            status_doc = 'pending'
            documento_id = None
            expires_at = None

        # Contadores
        if status_doc == 'pending':
            total_pendentes += 1
        elif status_doc == 'approved':
            total_aprovados += 1
        elif status_doc == 'in_review' or status_doc == 'submitted':
            total_em_analise += 1
        elif status_doc == 'rejected':
            total_reprovados += 1

        # Adiciona apenas documentos com status 'pending'
        if status_doc == 'pending':
            itens.append(DocumentoChecklistItem(
                tipo_documento_id=tipo_doc.id,
                tipo_documento_codigo=tipo_doc.codigo,
                tipo_documento_nome=tipo_doc.nome,
                obrigatorio=True,  # TODO: Verificar regra de obrigatoriedade
                status=status_doc,
                documento_id=documento_id,
                expires_at=expires_at
            ))

    perfil_completo = total_pendentes == 0 and total_reprovados == 0

    return DocumentoChecklistResponse(
        produtor_id=perfil_produtor_id,
        total_documentos=len(tipos_docs),
        documentos_pendentes=total_pendentes,
        documentos_aprovados=total_aprovados,
        documentos_em_analise=total_em_analise,
        documentos_reprovados=total_reprovados,
        perfil_completo=perfil_completo,
        itens=itens
    )


@router.get("/projeto-venda/checklist", response_model=List[ProjetoVendaChecklist])
async def listar_modelos_projeto_venda(
    subtipo: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna o checklist estruturado do Projeto de Venda para cada subtipo de produtor.
    Se um subtipo for informado, retorna apenas o checklist correspondente.
    """
    if subtipo:
        modelo_especifico = PROJETO_VENDA_MODELOS.get(subtipo)
        if not modelo_especifico:
            raise HTTPException(
                status_code=404,
                detail="Modelo de projeto nao encontrado para o subtipo informado"
            )
        return [_build_projeto_venda_checklist(subtipo, modelo_especifico)]

    return [
        _build_projeto_venda_checklist(key, value)
        for key, value in PROJETO_VENDA_MODELOS.items()
    ]


@router.patch("/{documento_id}", response_model=DocumentoProdutorResponse)
async def atualizar_documento(
    documento_id: int,
    documento_update: DocumentoProdutorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza status de um documento (aprovação/reprovação).
    RF-05: Gestão de documentação - Aprovação/reprovação
    """
    documento = db.query(DocumentoProdutor).filter(DocumentoProdutor.id == documento_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    if documento_update.status:
        documento.status = documento_update.status
        documento.reviewed_by_user_id = current_user.id
        documento.reviewed_at = datetime.utcnow()

        # Se reprovado, exige justificativa
        if documento_update.status == 'rejected':
            if not documento_update.rejection_reason:
                raise HTTPException(status_code=400, detail="Justificativa obrigatória para reprovação")
            documento.rejection_reason = documento_update.rejection_reason

    db.commit()
    db.refresh(documento)

    # TODO: Enviar notificação para o produtor

    return _build_documento_response(documento, db)


@router.post("/{documento_id}/upload", status_code=status.HTTP_201_CREATED)
async def upload_arquivo_documento(
    documento_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Faz upload de arquivo para um documento.
    RF-05: Upload de documento
    """
    documento = db.query(DocumentoProdutor).filter(DocumentoProdutor.id == documento_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    # TODO: Implementar upload real de arquivo
    # Por enquanto, apenas simula
    arquivo = Arquivo(
        nome_original=file.filename,
        caminho_storage=f"/storage/documentos/{documento_id}/{file.filename}",
        mime_type=file.content_type,
        uploaded_by_user_id=current_user.id
    )

    db.add(arquivo)
    db.flush()

    # Versiona arquivo do documento
    versao_atual = db.query(ArquivoDocumento).filter(
        ArquivoDocumento.documento_produtor_id == documento_id
    ).count()

    arquivo_doc = ArquivoDocumento(
        documento_produtor_id=documento_id,
        arquivo_id=arquivo.id,
        versao=versao_atual + 1,
        uploaded_by_user_id=current_user.id
    )

    db.add(arquivo_doc)

    # Atualiza status do documento
    documento.status = 'submitted'

    db.commit()

    return {"message": "Arquivo enviado com sucesso", "arquivo_id": arquivo.id, "versao": arquivo_doc.versao}


@router.post("/upload-by-name", status_code=status.HTTP_201_CREATED)
async def upload_documento_por_nome(
    nome_documento: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    valor: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Registra/atualiza um documento identificando pelo nome.

    O endpoint recebe o nome do documento e pode receber:
    - Um arquivo PDF (para upload de documento), OU
    - Um valor textual (ex: número de CPF, CNPJ)

    RF-05: Upload/Registro de documento por nome

    Parâmetros (form-data):
    - nome_documento: Nome do documento (string, OBRIGATÓRIO)
    - file: Arquivo PDF (opcional) - apenas se enviando arquivo
    - valor: Valor textual (opcional) - ex: "123.456.789-00" para CPF

    Validação:
    - nome_documento é obrigatório
    - Pelo menos um de 'file' ou 'valor' deve ser fornecido
    - Se file for enviado, deve ser PDF
    - Se file for enviado, valor será ignorado

    Armazenamento:
    - Se file: Arquivo é armazenado no caminho_arquivo
    - Se valor: Armazenado no campo observacoes

    Exemplos de uso:
    - Com valor: curl -F 'nome_documento=CPF' -F 'valor=123.456.789-00'
    - Com arquivo: curl -F 'nome_documento=DAP' -F 'file=@documento.pdf'
    """
    # Valida nome_documento
    if not nome_documento:
        raise HTTPException(
            status_code=400,
            detail="O parâmetro 'nome_documento' é obrigatório"
        )

    # Valida que pelo menos um campo foi fornecido
    if not file and not valor:
        raise HTTPException(
            status_code=400,
            detail="Pelo menos um de 'file' ou 'valor' deve ser fornecido"
        )

    # Valida tipo de arquivo se fornecido
    if file and file.content_type not in ['application/pdf', 'application/x-pdf']:
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos")

    # Busca ou cria DocumentoUsuario
    documento = db.query(DocumentoUsuario).filter(
        DocumentoUsuario.user_id == current_user.id,
        DocumentoUsuario.nome_documento == nome_documento
    ).first()

    if not documento:
        # Cria novo DocumentoUsuario se não existir
        documento = DocumentoUsuario(
            user_id=current_user.id,
            nome_documento=nome_documento,
            status='pending'
        )
        db.add(documento)
        db.flush()

    # Processa upload de arquivo se fornecido
    if file:
        # Atualiza caminho do arquivo
        documento.caminho_arquivo = f"/storage/documentos/{current_user.id}/{nome_documento}/{file.filename}"
        documento.data_envio = datetime.utcnow()

        # TODO: Implementar upload real do arquivo para storage
        # Por enquanto, apenas registra o caminho

    # Processa valor textual se fornecido (e nenhum arquivo foi enviado)
    elif valor:
        documento.observacoes = f"Valor informado: {valor}"
        documento.data_envio = datetime.utcnow()

    # Atualiza status para 'enviado'
    documento.status = 'enviado'

    db.commit()
    db.refresh(documento)

    return {
        "message": "Documento registrado com sucesso",
        "documento_id": documento.id,
        "nome_documento": nome_documento,
        "status": "enviado",
        "tipo_envio": "arquivo" if file else "valor textual",
        "valor_armazenado": valor if valor else file.filename if file else None
    }


# ===== WORKFLOW DE EMISSÃO ASSISTIDA (RF-06) =====

@router.post("/workflows", status_code=status.HTTP_201_CREATED, response_model=WorkflowDocumentoResponse)
async def criar_workflow_documento(
    workflow_data: WorkflowDocumentoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Inicia workflow de emissão assistida de documento.
    RF-06: Emissão assistida de documentos (workflow guiado)
    """
    # Valida produtor e tipo de documento
    produtor = db.query(PerfilProdutor).filter(PerfilProdutor.id == workflow_data.produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    tipo_doc = db.query(TipoDocumento).filter(TipoDocumento.id == workflow_data.tipo_documento_id).first()
    if not tipo_doc:
        raise HTTPException(status_code=404, detail="Tipo de documento não encontrado")

    # Cria workflow
    workflow = WorkflowDocumento(
        produtor_id=workflow_data.produtor_id,
        tipo_documento_id=workflow_data.tipo_documento_id,
        status='not_started',
        etapa_atual=1
    )

    db.add(workflow)
    db.flush()

    # Cria etapas padrão (exemplo para DAP)
    etapas_padrao = [
        {"numero": 1, "titulo": "Providenciar CPF", "descricao": "Certifique-se de ter CPF válido"},
        {"numero": 2, "titulo": "Agendar atendimento", "descricao": "Agende atendimento no sindicato rural"},
        {"numero": 3, "titulo": "Levar documentos", "descricao": "Leve RG, CPF e comprovante de residência"},
        {"numero": 4, "titulo": "Receber DAP", "descricao": "Receba sua DAP e anexe aqui"}
    ]

    for etapa_data in etapas_padrao:
        etapa = EtapaWorkflow(
            workflow_id=workflow.id,
            numero_etapa=etapa_data["numero"],
            titulo=etapa_data["titulo"],
            descricao=etapa_data["descricao"],
            status='todo'
        )
        db.add(etapa)

    db.commit()
    db.refresh(workflow)

    return _build_workflow_response(workflow, db)


@router.get("/workflows/{workflow_id}", response_model=WorkflowDocumentoResponse)
async def obter_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um workflow de documento"""
    workflow = db.query(WorkflowDocumento).filter(WorkflowDocumento.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    return _build_workflow_response(workflow, db)


@router.patch("/workflows/{workflow_id}", response_model=WorkflowDocumentoResponse)
async def atualizar_workflow(
    workflow_id: int,
    workflow_update: WorkflowDocumentoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza status ou etapa atual do workflow"""
    workflow = db.query(WorkflowDocumento).filter(WorkflowDocumento.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    if workflow_update.status:
        workflow.status = workflow_update.status
    if workflow_update.etapa_atual:
        workflow.etapa_atual = workflow_update.etapa_atual

    db.commit()
    db.refresh(workflow)

    return _build_workflow_response(workflow, db)


@router.patch("/workflows/etapas/{etapa_id}", response_model=EtapaWorkflowResponse)
async def atualizar_etapa_workflow(
    etapa_id: int,
    etapa_update: EtapaWorkflowUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marca etapa do workflow como concluída ou pulada"""
    etapa = db.query(EtapaWorkflow).filter(EtapaWorkflow.id == etapa_id).first()
    if not etapa:
        raise HTTPException(status_code=404, detail="Etapa não encontrada")

    etapa.status = etapa_update.status
    if etapa_update.status == 'done':
        etapa.concluida_em = datetime.utcnow()

    db.commit()
    db.refresh(etapa)

    return EtapaWorkflowResponse.from_orm(etapa)


# ===== FUNÇÕES AUXILIARES =====

def _build_projeto_venda_checklist(subtipo: str, modelo: dict) -> ProjetoVendaChecklist:
    """Monta o checklist do projeto de venda a partir do dicionário base"""
    secoes = [
        ChecklistSecao(titulo=secao["titulo"], itens=secao["itens"])
        for secao in modelo.get("secoes", [])
    ]
    return ProjetoVendaChecklist(
        subtipo=subtipo,
        titulo=modelo.get("titulo", ""),
        secoes=secoes
    )

def _build_documento_response(documento: DocumentoProdutor, db: Session) -> DocumentoProdutorResponse:
    """Constrói resposta de documento com informações do tipo"""
    tipo_doc = db.query(TipoDocumento).filter(TipoDocumento.id == documento.tipo_documento_id).first()

    return DocumentoProdutorResponse(
        id=documento.id,
        produtor_id=documento.produtor_id,
        tipo_documento_id=documento.tipo_documento_id,
        status=documento.status,
        reviewed_by_user_id=documento.reviewed_by_user_id,
        reviewed_at=documento.reviewed_at,
        rejection_reason=documento.rejection_reason,
        expires_at=documento.expires_at,
        created_at=documento.created_at,
        updated_at=documento.updated_at,
        tipo_documento_nome=tipo_doc.nome if tipo_doc else None,
        tipo_documento_codigo=tipo_doc.codigo if tipo_doc else None
    )


def _build_workflow_response(workflow: WorkflowDocumento, db: Session) -> WorkflowDocumentoResponse:
    """Constrói resposta de workflow com etapas"""
    tipo_doc = db.query(TipoDocumento).filter(TipoDocumento.id == workflow.tipo_documento_id).first()

    etapas = db.query(EtapaWorkflow).filter(
        EtapaWorkflow.workflow_id == workflow.id
    ).order_by(EtapaWorkflow.numero_etapa).all()

    etapas_response = [EtapaWorkflowResponse.from_orm(e) for e in etapas]

    return WorkflowDocumentoResponse(
        id=workflow.id,
        produtor_id=workflow.produtor_id,
        tipo_documento_id=workflow.tipo_documento_id,
        status=workflow.status,
        etapa_atual=workflow.etapa_atual,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at,
        tipo_documento_nome=tipo_doc.nome if tipo_doc else None,
        etapas=etapas_response
    )
