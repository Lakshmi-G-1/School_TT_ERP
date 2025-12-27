import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from timetable.models import Profile, Classroom, Subject, Teacher, TimetableEntry


def seed_data():
    print("🌱 Seeding updated data...")

    # 1. Create Admin
    admin_user, _ = User.objects.get_or_create(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    Profile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})

    # 2. Create Classrooms
    c1, _ = Classroom.objects.get_or_create(name='Class 10', section='A')
    c2, _ = Classroom.objects.get_or_create(name='Class 10', section='B')

    # 3. Create Subjects
    math, _ = Subject.objects.get_or_create(name='Mathematics', code='MATH101')
    sci, _ = Subject.objects.get_or_create(name='Science', code='SCI101')

    # 4. Create Teachers
    # Teacher 1
    t1_user, _ = User.objects.get_or_create(username='math_teacher')
    t1_user.set_password('pass123')
    t1_user.save()
    t1_profile, _ = Profile.objects.get_or_create(user=t1_user, role='teacher')
    teacher1, _ = Teacher.objects.get_or_create(profile=t1_profile)
    teacher1.subjects.add(math)

    # Teacher 2
    t2_user, _ = User.objects.get_or_create(username='sci_teacher')
    t2_user.set_password('pass123')
    t2_user.save()
    t2_profile, _ = Profile.objects.get_or_create(user=t2_user, role='teacher')
    teacher2, _ = Teacher.objects.get_or_create(profile=t2_profile)
    teacher2.subjects.add(sci)

    # 5. Create Timetable Entries
    TimetableEntry.objects.get_or_create(
        classroom=c1, day='Monday', period=1,
        defaults={'teacher': teacher1, 'subject': math}
    )

    print("✅ Seeding complete! Login with admin/admin123")


if __name__ == '__main__':
    seed_data()