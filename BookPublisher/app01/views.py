from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator


# Create your views here.

###################删除出版社，书籍和作者整合delete###################
def delete(request,table,pk):

    # 根据前端传过来的id查找数据库中的数据，返回的是一个对象列表
    class_table = getattr(models,table.capitalize())
    print()

    del_id = class_table.objects.filter(pk=pk)
    if not del_id:
        return HttpResponse('删除的数据不存在')

    del_id.delete()  # 删除数据
    return redirect(reverse(table))  # 重定向返回到显示页面

#########################################出版社管理系统################################
def publisher_system(request):
    # 获取所有的对象
    all_publisher = models.Publisher.objects.all().order_by('pid')
    # 向浏览器前端返回渲染的网页和数据库的数据对象
    return render(request, 'publisher_system.html', {'all_publisher': all_publisher})

# 增加
def add_publisher(request):
    error = ''
    # 如果是POST请求则执行增加操作
    if request.method == "POST":

        # 获取前端传过来的数据
        get_publisher = request.POST.get('add_publisher')
        # 从前端传过来的数据进行check，如果存在或者为空，则返回相应信息给客户
        if models.Publisher.objects.filter(name=get_publisher):
            error = '出版社已存在'
        if not get_publisher:
            error = '出版社不能为空'

        # 如果正常，则增加到数据库中
        if not error:
            models.Publisher.objects.create(name=get_publisher)
            return redirect('/publisher_system/')  # 增加数据成功后重定向显示

    return render(request, 'add_publisher.html', {'error': error})  # 若增加数据失败则传入错误信息并返回当前页面


# 删除
def del_publisher(request,pk):
    # 获取前端传过来的id数据
    # get_id = request.GET.get('id')  # url上携带的参数  不是GET请求提交参数

    # 根据前端传过来的id查找数据库中的数据，返回的是一个对象列表
    del_id = models.Publisher.objects.filter(pid=pk)
    if not del_id:
        return HttpResponse('删除的数据不存在')
    del_id.delete()  # 删除数据
    return redirect('/publisher_system/')  # 重定向返回到显示页面


# 编辑修正数据edit_publisher
def edit_publisher(request,pk):
    # get请求时判断数据是否存在
    error = ''
    # get_id = request.GET.get('id')
    edit_id = models.Publisher.objects.filter(pid=pk)
    if not edit_id:
        return HttpResponse('编辑的数据不存在')
    edit = edit_id[0]
    print(request.method)

    # 编辑之后的请求的post请求
    if request.method == 'POST':
        # 获取前端传过来的name数据
        get_name = request.POST.get('edit_publisher')

        # check编辑后的名字是否符合条件，符合则将编辑后的渲染到页面
        if models.Publisher.objects.filter(name=get_name):
            error = '修正的出版社名字已存在'
        if get_name == edit.name:
            error = '出版社名字已存在'
        if not get_name:
            error = '出版社名字不能为空'
        if not error:
            edit.name = get_name
            edit.save()  # save之后才真正的更新到了数据库
            return redirect('/publisher_system/')  # 重定向返回到显示页面

    # get请求时候，会渲染此页面，并将对象传到前端页面
    return render(request, 'edit_publisher.html', {'edit': edit, 'error': error})


#######################################图书管理系统###################################

# 给FBV加装饰器
import time

def timer(func):
    def inner(*args,**kwargs):
        start = time.time()
        ret = func(*args,**kwargs)
        print('time-->>>',time.time()-start)
        return ret
    return inner

@timer
def book_system(request):
    # 从数据库获取所有的图书，并从出版社表中取出出版社名字
    book_all = models.Book.objects.all()
    return render(request, 'book_system.html', {'book_all': book_all})


#增加图书(FBV)
# def add_book(request):
#     pub_all = models.Publisher.objects.all()
#     error = ''
#     # 如果是POST请求则执行增加操作
#     if request.method == "POST":
#         # 获取前端传过来的数据
#         get_book = request.POST.get('add_book')
#         pub_id = request.POST.get('pub_id')
#         # 从前端传过来的数据进行check，如果存在或者为空，则返回相应信息给客户
#         if models.Book.objects.filter(title=get_book):
#             error = '书名已存在'
#         if not get_book:
#             error = '书名不能为空'
#
#         # 如果正常，则增加到数据库中
#         if not error:
#             # 增加数据到数据库
#             # 注意这里，因为Book的pub是一个Publisher对象，所以要么传一个Publisher对象，要么直接传pub_id
#             # 这里还可以这样写：pub_id=pub_id-->> pub = models.Publisher.objects.get(pk=pub_id) 获取的是唯一符合条件的对象
#             models.Book.objects.create(title=get_book, pub_id=pub_id)
#
#             return redirect('/book_system/')  # 增加数据成功后重定向显示
#
#     return render(request, 'add_book.html', {'error': error, 'pub_all': pub_all})  # 若增加数据失败则传入错误信息并返回当前页面




