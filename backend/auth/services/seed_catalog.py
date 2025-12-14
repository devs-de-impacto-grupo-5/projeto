
from sqlalchemy.orm import Session
from models.Catalogo_model import CatalogoProduto, Unidade
from models.User_model import User
from models.PerfilProdutor_model import PerfilProdutor
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def seed_catalogo(db: Session):
    print("Seeding Catalog data...")
    try:
        # Seed Unidades
        unidades = [
            {"id": 1, "codigo": "kg", "nome": "Quilograma", "tipo": "mass"},
            {"id": 2, "codigo": "un", "nome": "Unidade", "tipo": "count"},
            {"id": 3, "codigo": "lt", "nome": "Litro", "tipo": "volume"},
            {"id": 4, "codigo": "cx", "nome": "Caixa", "tipo": "count"}
        ]
        for u_data in unidades:
            existing = db.query(Unidade).filter(Unidade.id == u_data["id"]).first()
            if not existing:
                db.add(Unidade(**u_data))
                print(f"Added Unidade: {u_data['nome']}")
        
        db.flush()

        # Seed Produtos (Catalogo)
        produtos = [
            {"id": 1, "nome": "Arroz Tipo 1", "categoria": "graos", "unidade_padrao_id": 1},
            {"id": 2, "nome": "Feijão Preto", "categoria": "graos", "unidade_padrao_id": 1},
            {"id": 3, "nome": "Leite Integral", "categoria": "laticinios", "unidade_padrao_id": 3},
            {"id": 4, "nome": "Banana Prata", "categoria": "hortifruti", "unidade_padrao_id": 1}
        ]
        for p_data in produtos:
            existing = db.query(CatalogoProduto).filter(CatalogoProduto.id == p_data["id"]).first()
            if not existing:
                db.add(CatalogoProduto(**p_data))
                print(f"Added Produto Catalogo: {p_data['nome']}")

        db.commit()
        print("Catalog seeding complete.")
    except Exception as e:
        print(f"Error seeding catalog: {e}")
        db.rollback()
