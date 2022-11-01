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
    # general_error = re.sub(
    #     r'(in\s.+?#.+[\s\S]*)', '', error_message.error_message)
    
    # xxxError in yyy#zzz の抽出
    selection_general_error = re.search(r'.*\s*(?=\n|\r)', error_message.error_message)
    if selection_general_error:
        general_error = selection_general_error.group()
    else:
        general_error = "文章を抽出できませんでした。"

    # xxxErrorの抽出
    selection_summary_error = re.search(r'.*\s(?=\bin\b\s)|.*\s*',general_error)
    if selection_summary_error:
        summary_error = selection_summary_error.group()
    else:
        summary_error = "文章を抽出できませんでした。"

    # yyy#zzzの抽出
    selection_general_path = re.search(r'(?<=\bin\b\s).*', general_error)
    if selection_general_path:
        general_path = selection_general_path.group()
    else:
        general_path = "今回はエラーの発生場所が示されていません。"
    
    # エラーの詳細を抽出
    # エラーの概要を取り除いたメッセージ全て
    reject_summary = re.sub(general_error,"",error_message.error_message)
    # 具体的なファイル名
    selection_file_path = re.findall(r'Showing.*raised:',error_message.error_message)
    if selection_file_path:
        file_path = selection_file_path[0]
    else:
        file_path = None 
    # 解決に繋がるエラーメッセージ
    error_detail = re.sub(r'(.+\s(/.+):)|(for\s#.+)|(.+in\s.+?#.+)|(Did you mean[\s\S]*)|(Routing Error)|(LoadError)', '',error_message.error_message)

    # 抽出したエラーメッセージを辞書型配列に格納
    collection_result = {"general_error": general_error,
                        "summary_error": summary_error,
                        "general_path" : general_path,
                        "error_detail": error_detail,
                        "file_path":file_path,
                        "reject_summary":reject_summary}
    return collection_result


# 検索ワード及び参考記事リンクの作成をする関数
def suggest_word(words, colection_error):
    # 提案ワードを格納する配列をオブジェクトの各要素を変数に定義
    suggest_words = []
    summary_error_word = []
    summary_error_link = []
    detail_error_word = []

    technique = words.technique
    summary_error = colection_error['summary_error']
    error_detail = colection_error['error_detail']
    Feature = words.Feature

    # 提案ワード（エラーの大枠）を配列に格納
    summary_error_word.append(technique + " " + summary_error + " " + "意味")
    # (エラータイトル)のリンクを格納
    print(type(colection_error['summary_error']))
    if 'SyntaxError' in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/SyntaxError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    elif "NoMethodError" in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/NoMethodError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    elif "NameError" in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/NameError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    elif "LoadError" in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/LoadError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    elif "TypeError" in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/TypeError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    elif "ArgumentError" in summary_error:
        summary_error_link.append("https://docs.ruby-lang.org/ja/latest/class/ArgumentError.html")
        summary_error_link.append("https://zenn.dev/nagan/articles/ca4b155c630f25")
    else:
        summary_error_link.append("参考になりそうなページを検索してみましょう。")
    print(summary_error_link)
    # 提案ワードを配列に格納(エラー解決ワード)
    detail_error_word.append(technique + " " + error_detail)
    detail_error_word.append(technique + " " + Feature + " " + error_detail)
    # 提案ワード（実装内容）を配列に格納
    suggest_words = [summary_error_word, detail_error_word, summary_error_link]
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

    # templateに渡す物を辞書型配列に変換
    # 抽出されたワードと検索ワード、参考記事のリンク
    context = {'object': object,
                'collection_result': collection_result, 
                'summary_error_word':suggest_result[0],
                'detail_error_word': suggest_result[1],'summary_error_link':suggest_result[2]}
    return render(request, 'search_word/suggest_result.html', context)


def DeleteSearchWord(request, pk):
    if request.method == 'POST':
        search_word = SearchWord.objects.get(pk=pk)
        search_word.delete()
    return redirect('search_words')


# 他の人が解決したワードとそのサイトURLを貼ってもらう。
# 自分の入力内容と解決した人の入力内容の近似値を求めページも出力できるようにするのがよさそう。


