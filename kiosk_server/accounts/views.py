import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import CustomUser, Membership
from .serializers import CustomUserSerializer, MembershipSerializer

class CustomUserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        user.IsDeleted = True
        user.save()
        return Response({'message': '사용자 프로필이 삭제되었습니다.'}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        name = request.data.get('name')
        password = request.data.get('password')
        
        if name:
            user.name = name
        if password:
            user.set_password(password)  # 비밀번호를 해시하여 저장합니다.

        user.save()

        # 사용자 정보를 다시 불러와서 직렬화합니다.
        serializer = CustomUserSerializer(user)
        
        return Response({'message': '프로필 수정 완료.', 'data': serializer.data}, status=status.HTTP_200_OK)

class MembershipView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        membership = Membership.objects.create(phone_number=phone_number)
        serializer = MembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if request.body:
            try:
                body_data = json.loads(request.body)
                phone_number = body_data.get('phone_number')
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone_number = None

        if phone_number:
            try:
                membership = Membership.objects.get(phone_number=phone_number)
                serializer = MembershipSerializer(membership)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Membership.DoesNotExist:
                return Response({'error': 'Membership not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            memberships = Membership.objects.all()
            serializer = MembershipSerializer(memberships, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, membership_ID):
        try:
            membership = Membership.objects.get(ID=membership_ID)
        except Membership.DoesNotExist:
            return Response({'error': '존재하지 않는 멤버십입니다.'}, status=status.HTTP_404_NOT_FOUND)

        earn_point = request.data.get('earn_point')
        use_point = request.data.get('use_point')

        if earn_point is not None:
            membership.total_point += int(earn_point)
        if use_point is not None:
            membership.total_point -= int(use_point)
            if membership.total_point < 0:
                return Response({'error': '포인트가 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        membership.save()
        serializer = MembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_200_OK)