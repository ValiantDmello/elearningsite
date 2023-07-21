from datetime import timedelta

import stripe
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from elearningsite import settings
from .forms import *
from .models import *
from django.urls import reverse



# Create your views here.
class HomepageView(View):

    def get(self,request,*args,**kwargs):
        rec_courses = HomepageRec.objects.all()
        courses = Course.objects.filter(is_featured=True)
        top_courses = Course.objects.filter(is_featured=False)
        content = {
            "rec_courses": rec_courses,
            "courses": courses,
            "top_courses": top_courses,

        }
        return render(request,'elearning/homepage.html',content)


def courselist(request):
    form=SearchForm()
    courses = Course.objects.all()
    content = {
        'courses':courses,
        'form':form,
    }
    return render(request, 'elearning/courselist.html', content)


class CourseDetailView(View):
    def get(self,request,*args,**kwargs):
        course = get_object_or_404(Course,pk=self.kwargs['course_id'])

        try:
            student = Student.objects.get(pk=request.user.id)
            CourseEnrollment.objects.get(student=student,course=course)
            is_enrolled = True
        except:
            is_enrolled = False

        content = {
            'course': course,
            'is_enrolled':is_enrolled
        }
        return render(request,'elearning/coursedetail.html',content)

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs['course_id']
        student = Student.objects.get(pk=request.user.id)
        course = Course.objects.get(pk=course_id)
        data = {
            'student': student,
            'course': course,
            'enrollment_type': "Premium"
        }
        enroll_form = EnrollForm(data)
        if enroll_form.is_valid():
            enroll_form.save()
        return redirect(reverse('elearning:coursedetail',args=[course_id]))

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            student = Student.objects.get(username=username)
            request.session["avatar"] = str(student.avatar.url)
            request.session["is_premier"]=student.is_premier
            return redirect('elearning:homepage')
        else:
            # Invalid login credentials, return error message
            return render(request, 'elearning/login.html', {'error': 'Invalid username or password'})

    return render(request,'elearning/login.html')


@login_required(login_url='elearning:login')
def signout(request):
    logout(request)
    return redirect('elearning:homepage')

def signup(request):
    error = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            #error = 'Success'
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            user = authenticate(request,username=username,password=password)
            login(request, user)
            student = Student.objects.get(username=username)
            request.session["avatar"] = str(student.avatar.url)
            request.session["is_premier"] = student.is_premier
            return redirect('elearning:homepage')

        else:
            errors = form.errors
            return render(request, 'elearning/signup.html', {'form': form, 'errors': errors})
    else:
        form = SignUpForm()

    return render(request,'elearning/signup.html',{'form':form,'error':error})


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_type = self.kwargs['type']
        item_id = self.kwargs['item_id']
        images = []
        description = ''
        print(item_id)
        if payment_type == 'c':
            item = Course.objects.get(id=item_id)
            description = 'By: %s %s'%(item.teacher.first_name,item.teacher.last_name)
            images = ['https://wiki.djcsyn.top/download/attachments/4718593/course-default.png']
        elif payment_type == 'p':
            item = PremiePlan.objects.get(pk=item_id)
            description = '%s days Premier plan' % item.days
            print(item)
        else:
            # Handle invalid type
            pass

        if request.user.is_authenticated:
            domain = "https://yourdomain.com"
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"

            success_url = f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}&type={payment_type}&id={item.id}"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'unit_amount': int(item.price*100),
                        'product_data': {
                            'name': item.name,
                            'images': images,
                            'description': description,

                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=domain + '/cancel/',
            )
            checkout_session.success_url.replace("{CHECKOUT_SESSION_ID}", checkout_session.id)
            #print(checkout_session.id)
            return redirect(checkout_session.url)
        else:
            return redirect('elearning:login')

