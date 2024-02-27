from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger('mylogger')

class UserAPI(APIView):
    def get(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info('user created successfully')
            return Response(data=serializer.data, status=201)
        except:
            logger.error('user creating time error')
            return Response(data=serializer.errors, status=404)
