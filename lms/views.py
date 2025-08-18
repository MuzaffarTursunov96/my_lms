from django.shortcuts import render,get_object_or_404
from quiz.models import CourseItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Blogs, Course , Tutor,Article, CourseSection,Lecture
from account.decorators import unauthenticated_user,allowed_users
from django.db.models import Prefetch
from quiz.models import Quiz
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseSerializer

# Create your views here.



def index(request):
    blogs = Blogs.objects.filter(page_type='basic_page')
    hero_section = blogs.filter(blog_type='online_platform_education').first()
    global_education = blogs.filter(blog_type='global_education').first()
    top_course = blogs.filter(blog_type='top_course').first()
    course = Course.objects.filter(is_preview=True)[:3]
    tutors = Tutor.objects.all()[:4]
    articles = Article.objects.all()[:3]


    context = {
        'hero_section': hero_section,
        'global_education': global_education,
        'top_course': top_course,
        'courses': course,
        'tutors': tutors,
        'articles': articles,
    }
    return render(request, 'index.html',context)


def login(request):
    return render(request,'account/login.html')

def popular_courses(request):
    courses = Course.objects.filter(rating__gte=4.5)[:12]
    context = {
        'courses': courses,
    }
    return render(request, 'course/courses.html',context)


def contact(request):
    return render(request, 'contact.html')

def team(request):
    tutors = Tutor.objects.all()[:8]
    context ={
        'tutors':tutors
    }
    return render(request, 'team.html',context)

def team_details(request,id):
    tutor = Tutor.objects.get(id=id)
    courses = Course.objects.filter(is_preview=True)[:3]
    
    context = {
        'tutor':tutor,
        'courses':courses
    } 
    return render(request, 'team-details.html',context)

def about(request):
    tutors = Tutor.objects.all()[:8]
    context ={
        'tutors':tutors
    }
    return render(request, 'about.html',context)


@api_view(['GET'])
def course_detail(request, id):
    course = get_object_or_404(Course.objects.prefetch_related('sections'), id=id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@login_required(login_url='login')
def lecture(request, id):
    course = get_object_or_404(Course, id=id)

    # print(course,course.sections.all())

    sections = []
    for section in course.sections.all():  # use related_name='sections' in CourseSection
        items_qs = CourseItem.objects.filter(section=section).select_related('content_type').order_by('order')

        # Filter out orphans & duplicates
        seen_ids = set()
        valid_items = []
        for item in items_qs:
            model_class = item.content_type.model_class() if item.content_type else None
            if not model_class:
                continue
            if not model_class.objects.filter(pk=item.object_id).exists():
                continue  # orphan
            if (item.content_type_id, item.object_id) in seen_ids:
                continue  # duplicate
            seen_ids.add((item.content_type_id, item.object_id))
            valid_items.append(item)

        section.items = valid_items
        sections.append(section)
    
    
    
    context ={
        'course': course,
        'sections': sections
    }
    

    return render(request, 'course/lecture.html', context)





@login_required(login_url='login')
def clear_course_item(request):
    invalid_items = []

    for ci in CourseItem.objects.all():
        model_class = ci.content_type.model_class() if ci.content_type else None
        if not model_class:
            # ContentType row missing
            invalid_items.append(ci)
            continue
        
        if not model_class.objects.filter(pk=ci.object_id).exists():
            # Related object missing
            invalid_items.append(ci)

    # Delete them
    for ci in invalid_items:
        print(f"Deleting: {ci}")
        ci.delete()
    return render(request, 'course/quiz.html')




def find_program(request):
    return render(request, 'find-program.html')

def program_details(request,id):
    return render(request, 'program-details.html')

def course_details(request,id):
    return render(request, 'course/course-details.html')

def event_details(request,id):
    return render(request, 'event-details.html')

def become_tutor(request):
    return render(request, 'become-tutor.html')

def blog_details(request,id):
    return render(request, 'blog-details.html')

def course_details_v2(request,id):
    return render(request, 'course/course-details-free.html')




def search(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()

    paginator = Paginator(courses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'courses': page_obj,
    }
    return render(request, 'course/search_course.html',context)