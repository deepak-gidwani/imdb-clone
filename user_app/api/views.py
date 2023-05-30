from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app.models import *   # used for autogenerating auth token
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST',])
def registerations_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Registeration successfully'
            
            data['username'] = account.username
            data['email'] = account.email
            
            data['token'] = Token.objects.get(user=account).key
            # refresh = RefreshToken.for_user(account)  jwt ka part
            
            # data['token'] = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
            
        else:
            data = serializer.errors    
        return Response(data)

@api_view(['POST'])    
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
    
      