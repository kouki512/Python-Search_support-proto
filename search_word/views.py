from django.shortcuts import render, redirect
# request送信後redirect先を決める reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView, TemplateView
from .models import SearchWord
from .forms import SelectLanguageFormClass, SelectErrorsFormClass
import re


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
    # # 送信されたセッションの取得
    # technique = request.session.get('technique')
    # # 選択言語及びフレームワークによるchoicesの定義
    # if technique['technique'] == 'rails':
    #     error_message = (
    #         ('syntax', 'SyntaxError'), ('undefind', 'UndefindMethod'))
    # elif technique['technique'] == 'django':
    #     error_message = (
    #         ('syntax', 'SyntaxError'), ('undefind', 'UndefindMethod'))
    # # フォームの呼び出し（使用技術は前回送信したものを初期値に）
    # form = SelectErrorsFormClass(technique)
    # # エラーメッセージのプルダウンの更新
    # form.fields['error_message'].choices = error_message
    # # contextの定義
    # context = {
    #     'form': form,
    #     'technique':technique['technique']
    # }
    # 送信されたセッションの取得
    technique = request.session.get('technique')
    print(technique)
    # 選択言語及びフレームワークによるchoicesの定義

    # フォームの呼び出し（使用技術は前回送信したものを初期値に）
    form = SelectErrorsFormClass()
    # エラーメッセージのプルダウンの更新
    #form.fields['error_message'].choices = error_message
    # contextの定義
    if request.method == 'POST':
        form = SelectErrorsFormClass(request.POST)
        #form.fields['error_message'].choices = error_message
        # formに入力がある場合オブジェクトを生成
        if form.is_valid():
            SearchWord.objects.create(**form.cleaned_data)
            return redirect('search_words')
        else:
            print(form)
    context = {
        'form': form,
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


def selection_error(error_message):
    # エラーの大枠を抽出
    general_error = re.sub(r'in\s.+?#.+\n.*', '', error_message.error_detail)
    # エラーの詳細を抽出
    error_detail = re.sub(r'(.+\s(/.+):)|(.+\n)', '',
                          error_message.error_detail)

    # 抽出したエラーメッセージを辞書型配列に格納
    collection_result = {"general_error": general_error,
                         "error_detail": error_detail}
    return collection_result


def suggest_word(words, colection_error):
    # 提案ワードを格納する配列をオブジェクトの各要素を変数に定義
    suggest_word = []
    technique = words.technique
    general_error = colection_error['general_error']
    error_detail = colection_error['error_detail']
    Feature = words.Feature

    # 提案ワードを配列に格納
    suggest_word.append(technique + " " + error_detail)
    suggest_word.append(technique + " " + Feature)
    suggest_word.append(technique + " " + Feature + " " + general_error)
    suggest_word.append(technique + " " + general_error)
    suggest_word.append(technique + " " + general_error + " " + error_detail)
    return suggest_word


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
    context = {'object': object, 'suggest_result': suggest_result}
    return render(request, 'search_word/suggest_result.html', context)
# Create your views here.

# 他の人が解決したワードとそのサイトURLを貼ってもらう。
# 自分の入力内容と解決した人の入力内容の近似値を求めページも出力できるようにするのがよさそう。
