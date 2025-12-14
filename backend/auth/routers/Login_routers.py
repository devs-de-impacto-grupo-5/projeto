from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from schemas.Password_schema import PasswordReset, PasswordResetRequest
from schemas.User_schema import UserCreate
from schemas.Register_schema import (
    RegisterRequest,
    RegisterFornecedorIndividual,
    RegisterGrupoInformal,
    RegisterGrupoFormal,
    RegisterEscola,
    RegisterGoverno
)
from schemas.Validacao_schema import ValidacaoCPFCNPJRequest, ValidacaoCPFCNPJResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi.security import OAuth2PasswordRequestForm
from security.security import (
    create_access_token,
    send_password_reset_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_db,
    get_password_reset_token,
    verify_password_reset_token
)
from models.User_model import User, pwd_context
from models.Conta_model import (
    FornecedorIndividual,
    GrupoInformal,
    GrupoFormal,
    Escola,
    Governo
)
from models.PerfilProdutor_model import PerfilProdutor
from models.Documentos_model import DocumentoUsuario, DOCUMENTOS_REQUERIDOS
from models.PerfilProdutor_model import PerfilProdutor

router = APIRouter(tags=["Autenticação"])


# ----------------------------
# Endpoints
# ----------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registra um novo usuário de acordo com o tipo especificado.

    Tipos de usuário suportados:
    - produtor:
        - fornecedor_individual: Requer CPF
        - grupo_informal: Requer lista de CPFs
        - grupo_formal: Requer CNPJ
    - entidade_executora:
        - escola: Requer nome_escola
        - governo: Requer nome_orgao e nivel
    """

    # Verifica se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    total_users = db.query(func.count(User.id)).scalar() or 0
    is_first_user = total_users == 0

    # Valida conforme o tipo de usuário
    if data.tipo_usuario == "produtor":
        if data.subtipo_usuario == "fornecedor_individual":
            if not data.cpf:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="CPF é obrigatório para fornecedor individual"
                )
            existing_cpf = db.query(FornecedorIndividual).filter(
                FornecedorIndividual.cpf == data.cpf
            ).first()
            if existing_cpf:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF já cadastrado"
                )

        elif data.subtipo_usuario == "grupo_informal":
            participantes_payload = []
            if data.participantes:
                for p in data.participantes:
                    participantes_payload.append(p if isinstance(p, dict) else p.model_dump())
            # compatibilidade: aceitar payload antigo com lista de CPFs
            if (not participantes_payload or len(participantes_payload) == 0) and data.cpfs:
                participantes_payload = [{"cpf": cpf} for cpf in data.cpfs]

            if not participantes_payload or len(participantes_payload) == 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Lista de participantes é obrigatória para grupo informal"
                )
            # Valida que cada participante tem nome e CPF
            for p in participantes_payload:
                if not p.get("cpf"):
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Cada participante deve ter CPF"
                    )
            data.participantes = participantes_payload

        elif data.subtipo_usuario == "grupo_formal":
            if not data.cnpj:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="CNPJ é obrigatório para grupo formal"
                )
            existing_cnpj = db.query(GrupoFormal).filter(
                GrupoFormal.cnpj == data.cnpj
            ).first()
            if existing_cnpj:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CNPJ já cadastrado"
                )

    elif data.tipo_usuario == "entidade_executora":
        if data.subtipo_usuario == "escola":
            if not data.nome_escola:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nome da escola é obrigatório"
                )

        elif data.subtipo_usuario == "governo":
            if not data.nome_orgao:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nome do órgão é obrigatório"
                )
            if not data.nivel:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nível do órgão (municipal, estadual, federal) é obrigatório"
                )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tipo de usuário inválido. Use: 'produtor' ou 'entidade_executora'"
        )

    # Valida coordenadas GPS se fornecidas
    if data.latitude is not None or data.longitude is not None:
        if data.latitude is None or data.longitude is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Latitude e longitude devem ser fornecidas juntas"
            )
        if not (-90 <= data.latitude <= 90):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Latitude deve estar entre -90 e 90"
            )
        if not (-180 <= data.longitude <= 180):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Longitude deve estar entre -180 e 180"
            )

    # Cria o usuário (primeiro é admin_master, demais entram como produtores por padrão de role)
    new_user = User(
        name=data.name,
        email=data.email,
        senha=data.senha,
        tipo_usuario=data.tipo_usuario,
        subtipo_usuario=data.subtipo_usuario,
        latitude=data.latitude,
        longitude=data.longitude,
        role="admin_master" if is_first_user else "produtor"
    )

    db.add(new_user)
    db.flush()

    # Cria a conta específica de acordo com o tipo
    if data.tipo_usuario == "produtor":
        # Cria o PerfilProdutor para todos os tipos de produtores
        endereco_json = None
        if data.latitude is not None and data.longitude is not None:
            endereco_json = {
                "geo": {
                    "latitude": data.latitude,
                    "longitude": data.longitude
                }
            }

        # Adiciona endereÇõo enviado no payload
        if data.endereco or data.numero or data.cidade or data.uf:
            endereco_json = endereco_json or {}
            endereco_json.update({
                "endereco": data.endereco,
                "numero": data.numero,
                "cidade": data.cidade,
                "uf": data.uf
            })

        perfil_produtor = PerfilProdutor(
            user_id=new_user.id,
            tipo_produtor=data.subtipo_usuario,
            identificacao_legal=data.cpf if data.subtipo_usuario == "fornecedor_individual" else data.cnpj,
            endereco_json=endereco_json,
            status_perfil='incomplete'
        )
        db.add(perfil_produtor)
        db.flush()

        if data.subtipo_usuario == "fornecedor_individual":
            conta = FornecedorIndividual(
                user_id=new_user.id,
                cpf=data.cpf
            )
            db.add(conta)

        elif data.subtipo_usuario == "grupo_informal":
            # Converte participantes para lista de dicts para armazenar em JSON
            participantes_list = []
            for p in data.participantes:
                participante_dict = {"cpf": p["cpf"]}
                if p.get("nome"):
                    participante_dict["nome"] = p["nome"]
                participantes_list.append(participante_dict)
            conta = GrupoInformal(
                user_id=new_user.id,
                participantes=participantes_list
            )
            db.add(conta)

        elif data.subtipo_usuario == "grupo_formal":
            conta = GrupoFormal(
                user_id=new_user.id,
                cnpj=data.cnpj
            )
            db.add(conta)

        # Cria PerfilProdutor se houver dados de endereço
        # Dados de endereÇõo jÇ­ foram anexados ao perfil_produtor acima

    elif data.tipo_usuario == "entidade_executora":
        if data.subtipo_usuario == "escola":
            escola = Escola(
                user_id=new_user.id,
                nome_escola=data.nome_escola,
                endereco=data.endereco,
                telefone=data.telefone
            )
            db.add(escola)

        elif data.subtipo_usuario == "governo":
            governo = Governo(
                user_id=new_user.id,
                nome_orgao=data.nome_orgao,
                nivel=data.nivel,
                endereco=data.endereco,
                telefone=data.telefone
            )
            db.add(governo)

    # Se for produtor, cria documentos pendentes
    if data.tipo_usuario == "produtor":
        _criar_documentos_pendentes(db, new_user.id, data.subtipo_usuario)

    db.commit()
    db.refresh(new_user)

    response = {
        "message": f"Usuário {data.tipo_usuario} ({data.subtipo_usuario}) criado com sucesso",
        "user_id": new_user.id,
        "tipo_usuario": data.tipo_usuario,
        "subtipo_usuario": data.subtipo_usuario,
        "email": new_user.email,
        "name": new_user.name,
        "role": new_user.role
    }

    # Adiciona localização se fornecida
    if new_user.latitude is not None and new_user.longitude is not None:
        response["localizacao"] = {
            "latitude": new_user.latitude,
            "longitude": new_user.longitude
        }

    # Para produtores, inclui quantidade de documentos pendentes
    if data.tipo_usuario == "produtor":
        documentos_pendentes = db.query(DocumentoUsuario).filter(
            DocumentoUsuario.user_id == new_user.id,
            DocumentoUsuario.status == "pending"
        ).count()
        response["documentos_pendentes"] = documentos_pendentes

    return response


def _criar_documentos_pendentes(db: Session, user_id: int, subtipo: str) -> None:
    """
    Cria registros de documentos obrigatórios com status 'pending' para o produtor.
    """
    documentos_requeridos = DOCUMENTOS_REQUERIDOS.get(subtipo, [])
    docs = [
        DocumentoUsuario(
            user_id=user_id,
            nome_documento=doc["nome"],
            descricao=doc.get("descricao"),
            status="pending"
        )
        for doc in documentos_requeridos
    ]
    if docs:
        db.add_all(docs)

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Busca o usuário pelo email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Se não achou por email, tenta por CPF
    if not user:
        # Tenta encontrar no FornecedorIndividual
        fornecedor = db.query(FornecedorIndividual).filter(FornecedorIndividual.cpf == form_data.username).first()
        
        if fornecedor:
            user = db.query(User).filter(User.id == fornecedor.user_id).first()
    
    # Verifica credenciais
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/CPF ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )

    role_out = user.role or user.tipo_usuario

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": role_out,
        "name": user.name,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario,
        "subtipo_usuario": user.subtipo_usuario
    }

@router.get("/usuarios")
async def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos os usuários registrados"""
    usuarios = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in usuarios]


