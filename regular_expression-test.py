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
error_type = syntax
general_error = re.sub(r'in\s.+?#.+\n.*', '', error_type)
general_error2 = re.sub(r'in\s.+?#.+', '', a)
error_details = re.sub(r'(.+\s(/.+):)|(.+\n)', '', error_type)
print(general_error2)
#print(error_details)
