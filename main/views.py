from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def home(request):
    return render(request, 'home.html')



def job_list(request):
    jobs = Job.objects.all().order_by('-date_posted')
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required(login_url='login')
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)

        user.save()
        messages.success(request,'Account created uccessfully!')
        return redirect('login')
    return render(request,'register.html')

    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login Successful!')
            return redirect('/')
    return render(request,'login.html')
       

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')






@login_required(login_url='login')
def recommend_jobs(request):
    user_input = request.GET.get('skills', '')  # user ka skill input
    
    jobs = Job.objects.all()
    if not user_input:
        return render(request, 'recommend.html', {'jobs': jobs, 'no_input': True})
    
    # Combine skills for similarity
    job_skills = [job.skills_required for job in jobs]
    job_titles = [job.title for job in jobs]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(job_skills + [user_input])
    
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    scores = list(enumerate(similarity[0]))
    ranked_jobs = sorted(scores, key=lambda x: x[1], reverse=True)
    
    recommended = [jobs[i] for i, score in ranked_jobs if score > 0]
    
    return render(request, 'recommend.html', {'jobs': recommended, 'skills': user_input})