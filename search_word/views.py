from django.shortcuts import render, redirect
# request送信後redirect先を決める reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView, TemplateView
from .models import SearchWord
from .forms import SelectLanguageFormClass, SelectErrorsFormClass
import re
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)

class TopPageView(TemplateView):
    template_name = 'search_word/top.html'


class ListSearchWordView(ListView):
    template_name = 'search_word/search_word_list.html'
    model = SearchWord


def SelectLanguage(request):
    # if request.method == 'GET':
    #     form = SelectLanguageFormClass(request.session.get('form_data'))
    # else:
    #     form = SelectLanguageFormClass(request.POST)
    #     if form.is_valid():
    #         request.session['technique'] = request.POST
    #         return redirect('select_errors')
    if request.method == 'GET':
        form = SelectLanguageFormClass(request.session.get('form_data'))
    else:
        form = SelectLanguageFormClass(request.POST)
        if form.is_valid():
            request.session['technique'] = 'rails'
            return redirect('select_errors')
    context = {
        'form': form
    }
    return render(request, 'search_word/select_language.html', context)


def SelectErrors(request):

    # 送信されたセッションの取得
    technique = request.session.get('technique')
    # 選択言語及びフレームワークによるchoicesの定義

    # フォームの呼び出し（使用技術は前回送信したものを初期値に）
    form = SelectErrorsFormClass()

    # contextの定義
    if request.method == 'POST':
        form = SelectErrorsFormClass(request.POST)
        #form.fields['error_message'].choices = error_message
        # formに入力がある場合オブジェクトを生成
        if form.is_valid():
            search_word = SearchWord.objects.create(**form.cleaned_data)
            # print(search_word.pk)
            return redirect('search_word', pk=search_word.pk)
        else:
            print(form)
    context = {
        'form': form,
    }
    return render(request, 'search_word/select_errors.html', context)


class SuggestWordView(DetailView):
    template_name = 'search_word/suggest_result.html'
    model = SearchWord

# 入力されたエラーメッセージを分割し検索に必要なワードを抽出する関数


def selection_error(error_message):
    # エラーの大枠を抽出
    general_error = re.sub(
        r'(in\s.+?#.+[\s\S]*)|(Showing.+raised:)', '', error_message.error_message)
    # エラーの詳細を抽出
    error_detail = re.sub(r'(.+\s(/.+):)|(for\s#.+)|(.+in\s.+?#.+)|(Did you mean[\s\S]*)|(Routing Error)', '',
                          error_message.error_message)

    # 抽出したエラーメッセージを辞書型配列に格納
    collection_result = {"general_error": general_error,
                         "error_detail": error_detail}
    return collection_result


def suggest_word(words, colection_error):
    # 提案ワードを格納する配列をオブジェクトの各要素を変数に定義
    suggest_words = []
    general_error_word = []
    detail_error_word = []
    make_function_word = []

    technique = words.technique
    general_error = colection_error['general_error']
    error_detail = colection_error['error_detail']
    Feature = words.Feature

    # 提案ワード（エラーの大枠）を配列に格納
    general_error_word.append(technique + " " + general_error + " " + "意味")
    # 提案ワードを配列に格納(エラー解決ワード)
    detail_error_word.append(technique + " " + error_detail)
    detail_error_word.append(technique + " " + Feature + " " + error_detail)
    # 提案ワード（実装内容）を配列に格納
    make_function_word.append(technique + " " + Feature)
    make_function_word.append(technique + " " + Feature + " " + "実装")
    suggest_words = [general_error_word, detail_error_word, make_function_word]
    return suggest_words


def detail_func(request, pk):
    object = SearchWord.objects.get(pk=pk)
    # エラーメッセージの抽出
    collection_result = {}
    collection_result = selection_error(object)
    # 抽出ココまで

    # 検索ワードの作成
    suggest_result = suggest_word(object, collection_result)
    # 検索ワードの作成ココまで

    # viewに渡す物を辞書型配列に変換
    context = {'object': object, 'collection_result': collection_result, 'general_error_word':
               suggest_result[0], 'detail_error_word': suggest_result[1], 'make_function_word': suggest_result[2]}
    return render(request, 'search_word/suggest_result.html', context)


def DeleteSearchWord(request, pk):
    if request.method == 'POST':
        search_word = SearchWord.objects.get(pk=pk)
        search_word.delete()
    return redirect('search_words')
# Create your views here.

# 他の人が解決したワードとそのサイトURLを貼ってもらう。
# 自分の入力内容と解決した人の入力内容の近似値を求めページも出力できるようにするのがよさそう。

# エラーのサンプル

# SyntaxError in Devise::RegistrationsController#new /app_name/app/views/devise/registrations/new.html.erb:10: syntax error, unexpected '<' <%= render "devise/shared/erro... ^ /app_name/app/views/devise/registrations/new.html.erb:50: syntax error, unexpected ensure, expecting ')' ensure ^~~~~~ /app_name/app/views/devise/registrations/new.html.erb:52: syntax error, unexpected end, expecting ')' end ^~~
