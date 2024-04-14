from .models import User

def increase_score():

    user = User.objects.first()
    user.score += 200
    user.save()
    print(f"{user.username} score increased by 200 , job done")
    
     