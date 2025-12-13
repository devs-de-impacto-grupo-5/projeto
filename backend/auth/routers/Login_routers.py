from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from schemas.Password_schema import PasswordReset, PasswordResetRequest
from schemas.User_schema import UserCreate
from schemas.Register_schema import (
    RegisterRequest,
    RegisterFornecedorIndividual,
    RegisterGrupoInformal,
    RegisterGrupoFormal
)
from sqlalchemy.orm import Session
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
from models.Conta_model import FornecedorIndividual, GrupoInformal, GrupoFormal

router = APIRouter(tags=["Autenticação"])


# ----------------------------
# Endpoints
# ----------------------------

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Registra um novo usuário no sistema"""

    # Verifica se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Cria o usuário
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        senha=user_data.senha,  # Será hasheado no __init__
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Usuário criado com sucesso",
        "user_id": new_user.id
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registra um novo usuário e conta de acordo com o tipo especificado.

    Tipos de conta suportados:
    - fornecedor_individual: Requer CPF
    - grupo_informal: Requer lista de CPFs
    - grupo_formal: Requer CNPJ
    """

    # Verifica se o email já está cadastrado
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Valida os dados de acordo com o tipo de conta
    if data.tipo_conta == "fornecedor_individual":
        if not data.cpf:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="CPF é obrigatório para fornecedor individual"
            )

        # Verifica se o CPF já está cadastrado
        existing_cpf = db.query(FornecedorIndividual).filter(
            FornecedorIndividual.cpf == data.cpf
        ).first()
        if existing_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )

    elif data.tipo_conta == "grupo_informal":
        if not data.cpfs or len(data.cpfs) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Lista de CPFs é obrigatória para grupo informal"
            )

        # Verifica se algum CPF já está cadastrado
        for cpf in data.cpfs:
            existing_cpf = db.query(GrupoInformal).filter(
                GrupoInformal.cpfs.contains([cpf])
            ).first()
            if existing_cpf:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"CPF {cpf} já cadastrado em outro grupo"
                )

    elif data.tipo_conta == "grupo_formal":
        if not data.cnpj:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="CNPJ é obrigatório para grupo formal"
            )

        # Verifica se o CNPJ já está cadastrado
        existing_cnpj = db.query(GrupoFormal).filter(
            GrupoFormal.cnpj == data.cnpj
        ).first()
        if existing_cnpj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tipo de conta inválido. Use: fornecedor_individual, grupo_informal ou grupo_formal"
        )

    # Cria o usuário
    new_user = User(
        name=data.name,
        email=data.email,
        senha=data.senha,
        role=data.tipo_conta
    )

    db.add(new_user)
    db.flush()  # Flush para obter o ID do usuário sem commitar ainda

    # Cria a conta específica de acordo com o tipo
    if data.tipo_conta == "fornecedor_individual":
        conta = FornecedorIndividual(
            user_id=new_user.id,
            cpf=data.cpf
        )
        db.add(conta)

    elif data.tipo_conta == "grupo_informal":
        conta = GrupoInformal(
            user_id=new_user.id,
            cpfs=data.cpfs
        )
        db.add(conta)

    elif data.tipo_conta == "grupo_formal":
        conta = GrupoFormal(
            user_id=new_user.id,
            cnpj=data.cnpj
        )
        db.add(conta)

    db.commit()
    db.refresh(new_user)

    return {
        "message": f"Conta {data.tipo_conta} criada com sucesso",
        "user_id": new_user.id,
        "tipo_conta": data.tipo_conta,
        "email": new_user.email,
        "name": new_user.name
    }

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Busca o usuário pelo email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verifica credenciais
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
        "name": user.name,
        "email": user.email
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