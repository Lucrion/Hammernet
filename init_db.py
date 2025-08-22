#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import get_db, Base, engine
from models import UsuarioDB
from auth import hash_contraseña
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_admin_user():
    try:
        # Crear las tablas si no existen
        Base.metadata.create_all(bind=engine)
        
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Verificar si el usuario admin ya existe
        admin = db.query(UsuarioDB).filter(UsuarioDB.username == 'admin').first()
        if admin:
            print('El usuario administrador ya existe')
            return
        
        # Crear usuario administrador
        admin_password = os.getenv('ADMIN_PASSWORD', '123')  # Contraseña por defecto: 123
        admin_user = UsuarioDB(
            nombre='Administrador',
            username='admin',
            password=hash_contraseña(admin_password),
            role='administrador'
        )
        
        db.add(admin_user)
        db.commit()
        print('Usuario administrador creado exitosamente')
        
    except Exception as e:
        print(f'Error al crear usuario administrador: {str(e)}')

if __name__ == '__main__':
    create_admin_user()