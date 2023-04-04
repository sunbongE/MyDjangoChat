# 로그인 in Django

```django
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

```



# 각 코드 역할



## LoginRequiredMixin

로그인된 유저만 이용할 수 있게 이용에 제한을 주는 기능

로그인 안된 유저는 로그인 화면으로 보내고 로그인되면 입장시킨다.



## TemplateView

템플을 랜더링하여 HTML 페이지를 생성하는 뷰 클래스.

`template_name` 변수로 주소? 템플릿? 을 넘겨준다.



## CreateView

`CreateView`는 다음과 같은 변수를 포함합니다.

- `model`: 새로 생성될 객체의 모델 클래스를 지정합니다.
- ⭐`form_class`: 모델 클래스를 기반으로 생성된 폼 클래스를 지정합니다. 
  만약 폼 클래스를 따로 지정하지 않으면 `ModelForm` 클래스가 자동으로 생성됩니다.
- ⭐`template_name`: **렌더링할 템플릿 파일의 경로**를 지정합니다. 
  만약 지정하지 않으면 기본값으로 `"{앱 이름}/{모델 이름}_form.html"` 형식의 파일을 사용합니다.
- ⭐`success_url`: **새로운 객체 생성 후에 이동할 URL을 지정합니다.** 
  만약 지정하지 않으면 기본값으로 `get_absolute_url` 메서드가 정의된 모델 객체의 `get_absolute_url()` 메서드를 호출하여 URL을 생성합니다.
- `form_valid(form)`: 폼 유효성 검사를 통과한 경우 호출되는 메서드입니다. 새로운 객체를 생성하고 저장하는 로직을 구현할 수 있습니다.
- `form_invalid(form)`: 폼 유효성 검사를 통과하지 못한 경우 호출되는 메서드입니다. 폼 오류 메시지를 처리하는 로직을 구현할 수 있습니다.
- ⭐`extra_context`: **렌더링할 템플릿에 추가적으로 전달할 컨텍스트 변수를 딕셔너리 형태로 지정**할 수 있습니다.



## UserCreationForm

이 폼은 Django의 기본 인증 시스템에 내장되어 있으며, **사용자 이름**, **비밀번호**, **이메일** 등과 같은 필수 입력 필드를 가지고 있습니다.

UserCreationForm은 forms.ModelForm 클래스를 상속받아 구현되어 있습니다.
이 폼을 사용하면 간단하게 사용자 생성 폼을 구현할 수 있으며, 사용자가 입력한 정보를 검증하여 새로운 사용자를 생성합니다.
이 폼을 통해 생성된 사용자는 Django의 인증 시스템에서 사용되며, **로그인 등의 기능을 수행**할 수 있습니다.

UserCreationForm 클래스는 다른 폼 클래스와 마찬가지로, Django의 템플릿 시스템과 연동하여 사용할 수 있습니다. 
사용자가 입력한 데이터를 저장하기 위해서는 폼을 저장하는 과정이 필요하며, 
이때 Django의 모델 폼을 사용하면 **간편하게 저장**할 수 있습니다.



## reverse_lazy

```django
signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="partials/form.html",
    extra_context={
        "form_name": "회원가입",
        "submit_label": "회원가입",
    },
    success_url=reverse_lazy("accounts:login"), # 가입 후 로그인페이지로 이동
)
```



`reverse_lazy`는 URL 패턴 이름을 가지고 URL을 생성하는 함수입니다. 이 코드에서 `reverse_lazy`는 `success_url` 옵션에 사용되어, 회원가입에 성공한 후 사용자를 로그인 페이지로 이동시키는 데 사용됩니다.

하지만 `reverse` 대신 `reverse_lazy`를 사용한 이유는, `reverse` 함수는 실행되는 시점에서 URL 패턴을 검사하여 URL을 생성합니다. 이는 뷰가 처음 실행될 때가 아니라, URL 패턴이 처음 로드될 때 한 번만 실행됩니다. 따라서, `reverse` 함수는 프로젝트의 URL 패턴이 전부 로드되지 않은 상태에서 실행되면 오류가 발생할 수 있습니다.

반면에 `reverse_lazy`는 지연 실행(lazy evaluation)을 지원하여, URL 패턴이 전부 로드된 이후에 실행됩니다. 따라서 `reverse_lazy`를 사용하면, URL 패턴이 전부 로드되지 않은 상태에서 뷰가 실행되어도 문제가 발생하지 않습니다.

따라서, `reverse_lazy`를 사용하는 것은 안정성을 고려하는 좋은 습관입니다.

## LoginView, LogoutView

제공되는 기능

- LoginView
  - 로그인 폼 보여주기
  - 로그인 처리
  - 로그인 후 페이지 이동

- LogoutView
  - 로그아웃 처리
  - 로그라웃 후 페이지 이동

![image-20230404164438713](%EB%A1%9C%EA%B7%B8%EC%9D%B8_in_Django.assets/image-20230404164438713.png)

## .as_view()

Django에서 `as_view()`는 클래스 기반 뷰를 함수 기반 뷰로 변환하는 메서드입니다.

클래스 기반 뷰는 객체를 생성하여 처리하는 반면,
함수 기반 뷰는 뷰 함수를 호출하여 처리합니다. 
Django의 URL 매핑 시스템은 **함수 기반 뷰를 기본적으로 지원**하기 때문에, 
클래스 기반 뷰를 URL 매핑하기 위해서는 `as_view()`를 사용하여 함수 기반 뷰로 변환해야 합니다.

Q. 그럼 처음부터 함수기반 뷰로하지 왜 클래스 기반으로하는거..?



A. 

클래스 기반 뷰와 함수 기반 뷰는 각각의 장단점이 있기 때문에, 개발자가 상황에 따라 적절히 선택하여 사용해야 합니다.

클래스 기반 뷰는 다음과 같은 장점을 가집니다.

- 코드 재사용성이 높습니다.
- 객체지향 프로그래밍의 특징인 상속, 다형성 등을 활용하여 코드를 구성할 수 있습니다.
- 클래스 내부에 요청 처리 메서드(`get()`, `post()` 등)를 포함하여 요청 처리 로직을 구현할 수 있습니다.
- Django의 **제네릭 뷰(generic view)**를 사용할 수 있으며, 
  이를 통해 간단하게 CRUD(Create, Read, Update, Delete) 기능을 구현할 수 있습니다.

반면 함수 기반 뷰는 다음과 같은 장점을 가집니다.

- 코드가 간결하고 이해하기 쉽습니다.
- 뷰 함수는 순수 함수(pure function)로 작성할 수 있어서 테스트가 쉽습니다.
- Django에서 제공하는 데코레이터를 활용하여 뷰 로직을 구성할 수 있습니다.
- URL 매핑 시에 직접 뷰 함수를 지정할 수 있어서 클래스 기반 뷰보다 유연합니다.