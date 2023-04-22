from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SalesInfo
from .forms import ProductForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count


def index(request):
    """
    sales 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')      # 검색어
    so = request.GET.get('so', 'recent')    # 정렬 기준

    if so == 'recommend':
        product_list = Product.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', 'pname')
    elif so == 'popular':
        product_list = Product.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', 'pname')
    else:  # recent
        product_list = Product.objects.order_by('pname')

    # 조회
    if kw:
        product_list = product_list.filter(
            Q(type__icontains=kw) |                      # 제목 검색
            Q(pname__icontains=kw)                       # 내용 검색
        ).distinct()

    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page)
    context = {'product_list' : page_obj}
    return render(request, 'sales/product_list.html', context)

def detail(request,product_id):
    """
    sales 내용 출력
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {'product' : product}
    return render(request, 'sales/product_detail.html', context)

@login_required(login_url='common:login')
def product_create(request):
    """
    sales 제품 등록
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('sales:index')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'sales/product_form.html', context)

@login_required(login_url='common:login')
def product_modify(request, product_id):
    """
    제품 수정
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:detail', product_id=product.id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.modify_date = timezone.now()  # 수정일시 저장
            product.save()
            return redirect('sales:detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'sales/product_form.html', context)

@login_required(login_url='common:login')
def product_delete(request, product_id):
    """
    제품 삭제
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:detail', product_id=product.id)
    product.delete()
    return redirect('sales:index')

def info_index(request):
    """
    sales 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')      # 검색어
    so = request.GET.get('so', 'recent')    # 정렬 기준

    if so == 'recommend':
        salesinfo_list = SalesInfo.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-p_date')
    elif so == 'popular':
        salesinfo_list = SalesInfo.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-p_date')
    else:  # recent
        salesinfo_list = SalesInfo.objects.order_by('-p_date')

    # 조회
    if kw:
        salesinfo_list = salesinfo_list.filter(
            Q(type__icontains=kw) |                      # 제목 검색
            Q(pname__icontains=kw)                       # 내용 검색
        ).distinct()

    paginator = Paginator(salesinfo_list, 10)
    page_obj = paginator.get_page(page)
    context = {'salesinfo_list' : page_obj}
    return render(request, 'sales/salesinfo_list.html', context)



