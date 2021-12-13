from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if not serializer.is_valid():
      key, value = serializer.errors.popitem()
      if key == 'password':
        key = "رمز عبور: "
      elif key == 'username':
        key = 'نام کاربری: '
      elif key == 'email':
        key = 'ایمیل: '
      content = {'message': key+value[0]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if not serializer.is_valid():
      key, value = serializer.errors.popitem()
      if key == 'password':
        key = "رمز عبور: "
      elif key == 'username':
        key = 'نام کاربری: '
      elif key == 'email':
        key = 'ایمیل: '
      content = {'message': key+value[0]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)
    #serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user
