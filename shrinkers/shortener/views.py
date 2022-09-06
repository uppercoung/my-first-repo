from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.http.response import JsonResponse
from shortener.models import Users
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from shortener.forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous User!"
    print("Logged in?", request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Anonymous User!"
    print(email)
    return render(request, "base.html")

def login_view(request): # POST가 Login을 위한 POST라서 Data를 집어 넣는게 아니라 입력 ID/PW를 POST 해서 검증
    if request.method == "POST": # ID/PW를 누르면 POST하는 것
        form = AuthenticationForm(request, request.POST)
        msg = ""
        if form.is_valid(): # Login 입력 ID/PW 형식이 정상적이면!
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password) # Users Data에 들어 있는지 검증
            if user is not None: # DB에 user가 조회 되면!
                msg = "로그인 성공"
                login(request, user)
                return redirect("index")
        else:
            msg = "올바른 유저ID와 패스워드를 입력하세요."
        return render(request, "login.html", {"form": form, "msg": msg})
    else: # 그냥 처음에 Login page를 방문하면 GET
        form = AuthenticationForm()
        for visible in form.visible_fields():
            visible.field.widget.attrs["placeholder"] = "유저ID" if visible.name == "username" else "패스워드"
            visible.field.widget.attrs["class"] = "form-control"
        return render(request, "login.html", {"form": form})
    
def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def users_view(request):
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})
