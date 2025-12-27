from .models import Classroom, Subject, TimetableEntry, Teacher


def generate_school_timetable():
    # 1. Clear existing data
    TimetableEntry.objects.all().delete()

    classrooms = Classroom.objects.all()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    total_periods = 8
    break_period = 4

    for classroom in classrooms:
        subjects = list(Subject.objects.filter(classroom=classroom))
        # Tracking remaining periods for this class
        subject_counts = {s.id: s.periods_per_week for s in subjects}

        for day in days:
            daily_subjects = []  # To prevent same subject twice a day

            for period in range(1, total_periods + 1):
                if period == break_period:
                    TimetableEntry.objects.create(classroom=classroom, day=day, period_number=period, is_break=True)
                    continue

                # Try to assign a subject
                assigned = False
                # Sort subjects by remaining periods to prioritize heavy subjects
                available_subjects = sorted(subjects, key=lambda s: subject_counts[s.id], reverse=True)

                for sub in available_subjects:
                    if subject_counts[sub.id] > 0 and sub.id not in daily_subjects:
                        # CHECK TEACHER AVAILABILITY
                        teacher_busy = TimetableEntry.objects.filter(
                            day=day,
                            period_number=period,
                            subject__teacher=sub.teacher
                        ).exists()

                        if not teacher_busy:
                            TimetableEntry.objects.create(classroom=classroom, day=day, period_number=period,
                                                          subject=sub)
                            subject_counts[sub.id] -= 1
                            daily_subjects.append(sub.id)
                            assigned = True
                            break

                # If no subject fits (fallback), leave empty or assign any free subject
                if not assigned:
                    TimetableEntry.objects.create(classroom=classroom, day=day, period_number=period, subject=None)