#增加图书(CBV写法)
# 写法二可以写多个：@method_decorator(timer,name='get')
# @method_decorator(timer,name='post')
# 写法三name指定为dispatch：@method_decorator(timer,name='dispatch')
@method_decorator(timer,name='dispatch')
class AddBook(View):

    #写法四调用父类的dispatch：@method_decorator(timer)
    def dispatch(self, request, *args, **kwargs):
        ret = super().dispatch(request, *args, **kwargs)
        return ret

    # 写法一：@method_decorator(timer)
    def get(self, request, *args, **kwargs):

        pub_all = models.Publisher.objects.all()
        return render(request, 'add_book.html', {'pub_all': pub_all})  # 若增加数据失败则传入错误信息并返回当前页面

    def post(self, request, *args, **kwargs):
        pub_all = models.Publisher.objects.all()
        error = ''
        # 获取前端传过来的数据
        get_book = request.POST.get('add_book')
        pub_id = request.POST.get('pub_id')
        # 从前端传过来的数据进行check，如果存在或者为空，则返回相应信息给客户
        if models.Book.objects.filter(title=get_book):
            error = '书名已存在'
        if not get_book:
            error = '书名不能为空'

        # 如果正常，则增加到数据库中
        if not error:
            # 增加数据到数据库
            # 注意这里，因为Book的pub是一个Publisher对象，所以要么传一个Publisher对象，要么直接传pub_id
            # 这里还可以这样写：pub_id=pub_id-->> pub = models.Publisher.objects.get(pk=pub_id) 获取的是唯一符合条件的对象
            models.Book.objects.create(title=get_book, pub_id=pub_id)

            return redirect('/book_system/')  # 增加数据成功后重定向显示

        return render(request, 'add_book.html', {'pub_all': pub_all})  # 若增加数据失败则传入错误信息并返回当前页面


# 删除图书
def del_book(request,pk):
    # 获取前端传过来的id数据
    # get_id = request.GET.get('id')  # url上携带的参数  不是GET请求提交参数

    # 根据前端传过来的id查找数据库中的数据，返回的是一个对象列表
    del_id = models.Book.objects.filter(pk=pk)
    if not del_id:
        return HttpResponse('删除的数据不存在')
    del_id.delete()  # 删除数据
    return redirect('/book_system/')  # 重定向返回到显示页面


# 修改书名和出版社的名字
def edit_book(request,pk):
    # get请求时判断数据是否存在
    error = ''
    # get_id = request.GET.get('id')
    edit_id = models.Book.objects.filter(pk=pk)
    if not edit_id:
        return HttpResponse('编辑的数据不存在')
    edit = edit_id[0]

    # 编辑之后的请求的post请求
    if request.method == 'POST':
        # 获取前端传过来的name数据
        get_book_name = request.POST.get('edit_book')
        get_publisher_id = request.POST.get('edit_publisher')

        # check编辑后的名字是否符合条件，符合则将编辑后的渲染到页面
        if models.Book.objects.filter(title=get_book_name):
            error = '修正的书名已存在'
        if get_book_name == edit.title:
            error = '书名已存在'
        if not get_book_name:
            error = '书名不能为空'
        if not error:
            edit.title = get_book_name
            edit.pub = models.Publisher.objects.get(pk=get_publisher_id)
            edit.save()  # save之后才真正的更新到了数据库
            return redirect('/book_system/')  # 重定向返回到显示页面
    pub_all = models.Publisher.objects.all()
    # get请求时候，会渲染此页面，并将对象传到前端页面
    return render(request, 'edit_book.html', {'edit': edit, 'pub_all': pub_all, 'error': error})


