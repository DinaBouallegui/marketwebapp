from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    print(created)
    if created:
        print('create the user profile')
        UserProfile.objects.create(user=instance)
    else: 
        try: 
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #create the user profile if it doesnt exist
            UserProfile.objects.create(user=instance)
            #print("profile wasn't existing but I created one")
        #print('user is updated')

#creating a pre saved signal for the User
def pre_save_profile_receiver(sender,instance,**kwargs):
    pass
