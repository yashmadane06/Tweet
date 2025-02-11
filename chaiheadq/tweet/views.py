from django.shortcuts import render
from . models import Tweet
from .forms import TweetFrom,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import TweetSearchForm

# Create your views here.
def index(request):
    return render(request,'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets' :tweets})

# def tweet_search(request):
#     form = TweetSearchForm()
#     results = []
#     if request.method == 'GET':
#         form = TweetFrom(request.GET)
#         if form.is_valid():
#             query =form.cleaned_data['query']
#             results=Tweet.objects.filter(text__icontains=query)
#     return render(request,'tweet_search.html',{'form' : form,'results' : results})

def tweet_search(request):
    form =None
    if request.method =='GET':
        form =TweetSearchForm(request.GET)
        if form.is_valid():
            query =form.cleaned_data['query']
            results =Tweet.objects.filter(text__icontains=query)
        else:
            form = TweetSearchForm()

    return render(request,'tweet_search.html',{'form' : form,'results' : results})

# from django.shortcuts import render
# from .models import Tweet
# from .forms import TweetSearchForm

# def tweet_search(request):
#     form = TweetSearchForm()
#     results = []
#     if request.method == 'GET':
#         form = TweetSearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             print(f"Search query: {query}")  # Debugging statement
#             results = Tweet.objects.filter(text__icontains=query)
#             print(f"Results: {results}")  # Debugging statement
#         else:
#             print("Form is not valid")  # Debugging statement
#     return render(request, 'tweet_search.html', {'form': form, 'results': results})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetFrom(request.POST,request.FILES)
        if form.is_valid():
            tweet =form.save(commit=False)
            tweet.user =request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
        form =TweetFrom
    return render(request,'tweet_from.html',{'form' : form})


@login_required
def tweet_edit(request,tweet_id):
    tweet =get_object_or_404(Tweet,pk=tweet_id,user= request.user)
    if request.method == "POST":
        form = TweetFrom(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user =request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form =TweetFrom(instance=tweet)
    return render(request,'tweet_from.html',{'form' : form})

@login_required
def tweet_delete(request,tweet_id):
    tweet =get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet' : tweet})

def register(request):
    if request.method == 'POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form' : form})