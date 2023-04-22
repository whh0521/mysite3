from django import forms
from sales.models import Product
from sales.models import SalesInfo

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['type', 'pname', 'releasedate', 'runningtime', 'pprice','imgfile']
        labels = {
            'type': '장르',
            'pname': '영화 제목 ',
            'releasedate': '개봉일 ',
            'runningtime': '러닝타임 ',
            'pprice': '구매가격 ',
            'imgfile': '포스터',
        }

class SalesInfoForm(forms.ModelForm):
    class Meta:
        model = SalesInfo
        fields = ['type', 'pname', 'pprice', 'p_date']
        labels = {
            'type': '장르',
            'pname': '영화 제목 ',
            'pprice': '구매가격 ',
            'p_date': '판매일'
        }