#########################################作者管理系统###############################################
def author_system(request):
    all_author = models.Author.objects.all()

    # #查询所有的作者
    # # all_author--->>> <QuerySet [<Author: Author object>, <Author: Author object>, <Author: Author object>, <Author: Author object>]>
    # print('all_author--->>>',all_author)
    #
    # #author是单独的作者对象
    # for author in all_author:
    #     print('author.name--->>>', author.name) # 张燕秋 、张小红、刘宇、韩红 (也就是将所有的作者姓名输出)
    #
    #     # type类型输出的是：<class 'django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
    #     # ManyRelatedManager就是关系管理对象、
    #     print('author.books--->>>', author.books,type(author.books)) # 输出：app01.Book.None（注意books这里是）
    #
    #     #关系管理对象有自己的方法.all() 拿到的就是Book书籍对象
    #     #作者对象-->关系对象--->书籍对象-->再去拿书籍对象中相应的属性值
    #     print('author.books.all--->>>', author.books.all()) # QuerySet [<Book: Book object>]>
    #
    #     boo = author.books.all() # 注意取得的是所有的Book对象
    #     for bo in boo:
    #         print('bo.title--->>>',bo.title) # 所有书名都输出
    if not all_author:
        return HttpResponse('要查询的数据不存在')
    return render(request, 'author_system.html', {'all_author': all_author})


def add_author(request):
    error = ''
    if request.method == 'POST':
        # 获取前端传过来的数据
        add_author = request.POST.get('add_author')

        # getlist获取的是所有的pk，getlist返回的是列表值
        # request.POST.get('author_book')--> get获取的是当前的pk值,如果有多个取得是最后一个
        book_id = request.POST.getlist('author_book')

        if models.Author.objects.filter(name=add_author):
            error = '用户名已存在，请重新输入'

        if not add_author:
            error = '用户名不能为空，请重新输入'

        if not error:
            # 存入数据库
            author_name = models.Author.objects.create(name=add_author)  # 返回的是一个作者对象
            # #create 方法返回的也是一个对象
            # print('author_name-->>',author_name) # author_name-->> Author object
            # author_name.books 是关系管理对象 ，就是负责管理多对多的关系的，将上面获取到的书籍列表直接set就可以了
            author_name.books.set(book_id)
            return redirect('/author_system/')

    all_book = models.Book.objects.all()
    return render(request, 'add_author.html', {'all_book': all_book, 'error': error})


def del_author(request,pk):
    # 通过参数传递，所以不需要获取了
    # pk = request.GET.get('pk')
    aut_obj = models.Author.objects.filter(pk=pk)
    if not aut_obj:
        return HttpResponse('要删除的数据不存在')
    aut_obj.delete()
    return redirect('/author_system/')


def edit_author(request,pk):
    # pk = request.GET.get('pk')
    edit_author = models.Author.objects.filter(pk=pk)  # 获取对象列表
    edit_author = edit_author[0]
    error = ''
    if request.method == 'POST':
        get_author = request.POST.get('edit_author')
        get_id = request.POST.getlist('authod_id')  # 用getlist获取列表值（获取多个值）

        if not get_author:
            error = '修改的作者名称不能为空'

        if models.Author.objects.filter(name=get_author):
            error = '作者名称已存在'

        if not error:
            edit_author.name = get_author
            edit_author.save()  # 先将名字提交到数据库
            edit_author.books.set(get_id)  # 更新books字段，因为books是多对多关系，所以要取到关系管理对象再通过set插入数据

            return redirect('/author_system/')
    book_all = models.Book.objects.all()
    return render(request, 'edit_author.html', {'edit_author': edit_author, 'book_all': book_all, 'error': error})

###########################test 动态路由#########################
def index(request):
    ind1 = reverse('app01:blogs',args=('666',))
    print(ind1)

    ind2 = reverse('app01:blog2',args=('kkkk',8956,))
    print(ind2)
    # return HttpResponse('你好，我是动态url，index')
    return render(request, 'index3.html')

def indexs(request):
    return HttpResponse('你好，我是动态url，indexs')

def years(request,years):
    return HttpResponse('你好，我是动态url，years',years)

def yearsmonth(request,years,month):
    print(years)
    print(month)
    return HttpResponse('你好，我是动态url，yearsmonth')

def year(request,yy,mm):
    print(yy)
    print(mm)
    return HttpResponse('你好，我是动态url，year')

def index2(request,num = 1):
    print('num--->>>',num)
    return HttpResponse('你好，我是动态url，index2')

# 路由分发
def blog(request,year):
    print(year)
    return HttpResponse('你好，我是动态url，blog')

def blogs(request,year):
    print(year)
    return HttpResponse('你好，我是动态url，blogs')

def blog2(request,years,months):

    return HttpResponse('你好，我是动态url，blog2')

# 反向解析
def blog(request):
    return HttpResponse('你好，我是动态url，反向解析blog')

def index3(request):
    return render(request, 'index3.html')

def index10(request):
    return HttpResponse('你好，我是动态url，index10')

def home(request):
    return HttpResponse('app01，home')

