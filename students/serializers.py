from rest_framework import serializers
from .models import Department, Student, Subject
from users.serializers import UserSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'department', 'department_name',
                  'age', 'address', 'phone', 'enrolled_date']


class StudentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['username', 'email', 'first_name', 'last_name', 'password',
                  'student_id', 'department', 'age', 'address', 'phone']

    def create(self, validated_data):
        from users.models import CustomUser
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
            'password': validated_data.pop('password'),
            'role': CustomUser.ROLE_STUDENT,
        }
        user = CustomUser.objects.create_user(**user_data)
        return Student.objects.create(user=user, **validated_data)
