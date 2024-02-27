from rest_framework.views import APIView
from .serializers import StudentSerializer
from .models import Student
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging
from .utils import EmailThread
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


logger = logging.getLogger('mylogger')

class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            student = Student.objects.all()
            serializer = StudentSerializer(student, many=True)
            logger.info('Data fetch successfully')
            
            return Response(data=serializer.data, status=200)
        except:
            logger.error('this is error log')
            return Response(data={'details':'There is an error fetch data'},status=400)
        
    def post(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Data insert successfully')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'You data feteching'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details':'testing email'})
            return Response(data=serializer.data, status=201)
        except:
            logger.error('insert error')
            return Response(data=serializer.errors, status=400)

class StudentDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            students = Student.objects.get(pk=pk)
            serializer = StudentSerializer(students)
            logger.info('fetch data')
            return Response(data=serializer.data, status=200)
        except:
            logger.error('fetching issue')
            return Response(data={'details':'fectching error'}, status=400)
        
    def put(self, request, pk=None):
        try:
            students = Student.objects.get(pk=pk)
            serializer = StudentSerializer(data=request.data, instance=students)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info('updated data')
            user_email = request.user.email
            subject = 'test email'
            message = 'You data feteching'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details': 'User Update successfully'})

            return Response(data=serializer.data, status=205)
        except Student.DoesNotExist as e:
            logger.error('No matching data found')
            return Response(data={'details':'not found'}, status=404)
        except Exception as e:
            print(e)
            logger.error('show error on updating time')
            return Response(data=serializer.errors, status=400)
    
    def delete(self, request, pk=None):
        try:
            students = Student.objects.get(pk=pk)
            students.delete()
            logger.info('Delete Successfully')
            user_email = request.data.get('email')
            subject = 'test email'
            message = 'You data feteching'
            if user_email:
                EmailThread(
                    subject = subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details':'User Delete succesfully'})
            return Response(data=None, status=204)
        except:
            logger.error('Delete time error')
            return Response(data={'details':'not found'}, status=400)

