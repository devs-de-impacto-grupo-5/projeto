# models/Blockchain_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class RegistroBlockchain(Base):
    """Registro de contratos em blockchain"""
    __tablename__ = "registros_blockchain"

    id = mapped_column(Integer, primary_key=True)
    contrato_id = mapped_column(Integer, ForeignKey("contratos.id"), nullable=False, unique=True)
    hash_documento = mapped_column(String(255), nullable=False)  # SHA256 do contrato
    blockchain_network = mapped_column(String(50), nullable=False)  # ethereum|polygon|hyperledger|etc
    transaction_hash = mapped_column(String(255), nullable=True)  # Hash da transação blockchain
    block_number = mapped_column(Integer, nullable=True)
    wallet_address = mapped_column(String(255), nullable=True)
    status = mapped_column(String(50), default='pending', nullable=False)  # pending|confirmed|failed
    metadados_json = mapped_column(JSON, nullable=True)  # Metadados adicionais
    erro_mensagem = mapped_column(Text, nullable=True)
    registrado_em = mapped_column(TIMESTAMP, nullable=True)
    verificado_em = mapped_column(TIMESTAMP, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    contrato = relationship("Contrato", back_populates="registro_blockchain")
