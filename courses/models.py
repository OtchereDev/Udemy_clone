from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

class Course(models.Model):
    title=models.CharField(max_length=225)
    description=models.TextField()
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)
    rating=models.ManyToManyField('Rate',blank=True)
    sector=models.ForeignKey('Sector',on_delete=models.CASCADE)
    # author=models.ForeignKey(Author,on_delete=models.CASCADE)
    student_engaged_rating=models.IntegerField(default=0)
    language=models.CharField(max_length=225)
    course_length=models.CharField(default=0,max_length=20)
    course_sections=models.ManyToManyField('CourseSection',blank=True)
    comment=models.ManyToManyField('Comment',blank=True)

    def get_rating(self):
        if self.rating:
            ratings=self.rating.objects.all()
            rate=0
            for rating in ratings:
                rate+=rate.rate_number
            rate/=len(ratings)

            return rate

    def get_short_brief(self):
        return self.description[:100]


class Rate(models.Model):
    rate_number=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])


class Section(models.Model):
    section_title=models.CharField(max_length=225,blank=True,null=True)
    section_number=models.IntegerField(blank=True,null=True)
    episodes=models.ManyToManyField('Episode',blank=True)


class Episode(models.Model):
    title=models.CharField(max_length=225)
    file=models.FileField(upload_to='courses')
    length=models.FloatField(default=0)

    def get_video_length(self):
        # get video length here
        pass
    
    def save(self,*args, **kwargs):
        # self.length=self.get_video_length()
        return super().save(*args, **kwargs)

