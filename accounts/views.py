from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin  # 로그인 상태만 허용하는 기능
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Create your views here.
signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="partials/form.html",
    extra_context={
        "form_name": "회원가입",
        "submit_label": "회원가입",
    },
    success_url=reverse_lazy("accounts:login"), # 가입 후 로그인페이지로 이동
)

login = LoginView.as_view(
    # 랜더링될 페이지 경로 설정
    template_name="partials/form.html",
    # 템플릿에서 사용할 context data
    extra_context={
        "form_name": "로그인",
        "submit_label": "로그인",
    },
)

logout = LogoutView.as_view(
    # 로그아웃 완료 후 이동할 페이지 설정
    next_page="accounts:login",
)


# 프로필 뷰 구현 로그인 상태에서만 허용(LoginRequiredMixin)
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


profile = ProfileView.as_view()
