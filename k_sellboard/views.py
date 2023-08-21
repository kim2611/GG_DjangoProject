from django.shortcuts import render, redirect, get_object_or_404
from k_sellboard.models import Product
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from .models import Product, Comment

from n_order.forms import RegisterForm as OrderForm

from django.http import Http404
from .forms import *

from django.shortcuts import render

from django.contrib.auth import get_user_model
from bcuser.models import Bcuser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils import timezone





# Create your views here.
class ProductList(ListView):
    model=Product
    template_name='k_sell_board.html'
    context_object_name='product_list'
    paginate_by=10
    ordering = ['-register_date']

    def get_queryset(self):
        category_filter = self.request.GET.get('category')
        search_query = self.request.GET.get('search_query')

        chats = Product.objects.all().order_by("-register_date")

        if category_filter and category_filter != '전체':
            chats = chats.filter(category=category_filter)

        if search_query:
            chats = chats.filter(name__icontains=search_query)

        return chats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChatSearchForm(self.request.GET)
        return context

@method_decorator(login_required, name='dispatch')
class ProductCreate(FormView):
    template_name='k_register_sell.html'
    form_class=RegisterForm
    success_url='/sellboard/'

    def form_valid(self, form):
        product = form.save(commit=False)
        bcuser = Bcuser.objects.get(email=self.request.session.get('user'))
        product.writer = bcuser
        product.save()

        return super().form_valid(form)

def board_vote(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    product = Product.objects.get(pk=pk)
    user = Bcuser.objects.get(email=request.session.get('user')) # 현재 로그인한 사용자
    
        # 중복 추천 확인
    if user in product.jjims.all():
        product.jjim -= 1  # 추천수 감소
        product.jjims.remove(user)  # 사용자를 추천한 사용자 목록에서 제거
        is_jjimed = False # 추천 취소됨
    else:
        product.jjim += 1  # 추천수 증가
        product.jjims.add(user)  # 해당 사용자를 추천한 사용자 목록에 추가
        is_jjimed = True  # 추천됨
        
    product.save()
    return redirect('product_detail', pk=product.pk)

class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'k_sell_detail.html'

# 댓글 기능
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        product.views += 1
        product.save()
        is_jjimed = False

        try:
            user = Bcuser.objects.get(email=request.session.get('user'))
            is_jjimed = user in product.jjims.all()
        except Bcuser.DoesNotExist:
            user=""
            

        comments = Comment.objects.filter(post=product)
        comment_form = CommentForm()
        context = {
            'product': product,
            'comment_form': comment_form,
            'comments': comments,
            'is_jjimed' : is_jjimed,
            'user' : user
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        product = self.get_object()  # product 변수 정의
        

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = product
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('product_detail', pk=product.pk)
        else:
            comment_form = CommentForm()
        context = {
            'product': product,
            'comment_form': comment_form,
        }

        return render(request, self.template_name, context)



def post_update(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    
    try:
        chat = Product.objects.get(pk=pk)
    except Product.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
        raise Http404('게시글을 찾을 수 없습니다.')
    

    if Bcuser.objects.get(email=request.session.get('user')) == chat.writer:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():  # 폼이 유효한지
                chat.name = form.cleaned_data['name']
                chat.price = form.cleaned_data['price']
                chat.description = form.cleaned_data['description']
                chat.category = form.cleaned_data['category']
                chat.stock = form.cleaned_data['stock']
                chat.writer = Bcuser.objects.get(email=request.session.get('user'))
                chat.save()
                return redirect('/sellboard/')
            post = get_object_or_404(Product, pk=pk)
            if request.method == "POST":
                    form = RegisterForm(request.POST, request.FILES, instance=post)
                    if form.is_valid():
                        updated_post = form.save(commit=False)
                        updated_post.writer = Bcuser.objects.get(email=request.user.email)  # 로그인된 사용자의 Bcuser 인스턴스를 가져옵니다.
                        updated_post.register_date = timezone.now()
                        updated_post.save()
                        return redirect('product_detail', pk=updated_post.pk)
            else:
                    form = RegisterForm(instance=post)
            return render(request, 'k_sell_update.html', {'form': form})
        else:
            form = RegisterForm(initial={'name':chat.name,'price':chat.price, 'description':chat.description,'category':chat.category, 'stock':chat.stock})
        return render(request, 'k_sell_update.html', {'form': form})
    else:
        raise Http404('권한이 없습니다')


def post_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    post = get_object_or_404(Product, pk=pk)
    if post.writer == Bcuser.objects.get(email=request.session.get('user')):
        post.delete()
        return redirect('sellboard')  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')

    

def k_comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    k_comment = get_object_or_404(Comment, pk=pk)
    if k_comment.author == Bcuser.objects.get(email=request.session.get('user')):
        k_chat_pk = k_comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        k_comment.delete()
        return redirect('product_detail', pk=k_chat_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')

