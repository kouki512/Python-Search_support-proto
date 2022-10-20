import re
syntax = '''SyntaxError in Devise::RegistrationsController#new
/app_name/app/views/devise/registrations/new.html.erb:10: syntax error, unexpected '<' <%= render "devise/shared/erro... ^ /app_name/app/views/devise/registrations/new.html.erb:50: syntax error, unexpected ensure, expecting ')' ensure ^~~~~~ /app_name/app/views/devise/registrations/new.html.erb:52: syntax error, unexpected end, expecting ')' end ^~~'''

#syntax = '''/app_name/app/views/devise/registrations/new.html.erb:10: syntax error, unexpected '''

no_method = '''NoMethodError in BooksController#create
undefined method `save' for nil:NilClass'''

type_error = '''TypeError in BooksController#create 
no implicit conversion of Symbol into Integer'''
a = '''NoMethodError in Books#index
Showing /app_name/app/views/books/index.html.erb where line #43 raised:

undefined method `titlea' for #<Book:0x00007f63b5818ee8>
Did you mean?  title
               title?
               title='''

route_error = '''NameError in BooksController#create
undefined local variable or method `ok_params' for #<BooksController:0x00007f6d40078118> Did you mean? book_params params @_params to_param'''

error_type = syntax
general_error = re.sub(r'in\s.+?#.+\n.*', '', error_type)
general_error2 = re.sub(r'in\s.+?#.+', '', a)
error_details = re.sub(r'(.+\s(/.+):)|(.+\n)', '', error_type)


# general_error3の解説
# (.*\s)+(.+#.+)=>任意の文字列＋#~（コントローラ名＃アクション名）
# .*\s*(?=\n|\r)=>任意の文字列（＋半角）＋改行文字
general_error3 = re.search(r'(?<=\bin\b\s)(.*\s)+(.+#.+)|.*\s*(?=\n|\r)', route_error )
# summary_errorの解説
# .*\s(?=\bin\b\s)|.*\s* => "in"という単語より前の任意の文字列 or 任意の文字列（パスが書かれていない場合）
summary_error = re.search(r'.*\s(?=\bin\b\s)|.*\s*',general_error3.group())
# general_pathの解説
# .(?<=\bin\b\s).* => "in"という単語より後の任意の文字列（パスがない場合はnoneが返る）
general_path = re.search(r'(?<=\bin\b\s).*', general_error3.group())
print(general_error3.group())


print(summary_error.group())

if general_path:
  print(general_path.group())
else:
  print("パスは記載されていません。")