class SuccessView(TemplateView):
    template_name = "elearning/success.html"

    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_type = request.GET.get('type')
        item_id = request.GET.get('id')


        if session.payment_status == 'paid':
            student = Student.objects.get(id=request.user.id)
            if payment_type == 'c':
                course = Course.objects.get(id=item_id)
                Payment.objects.create(
                    time=timezone.now(),
                    student=student,
                    type=payment_type,  # use the type from the URL
                    course=course,
                    status='1',
                )

            elif payment_type == 'p':
                plan = PremiePlan.objects.get(id=item_id)
                Payment.objects.create(
                    time=timezone.now(),
                    student=student,
                    type=payment_type,  # use the type from the URL
                    plan=plan,
                    status='1',
                )
                student.premier_expiration = datetime.date.today() + timedelta(days=plan.days)
                # Save the changes
                student.save()
                request.session["is_premier"] = True
            else:
                pass


        return render(request, self.template_name)

class CancelView(TemplateView):
    template_name = "elearning/cancel.html"

def premier(request):
    plans = PremiePlan.objects.all()
    return render(request,'elearning/premierplan.html',{"plans":plans})


@login_required(login_url='elearning:login')
def profile(request):
    student = Student.objects.get(id=request.user.id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            msg = 'Successfully updated your profile.'
            request.session["avatar"] = str(student.avatar.url)
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=student)
            return render(request, 'elearning/profile.html', {"student": student, "user_form": user_form, "profile_form": profile_form, "msg": msg})
        else:
            errors = user_form.errors
            errors.update(profile_form.errors)
            return render(request, 'elearning/profile.html', {"student": student, "user_form": user_form, "profile_form": profile_form, "errors": errors})
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=student)

    return render(request, 'elearning/profile.html', {"student": student, "user_form": user_form, "profile_form": profile_form})


@login_required(login_url='elearning:login')
def mypremier(request):
    exp_date = ''
    student = Student.objects.get(pk=request.user.id)
    is_premier = student.is_premier
    if is_premier:
        exp_date = student.premier_expiration

    return render(request,'elearning/mypremier.html',{"is_premier":is_premier,"exp_date":exp_date})

@login_required(login_url='elearning:login')
def mycourses(request):
    student = Student.objects.get(pk=request.user.id)
    enrolled_courses = CourseEnrollment.objects.filter(student=student)
    return render(request,'elearning/mycourses.html',{"enrolled_courses":enrolled_courses})

def search(request):
    if request.method == 'POST':
        print('if block post')
        form = SearchForm(request.POST)
        results = ''
        if form.is_valid():
            search = form.data['name']
            # print(search)
            results = (Course.objects.filter(name__contains=search))
            if not results:
                return render(request, 'elearning/nosearch.html', {'error': 'No results found'})
            form = SearchForm()
    else:
        print('else block post')
        form = SearchForm()
        results = ''
    return render(request, 'elearning/search.html', {'form': form, 'results': results})

@login_required(login_url='elearning:login')
def teacher_portal(request):
    teacher = get_object_or_404(Student, pk=request.user.id)
    courses = Course.objects.filter(teacher=teacher)
    print(courses)
    return render(request, 'elearning/teacherportal.html', {'courses': courses})

@login_required(login_url='elearning:login')
def add_course(request):
    heading = "Please enter details for new course: "
    if request.method == 'POST':
        form = AddCourseForm(request.POST, request.FILES)  # Add request.FILES here
        teacher = get_object_or_404(Student, pk=request.user.id)
        form.instance.teacher = teacher
        if form.is_valid():
            course = form.save()
            return HttpResponseRedirect(reverse('elearning:teacher-portal'))
        else:
            print(form.errors)
            return HttpResponse("Invalid data")
    else:
        form = AddCourseForm()
        return render(request, 'elearning/add_course.html', {'form': form, 'heading': heading})

@login_required(login_url='elearning:login')
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            # Redirect to the course detail page or any other page you wish
            return redirect('elearning:teacher-viewcourse', course_id=course.id)
    else:
        form = AddCourseForm(instance=course)
        return render(request, 'elearning/edit_course.html', {'form': form, 'course': course})


@login_required(login_url='elearning:login')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return HttpResponseRedirect(reverse('elearning:teacher-portal'))

@login_required(login_url='elearning:login')
def teacher_viewcourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    categories = course.category.all()
    categories = list(categories.values_list('name', flat=True))
    return render(request, 'elearning/teacher_viewcourse.html', {'course': course, 'categories': categories})