# models/User_model.py
from sqlalchemy import Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import mapped_column
from db.base import Base  # Importação direta da Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    senha = mapped_column(String(255), nullable=False)

    # Tipo de usuário: "entidade_executora" ou "produtor"
    tipo_usuario = mapped_column(String(50), nullable=False)

    # Subtipo específico:
    # Se tipo_usuario="entidade_executora": "escola" ou "governo"
    # Se tipo_usuario="produtor": "fornecedor_individual", "grupo_informal" ou "grupo_formal"
    subtipo_usuario = mapped_column(String(50), nullable=False)

    # Localização (coordenadas GPS)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)

    role = mapped_column(String(100), nullable=True)  # Kept for backward compatibility

    # Novos campos para MVP
    status = mapped_column(String(50), default='active', nullable=False)  # active|disabled|pending_verification
    phone = mapped_column(String(20), nullable=True)
    last_login_at = mapped_column(TIMESTAMP, nullable=True)

    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    def __init__(self, **kwargs):
        if 'senha' in kwargs:
            senha_plana = kwargs.pop('senha')
            self.senha = pwd_context.hash(senha_plana)
        super().__init__(**kwargs)

    def verify_password(self, senha_plana):
        return pwd_context.verify(senha_plana, self.senha)
