from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.middleware.jwt_middleware import token_required
from app.utils.jwt_util import JwtUtil

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')



@auth_bp.route('/register', methods=['POST'])
def register():
   #register a new user
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Create user
        user, message = UserService.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone')
        )
        
        if not user:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


#Login Endpoint
@auth_bp.route('/login', methods=['POST'])
def login():

    try:
        data = request.get_json()
        
        # Validate required fields
        #if the data is missing return 400 
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password required'}), 400
        
        # Authenticate user
        result, message = UserService.authenticate_user(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if not result:
            return jsonify({'message': message}), 401
        
        return jsonify({
            'message': message,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get The Profile Endpoint
@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    
    try:
        # Get user ID from token 
        user_id = request.user_data.get('user_id')
        
        # Get user from database
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile retrieved successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# UPDATE PROFILE ENDPOINT

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
  
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Update user
        user, message = UserService.update_user(user_id, **data)
        
        if not user:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# CHANGE PASSWORD ENDPOINT

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
 
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Validate required fields
        if not data or not data.get('old_password') or not data.get('new_password'):
            return jsonify({'message': 'Old password and new password required'}), 400
        
        # Change password
        user, message = UserService.change_password(
            user_id,
            data.get('old_password'),
            data.get('new_password')
        )
        
        if not user:
            return jsonify({'message': message}), 400
        
        return jsonify({'message': message}), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# REFRESH TOKEN ENDPOINT

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
 
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'message': 'Refresh token required'}), 400
        
        # Verify refresh token
        payload = JwtUtil.verify_token(data.get('refresh_token'))
        
        if not payload or payload.get('type') != 'refresh':
            return jsonify({'message': 'Invalid refresh token'}), 401
        
        # Get user
        user = UserService.get_user_by_id(payload.get('user_id'))
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Generate new access token
        new_access_token = JwtUtil.generate_access_token(
            user_id=user.id,
            email=user.email,
            username=user.username,
            role=user.role.value
        )
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'access_token': new_access_token
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# LOGOUT ENDPOINT

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout user (token invalidation handled on frontend)
    
    Headers:
    {
        "Authorization": "Bearer <access_token>"
    }
    """
    return jsonify({'message': 'Logged out successfully'}), 200