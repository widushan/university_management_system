from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Semester(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    

class Student(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    contact_no = models.CharField(max_length=15)
    personal_email = models.EmailField()
    nic_no = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=100)
    guardian_contact_no = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    entry_year = models.IntegerField()
    batch = models.CharField(max_length=20)
    university_email = models.EmailField()
    registration_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.registration_no})"
    

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.course_id} - {self.course_name}"
    

class Lecturer(models.Model):
    avatar = models.ImageField(upload_to='lecturer_avatars/')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField()
    university_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=100)

class LectureModule(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='modules')
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    

class DepartmentCourse(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.course_id} - {self.course_name}"

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    result = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.student.registration_no} - {self.course_id} - {self.result}"