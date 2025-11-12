from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPE = (
        ('Full-time','Full-time'),
        ('Part-time','Part-time'),
        ('Internship','Internship')
        
    )
    
    title =models.CharField(max_length=200)
    company =models.CharField(max_length=100)
    location =models.CharField(max_length=100)
    job_type =models.CharField(max_length=50, choices=JOB_TYPE)
    description =models.TextField()
    skills_required = models.CharField(max_length=200, default='Python, Django')
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    

