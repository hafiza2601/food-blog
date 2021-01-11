from django.shortcuts import render,redirect,HttpResponse
from django.utils import timezone
from .models import Post 
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Contact,BlogComment,Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def home(request):
    return render(request, 'blog/home/home.html')

'''
Blog Api
'''


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context={'allpost':posts}
    return render(request, 'blog/home/blog.html',context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = BlogComment.objects.filter(post=post)
    context = {'post':post, 'comments':comments, 'user':request.user}
    return render(request, 'blog/post_detail.html', context)

'''
comment API
'''
def postComment(request):
    if request.method== "POST":
        comment = request.POST.get("comment")
        user= request.user
        post_pk = request.POST.get("post_pk")
        post = Post.objects.get(pk = post_pk)
        parent_sno = request.POST.get("post_pk")
    

        if parent_sno == "":
            comment = BlogComment(comment= comment, user=user, post=post)
            messages.success(request, "Your comment has been posted successfully")
        else :
            parent = BlogComment.objects.get(pk = parent_sno)
            comment = BlogComment(comment= comment, user=user, post=post, parent=parent) 
            messages.success(request, "Your Reply has been posted successfully")
        comment.save()
    return redirect(f"/blog/{post.slug}")
            

'''
post add and edit
'''    
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})
    
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})

'''
search
'''

def search(request):
    query = request.GET['query']
    posts_title = Post.objects.filter(title__icontains =query)
    posts_text = Post.objects.filter(text__icontains =query)
    result= posts_title | posts_text
    

    context = {'allposts':result}
    #print(context)
    #return render(request, 'blog/home/search.html',{'allposts':posts})
    return render(request, 'blog/home/search.html',context)

'''About Us'''
def about_us(request):
    
    return render(request, 'blog/home/aboutus.html')

'''Contact Us'''

def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else :
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, "Your message has been succesfully sent")
        
    

    
    return render(request, 'blog/home/contact.html')

'''
signup
'''
def handlesignup(request):
    if request.method == 'POST':
        username= request.POST['username']
        firstname= request.POST['fname']
        lastname= request.POST['lname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

        #check for error input

        #username should be 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        #username should be alpha numeric

        if not username.isalnum():
            messages.error(request, "useranme should only contain alphabets and numbers")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')



        #create user
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your account has been succesfully created")

        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername , password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Succesfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials ,Please try again")
            redirect('home')
            


    return HttpResponse('404 - Not Found')

def handlelogout(request):
    logout(request)
    messages.success(request, "Succesfully Logged Out")

    return redirect('home')




