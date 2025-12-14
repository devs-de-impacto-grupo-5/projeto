# models/Auditoria_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class EventoAuditoria(Base):
    """Eventos de auditoria do sistema"""
    __tablename__ = "eventos_auditoria"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    acao = mapped_column(String(100), nullable=False)  # create|update|delete|approve|reject|etc
    entidade_tipo = mapped_column(String(100), nullable=False)  # demanda|proposta|documento|etc
    entidade_id = mapped_column(Integer, nullable=True)
    dados_anteriores = mapped_column(JSON, nullable=True)
    dados_novos = mapped_column(JSON, nullable=True)
    ip_address = mapped_column(String(50), nullable=True)
    user_agent = mapped_column(String(500), nullable=True)
    detalhes = mapped_column(Text, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    user = relationship("User", back_populates="eventos_auditoria")
