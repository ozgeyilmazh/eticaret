from django import forms

from products.models import Comment


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length = 100)


# ÜRÜN YORUM FORM
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'content',
        ]