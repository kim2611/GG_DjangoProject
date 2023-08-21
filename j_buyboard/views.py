from django.shortcuts import render, redirect, get_object_or_404
from .models import buyProduct, j_Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .forms import *
from django.shortcuts import render
from bcuser.models import Bcuser
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator







# Create your views here.
class buyProductList(ListView):
    model=buyProduct
    template_name='j_buy_board.html'
    context_object_name='buyproduct_list'
    paginate_by=10
    ordering = ['-register_date']

    def get_queryset(self):
        category_filter = self.request.GET.get('category')
        search_query = self.request.GET.get('search_query')

        chats = buyProduct.objects.all().order_by("-register_date")

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
class buyProductCreate(FormView):
    template_name='j_register_buy.html'
    form_class=buyRegisterForm
    success_url='/buyboard/'

    #댓글 추가
    def form_valid(self, form):
        buyproduct = form.save(commit=False)
        bcuser = Bcuser.objects.get(email=self.request.session.get('user'))
        buyproduct.writer = bcuser
        buyproduct.save()

        return super().form_valid(form)
    #######################################################


class buyProductDetail(DetailView):
    queryset = buyProduct.objects.all()
    context_object_name = 'buyproduct'
    template_name = 'j_buy_detail.html'

# 댓글 기능
    def get(self, request, pk):
        try:
            chat = buyProduct.objects.get(pk=pk)
        except buyProduct.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
            
        buyproduct = self.get_object()  # buyproduct 변수 정의
        chat = buyproduct
        chat.save()

        comments = j_Comment.objects.filter(post=chat)
        comment_form = CommentForm()
        context = {
            'buyproduct': buyproduct,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        buyproduct = self.get_object()  # buyproduct 변수 정의
        chat = buyproduct
        

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = chat
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('buyproduct_detail', pk=chat.pk)
        else:
            comment_form = CommentForm()
        context = {
            'buyproduct': buyproduct,
            'comment_form': comment_form,
        }

        return render(request, self.template_name, context)



    

def post_update(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    
    try:
        chat = buyProduct.objects.get(pk=pk)
    except buyProduct.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
        raise Http404('게시글을 찾을 수 없습니다.')
    

    if Bcuser.objects.get(email=request.session.get('user')) == chat.writer:
        if request.method == 'POST':
            form = buyRegisterForm(request.POST)
            if form.is_valid():  # 폼이 유효한지
                chat.name = form.cleaned_data['name']
                chat.price = form.cleaned_data['price']
                chat.description = form.cleaned_data['description']
                chat.category = form.cleaned_data['category']
                chat.writer = Bcuser.objects.get(email=request.session.get('user'))
                chat.save()
                return redirect('/buyboard/')
            post = get_object_or_404(buyProduct, pk=pk)
            if request.method == "POST":
                    form = buyRegisterForm(request.POST, request.FILES, instance=post)
                    if form.is_valid():
                        updated_post = form.save(commit=False)
                        updated_post.writer = Bcuser.objects.get(email=request.user.email)  # 로그인된 사용자의 Bcuser 인스턴스를 가져옵니다.
                        updated_post.register_date = timezone.now()
                        updated_post.save()
                        return redirect('buyproduct_detail', pk=updated_post.pk)
            else:
                    form = buyRegisterForm(instance=post)
            return render(request, 'j_buy_update.html', {'form': form})
        else:
            form = buyRegisterForm(initial={'name':chat.name,'price':chat.price, 'description':chat.description,'category':chat.category})
        return render(request, 'j_buy_update.html', {'form': form})
    else:
        raise Http404('권한이 없습니다')









def post_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    post = get_object_or_404(buyProduct, pk=pk)
    if post.writer == Bcuser.objects.get(email=request.session.get('user')):
        post.delete()
        return redirect('buyboard')  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')

    

def comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    comment = get_object_or_404(j_Comment, pk=pk)
    if comment.author == Bcuser.objects.get(email=request.session.get('user')):
        chat_pk = comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        comment.delete()
        return redirect('buyproduct_detail', pk=chat_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
