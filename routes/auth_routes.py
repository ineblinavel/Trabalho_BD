from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import AuthService

def init_auth_routes(auth_service: AuthService):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = auth_service.login(username, password)
            
            if user:
                session['user_id'] = user['id_usuario']
                session['username'] = user['username']
                session['role'] = user['role']
                session['referencia_id'] = user.get('referencia_id') # Adiciona referencia_id na sessão
                
                if user['role'] == 'admin':
                    return redirect('/ui/portal/admin')
                elif user['role'] == 'medico':
                    return redirect('/ui/portal/medico')
                elif user['role'] == 'enfermeiro':
                    return redirect('/ui/portal/enfermeiro')
                else:
                    return redirect('/')
            else:
                flash('Usuário ou senha inválidos', 'danger')
                
        return render_template('login.html')

    @auth_bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('auth.login'))

    return auth_bp
