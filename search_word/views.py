from django.shortcuts import render, redirect
# request送信後redirect先を決める reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView, TemplateView
from .models import SearchWord
from .forms import SelectLanguageFormClass, SelectErrorsFormClass


class TopPageView(TemplateView):
    template_name = 'search_word/top.html'


class ListSearchWordView(ListView):
    template_name = 'search_word/search_word_list.html'
    model = SearchWord


def SelectLanguage(request):
    if request.method == 'GET':
        form = SelectLanguageFormClass(request.session.get('form_data'))
    else:
        form = SelectLanguageFormClass(request.POST)
        if form.is_valid():
            request.session['technique'] = request.POST
            return redirect('select_errors')
    context = {
        'form': form
    }
    return render(request, 'search_word/select_language.html', context)


def SelectErrors(request):
    # 送信されたセッションの取得
    technique = request.session.get('technique')
    # 選択言語及びフレームワークによるchoicesの定義
    if technique['technique'] == 'rails':
        error_message = (
            ('syntax', 'SyntaxError'), ('undefind', 'UndefindMethod'))
    elif technique['technique'] == 'django':
        error_message = (
            ('syntax', 'SyntaxError'), ('undefind', 'UndefindMethod'))
    # フォームの呼び出し（使用技術は前回送信したものを初期値に）
    form = SelectErrorsFormClass(technique)
    # エラーメッセージのプルダウンの更新
    form.fields['error_message'].choices = error_message
    # contextの定義
    context = {
        'form': form,
        'technique':technique['technique']
    }
    return render(request, 'search_word/select_errors.html', context)


class CreateSearchWordView(CreateView):
    template_name = 'search_word/search_word_create.html'
    model = SearchWord
    fields = {'technique',
              'error_message', 'error_detail', 'Feature'}
    success_url = reverse_lazy('search_words')


class SuggestWordView(DetailView):
    template_name = 'search_word/suggest_result.html'
    model = SearchWord


def suggest_word(words):
    # 提案ワードを格納する配列をオブジェクトの各要素を変数に定義
    suggest_word = []
    technique = words.technique
    error_message = words.error_message
    error_detail = words.error_detail
    Feature = words.Feature

    # 提案ワードを配列に格納
    suggest_word.append(technique + " " + error_detail)
    suggest_word.append(technique + " " + Feature)
    suggest_word.append(technique + " " + error_message)
    suggest_word.append(technique + " " + error_message + " " + error_detail)
    return suggest_word


def detail_func(request, pk):
    object = SearchWord.objects.get(pk=pk)
    suggest_result = suggest_word(object)
    # viewに渡す物を辞書型配列に変換
    context = {'object': object, 'suggest_result': suggest_result}
    return render(request, 'search_word/suggest_result.html', context)
# Create your views here.

# 他の人が解決したワードとそのサイトURLを貼ってもらう。
# 自分の入力内容と解決した人の入力内容の近似値を求めページも出力できるようにするのがよさそう。
