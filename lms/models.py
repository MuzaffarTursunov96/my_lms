from django.db import models
from account.models import User
from datetime import timedelta

# Create your models here.

class Blogs(models.Model):
    BLOG_TYPE_CHOICES = [
        ('online_platform_education', 'Online Platform Education'),
        ('top_categories', 'Top Categories'),
        ('global_education', 'Global Education'),
        ('top_course', 'Top Course'),
        ('becoming_a_tutor', 'Becoming a Tutor'),
    ]
    PAGE_TYPE_CHOICES =[
        ('basic_page', 'Главный'),
    ]
    title = models.CharField(max_length=200)
    page_type = models.CharField(max_length=50, choices=PAGE_TYPE_CHOICES, blank=True, null=True)  # New field for page type
    blog_type = models.CharField(max_length=50, choices=BLOG_TYPE_CHOICES,blank=True, null=True)  # New field for blog type
    description = models.TextField()
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text4 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text5 = models.TextField(blank=True, null=True)  # New helper text field
    created_at = models.DateTimeField(auto_now_add=True)  # New date field
    image = models.ImageField(upload_to='pages/images/', null=True, blank=True)  # New image field
    vimeo_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)  # New category field
    start_date = models.DateField(blank=True, null=True) 
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    topic = models.CharField(max_length=200, blank=True, null=True) 
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    organiser_full_name =  models.CharField(max_length=200, blank=True, null=True)
    organiser_email = models.EmailField(blank=True, null=True)
    organiser_phone = models.CharField(max_length=15, blank=True, null=True)
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    image = models.ImageField(upload_to='pages/images/', null=True, blank=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)  # New date field

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title
    



class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    experience_years = models.PositiveIntegerField()
    lessons_completed = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)

    profile_image = models.ImageField(upload_to='tutors/', null=True, blank=True)

    social_facebook = models.URLField(blank=True, null=True)
    social_twitter = models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  # New date field
    

    def __str__(self):
        return self.name


class Qualification(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_qualifications',blank=True,null=True)
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    institution = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.year} - {self.title} -{self.institution}"



class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"



class Course(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)  # Foreign key to Tutor
    course_type = models.CharField(max_length=100,blank=True)  # e.g., "Online", "In-person", "Hybrid"
    tags = models.TextField(blank=True)  # e.g., "English, Math, Science"
    duration = models.CharField(max_length=100)  # e.g., "4 weeks"
    weekly_study = models.CharField(max_length=100)  # e.g., "11 Hours"
    student_count = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g., 180.00
    payment_period = models.CharField(max_length=50, default="month")

    course_image = models.ImageField(upload_to='courses/images/', null=True, blank=True)
    preview_image = models.ImageField(upload_to='courses/images/', null=True, blank=True)
    vimeo_url = models.URLField(blank=True, null=True)  # URL to the Vimeo video
    is_preview = models.BooleanField(default=False)

    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  # New date field

    def __str__(self):
        return self.title


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(blank=True, default=1)


    def __str__(self):
        return self.title
    
    @property
    def total_duration(self):
        total = timedelta()
        # We can access the lectures in this specific section using 'lectures'
        # because of the `related_name` on the Lecture model's ForeignKey
        for lecture in self.lectures.all():
            if lecture.duration:
                total += lecture.duration
        return total

    @property
    def formatted_total_duration(self):
        # This property formats the total duration into a readable string
        total_seconds = int(self.total_duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return f"{minutes:02}:{seconds:02}"


class Lecture(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE,related_name='lectures')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.DurationField()

    def __str__(self):
        return self.title
    
    @property
    def formatted_duration(self):
        if self.duration is None:
            return ""
        total_seconds = int(self.duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return f"{minutes:02}:{seconds:02}"

class CourseBulletPoint(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='bullet_points')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    



class Review(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField()
    show = models.BooleanField(default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
