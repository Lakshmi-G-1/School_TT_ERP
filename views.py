from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Classroom, Teacher, Subject, TimetableEntry
import random


@login_required
def dashboard(request):
    return render(request, 'timetable/dashboard.html')


@login_required
def generate_timetable_view(request):
    if request.method == "POST":
        # Clear old data
        TimetableEntry.objects.all().delete()

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = range(1, 9)  # 1, 2, 3, 4, 5, 6, 7, 8
        classrooms = Classroom.objects.all()
        teachers = list(Teacher.objects.all())

        if not teachers or not classrooms:
            messages.error(request, "Please add teachers and classrooms in Admin first!")
            return redirect('dashboard')

        for day in days:
            for period in periods:
                # Keep track of which teachers are already busy this period
                busy_teachers = []

                for classroom in classrooms:
                    # Filter teachers who teach at least one subject
                    available_teachers = [t for t in teachers if t not in busy_teachers and t.subjects.exists()]

                    if available_teachers:
                        selected_teacher = random.choice(available_teachers)
                        selected_subject = random.choice(selected_teacher.subjects.all())

                        TimetableEntry.objects.create(
                            classroom=classroom,
                            teacher=selected_teacher,
                            subject=selected_subject,
                            day=day,
                            period=period
                        )
                        busy_teachers.append(selected_teacher)

        messages.success(request, "Successfully generated 8 periods for all classes!")
        return redirect('dashboard')


@login_required
def view_timetable(request):
    classroom_id = request.GET.get('classroom')
    teacher_id = request.GET.get('teacher')

    entries = TimetableEntry.objects.all()

    if classroom_id:
        entries = entries.filter(classroom_id=classroom_id)
    if teacher_id:
        entries = entries.filter(teacher_id=teacher_id)

    context = {
        'entries': entries,
        'classrooms': Classroom.objects.all(),
        'teachers': Teacher.objects.all(),
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'periods': range(1, 9),
    }
    return render(request, 'timetable/view_timetable.html', context)