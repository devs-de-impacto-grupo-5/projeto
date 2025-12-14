# models/Sistema_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class EventoAuditoria(Base):
    """Log de auditoria para rastreamento de ações"""
    __tablename__ = "eventos_auditoria"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    tipo_evento = mapped_column(String(100), nullable=False)  # login|logout|create|update|delete|approve|reject|etc
    entidade_tipo = mapped_column(String(100), nullable=True)  # users|demandas|propostas|contratos|etc
    entidade_id = mapped_column(Integer, nullable=True)
    dados_antes_json = mapped_column(JSON, nullable=True)
    dados_depois_json = mapped_column(JSON, nullable=True)
    ip_address = mapped_column(String(45), nullable=True)
    user_agent = mapped_column(Text, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    user = relationship("User", backref="eventos_auditoria")


class Notificacao(Base):
    """Notificações internas para usuários"""
    __tablename__ = "notificacoes"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tipo = mapped_column(String(100), nullable=False)  # info|warning|error|success
    titulo = mapped_column(String(255), nullable=False)
    mensagem = mapped_column(Text, nullable=False)
    link = mapped_column(String(500), nullable=True)  # URL para ação relacionada
    lida = mapped_column(Boolean, default=False)
    lida_em = mapped_column(TIMESTAMP, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    user = relationship("User", backref="notificacoes")
