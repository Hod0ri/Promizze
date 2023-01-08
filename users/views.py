import json
import uuid

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.core.serializers import serialize


# Check Validation Token
def checkTokenValidation(token):
    # Check Incorrect Token
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    # Decode Payload and Token Expiration
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token Expire')

    return payload


# 사용자 회원가입 API View
class RegisterView(APIView):
    def post(self, request):

        # Set Id <- Minecraft UUID
        request.data.update({
            "id": str(uuid.uuid4())
        })
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


# 사용자 로그인 API View
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # Find Users
        user = User.objects.filter(email=email).first()

        # Check Present User
        if user is None:
            raise AuthenticationFailed('User Not Found')
        # Password Checking
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        # Set Payload
        payload = {
            'id': user.id,
            'role': user.userRole,
            # Expriration 60m
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        # Set Cookie
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


# 사용자 정보 API View
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        payload = checkTokenValidation(token)

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


# 사용자 Logout API View
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


# 사용자 권한 수정 API View
class EditUserRoleView(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')
        payload = checkTokenValidation(token)
        user = User.objects.filter(id=payload['id']).first()
        # Check Permission
        if not user.userRole == 'Owner':
            raise AuthenticationFailed('Permission Denied')
        if request.GET.get('name') is None:
            raise ValueError('Could\'nt found User Name')
        else:
            name = request.GET.get('name')

        modifiedUser = User.objects.filter(name=name).first()
        modifiedUser.userRole = request.data['role']
        modifiedUser.save()

        return Response({
            'message': 'success'
        })


# 사용자 탈퇴 API View
class ExitSiteView(APIView):
    def delete(self, request):
        token = request.COOKIES.get('jwt')
        payload = checkTokenValidation(token)
        user = User.objects.filter(id=payload['id']).first()
        user.delete()

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


# 사용자 정보 조회 (전체 리스트)
class GetUserListView(APIView):
    def get(self, request):
        origin_UserList = User.objects.all()
        serializedList = serialize("json", origin_UserList)
        serializedList = json.loads(serializedList)
        return JsonResponse(serializedList, safe=False)


# 사용자 정보 조회 (단건 조회)
class GetUserInfoByName(APIView):
    def get(self, request):
        username = request.GET['name']
        selectedUser = User.objects.filter(name=username)
        serializedUser = serialize("json", selectedUser)
        serializedUser = json.loads(serializedUser)
        return JsonResponse(serializedUser, safe=False)