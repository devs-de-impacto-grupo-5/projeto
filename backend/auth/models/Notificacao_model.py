# models/Notificacao_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, Boolean
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Notificacao(Base):
    """Notificações para usuários"""
    __tablename__ = "notificacoes"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tipo = mapped_column(String(50), nullable=False)  # proposta_recebida|documento_aprovado|demanda_publicada|etc
    titulo = mapped_column(String(255), nullable=False)
    mensagem = mapped_column(Text, nullable=False)
    lida = mapped_column(Boolean, default=False)
    link_acao = mapped_column(String(500), nullable=True)  # URL para ação relacionada
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    lida_em = mapped_column(TIMESTAMP, nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="notificacoes")
