from django.http.response import JsonResponse
from shortener.models import Users
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous User!"
    print(email)
    print(request.user.is_authenticated)
    return render(request, "base.html", {"welcome_msg": f"Hello {email}", "hello": "world"})

@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        
        # user 객체를 넘겨줘도 자동으로 해당 객체의 name으로 인식
        # params: 쿼리스트링 값을 넘겨받을 때 이용. URL에서 넘겨받지 못할 때(쿼리 스트링 미 작성 시) abc, xyz에 None 들어간다
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method!"), status=201, safe=False)
