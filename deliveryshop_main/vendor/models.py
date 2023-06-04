from django.db import models
from useraccounts.utils import send_notification
from useraccounts.models import User, UserProfile


class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_name= models.CharField(max_length=50)
    #adding slug here
    vendor_slug = models.SlugField(max_length=100, unique=True)  
    # behind this there is one folder called media
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default = False)
    created_At = models.DateTimeField(auto_now_add = True)
    mnodified_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.vendor_name
    def save(self,*args,**kwargs):
        if self.pk is not None:

            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template ='useraccounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # sending notification email
                    mail_subject = "congratulations! your restaurant has been approved"
                    send_notification(mail_subject,mail_template,context)
                else: 
                    # send notification email
                    mail_subject="we're sorry! you are not eligible for publishing your food menu"
                    send_notification(mail_subject,mail_template,context)

        return super(Vendor,self).save(*args,**kwargs)