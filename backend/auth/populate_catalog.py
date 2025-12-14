#!/usr/bin/env python3
"""
Script para popular o catálogo de produtos manualmente.
Execute: python populate_catalog.py
"""

import sys
from pathlib import Path

# Adiciona o diretório auth ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from db.db import get_session_local, create_tables
from services.seed_catalog import seed_catalogo

def main():
    print("=" * 50)
    print("Populando catálogo de produtos...")
    print("=" * 50)

    # Create tables first
    create_tables()
    
    # Get SessionLocal and create a session
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        seed_catalogo(db)
        print("\n" + "=" * 50)
        print("✓ Catálogo populado com sucesso!")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Erro ao popular catálogo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
