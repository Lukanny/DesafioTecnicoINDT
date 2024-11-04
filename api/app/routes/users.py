from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from ..schemas import UserCreate, UserResponse, UserUpdate
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta
from flask_restx import Api, Resource, fields

users_bp = Blueprint('users', __name__)
api = Api(users_bp, doc='/docs', title='User Management API', description='API para gerenciamento de usuários')

# Definição dos modelos para documentação Swagger
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True, description='Primeiro nome'),
    'last_name': fields.String(required=True, description='Sobrenome'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Senha'),
    'access_level': fields.String(required=True, description='Nível de acesso'),
    'status': fields.String(description='Status do usuário')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Senha')
})

@api.route('/register')
class Register(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuário criado com sucesso')
    @api.response(400, 'Erro na criação do usuário')
    def post(self):
        """Registro de novo usuário"""
        try:
            user_data = UserCreate(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400
        except Exception as e:
            return {'errors': str(e)}, 400

        if User.query.filter_by(email=user_data.email).first():
            return {'message': 'Email já registrado'}, 400
        
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            access_level=user_data.access_level,
            status=user_data.status
        )
        user.set_password(user_data.password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'Usuário criado com sucesso'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login bem-sucedido')
    @api.response(401, 'Credenciais inválidas')
    def post(self):
        """Login de usuário"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity={'id': user.id, 'access_level': user.access_level},
                expires_delta=timedelta(hours=1)
            )
            return {'access_token': access_token}, 200
        return {'message': 'Credenciais inválidas'}, 401

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'Sucesso')
    @api.response(403, 'Acesso negado')
    def get(self):
        """Obter todos os usuários (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403
        
        users = User.query.all()
        users_data = [UserResponse.from_orm(user).dict() for user in users]
        return {'users': users_data}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuário criado com sucesso')
    @api.response(403, 'Acesso negado')
    @api.response(400, 'Erro na criação do usuário')
    def post(self):
        """Criar um novo usuário (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403

        try:
            user_data = UserCreate(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400
        except Exception as e:
            return {'errors': str(e)}, 400
        
        if User.query.filter_by(email=user_data.email).first():
            return {'message': 'Email já registrado'}, 400
        
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            access_level=user_data.access_level,
            status=user_data.status
        )
        user.set_password(user_data.password)
        db.session.add(user)
        db.session.commit()
        return UserResponse.from_orm(user).dict(), 201

@api.route('/<int:id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'Sucesso')
    @api.response(403, 'Acesso negado')
    @api.response(404, 'Usuário não encontrado')
    def get(self, id):
        """Obter detalhes de um usuário específico (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403
        
        user = User.query.get_or_404(id)
        return UserResponse.from_orm(user).dict(), 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'Usuário atualizado com sucesso')
    @api.response(403, 'Acesso negado')
    @api.response(400, 'Erro na atualização do usuário')
    @api.response(404, 'Usuário não encontrado')
    def put(self, id):
        """Atualizar um usuário específico (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403
        
        user = User.query.get_or_404(id)
        try:
            user_data = UserUpdate(**request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400
        except Exception as e:
            return {'errors': str(e)}, 400
        
        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        if user_data.email:
            if User.query.filter_by(email=user_data.email).first() and user.email != user_data.email:
                return {'message': 'Email já registrado'}, 400
            user.email = user_data.email
        if user_data.password:
            user.set_password(user_data.password)
        if user_data.access_level:
            user.access_level = user_data.access_level
        if user_data.status:
            user.status = user_data.status
        
        db.session.commit()
        return UserResponse.from_orm(user).dict(), 200

    @jwt_required()
    @api.response(200, 'Usuário deletado com sucesso')
    @api.response(403, 'Acesso negado')
    @api.response(404, 'Usuário não encontrado')
    def delete(self, id):
        """Deletar um usuário específico (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403
        
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Usuário deletado com sucesso'}, 200

@api.route('/stats')
class UserStats(Resource):
    @jwt_required()
    @api.response(200, 'Sucesso')
    @api.response(403, 'Acesso negado')
    def get(self):
        """Obter estatísticas de usuários (Admin apenas)"""
        current_user = get_jwt_identity()
        if current_user['access_level'] != 'admin':
            return {'message': 'Acesso negado'}, 403
        
        stats = db.session.query(
            User.access_level,
            User.status,
            db.func.count(User.id)
        ).group_by(User.access_level, User.status).all()
        
        result = []
        for access_level, status, count in stats:
            result.append({
                'access_level': access_level,
                'status': status,
                'count': count
            })
        
        return jsonify(result), 200