@router.post("/solicitar-redefinicao-senha")
async def solicitar_redefinicao_senha(
    request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Inicia o processo de redefinição de senha"""
    
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Gera token de redefinição (expira em 1 hora)
    reset_token = get_password_reset_token(email=user.email)
    
    # Simula envio de email (implemente sua lógica real aqui)
    background_tasks.add_task(
        send_password_reset_email,
        user.email,
        reset_token
    )

    return {"message": "Instruções de redefinição enviadas para o email"}

@router.post("/redefinir-senha")
async def redefinir_senha(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Finaliza a redefinição de senha com token válido"""
    
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Faz o hash da nova senha antes de salvar
    hashed_password = pwd_context.hash(reset_data.new_password)
    user.senha = hashed_password
    db.commit()

    return {"message": "Senha redefinida com sucesso"}

@router.get("/usuarios/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Obtém um usuário pelo ID"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@router.post("/validar-usuario", response_model=ValidacaoCPFCNPJResponse)
async def validar_documento(
    request: ValidacaoCPFCNPJRequest,
    db: Session = Depends(get_db)
):
    """
    Valida se um CPF ou CNPJ já está cadastrado no sistema.
    
    Verifica em:
    - Fornecedores individuais (CPF)
    - Grupos informais (CPF nos participantes)
    - Grupos formais (CNPJ)
    
    Retorna True se já está cadastrado, False caso contrário.
    """
    documento = request.documento.strip()
    
    # Detecta se é CPF ou CNPJ baseado no formato
    # CPF: XXX.XXX.XXX-XX (14 caracteres)
    # CNPJ: XX.XXX.XXX/XXXX-XX (18 caracteres)
    is_cpf = len(documento) == 14 and documento.count('.') == 2 and documento.count('-') == 1
    is_cnpj = len(documento) == 18 and documento.count('.') == 2 and documento.count('/') == 1 and documento.count('-') == 1
    
    if not is_cpf and not is_cnpj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato inválido. Use CPF (XXX.XXX.XXX-XX) ou CNPJ (XX.XXX.XXX/XXXX-XX)"
        )
    
    ja_cadastrado = False
    
    if is_cpf:
        # Verifica em fornecedores individuais
        fornecedor = db.query(FornecedorIndividual).filter(
            FornecedorIndividual.cpf == documento
        ).first()
        
        if fornecedor:
            ja_cadastrado = True
        else:
            # Verifica em grupos informais (dentro do JSON de participantes)
            # Busca grupos informais onde o JSON contém o CPF
            grupos_informais = db.query(GrupoInformal).all()
            for grupo in grupos_informais:
                if grupo.participantes:
                    # participantes é uma lista de dicts: [{"nome": "...", "cpf": "..."}, ...]
                    if isinstance(grupo.participantes, list):
                        for participante in grupo.participantes:
                            if isinstance(participante, dict) and participante.get("cpf") == documento:
                                ja_cadastrado = True
                                break
                    if ja_cadastrado:
                        break
    
    elif is_cnpj:
        # Verifica em grupos formais
        grupo_formal = db.query(GrupoFormal).filter(
            GrupoFormal.cnpj == documento
        ).first()
        
        if grupo_formal:
            ja_cadastrado = True
    
    return ValidacaoCPFCNPJResponse(
        ja_cadastrado=ja_cadastrado,
        documento=documento,
        tipo="cpf" if is_cpf else "cnpj"
    )
