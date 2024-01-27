from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def home(request):
    search = request.GET.get('searchMovie')
    if search:
        movies = Movie.objects.filter(title__icontains=search)
    else:
        movies = Movie.objects.all()
    # return HttpResponse('<h1>Hello wecome Home!!</h1>')
    return render(request, 'home.html', {'name': search, 'movies': movies})

def about(request):
    return HttpResponse('<h2>There is nothing About this!1</h1>')

@require_http_methods(['GET','POST'])
def signup(request):
    email = request.GET.get('email')
    print(email)
    return render(request, 'signup.html', {'email': email})

def details(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'details.html',{'movie': movie, 'reviews': reviews})

@login_required
def createReview(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == "GET":
        return render(request, 'createreview.html',{'form': ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('movie-details', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html',{'form': ReviewForm(),'error': 'Bad Data! please check again!'})
      
@login_required
def updateReview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == "GET":
        form = ReviewForm(instance=review)
        return render(request,'updatereview.html',{'review': review, 'form': form})
    else:
        try:
            form = ReviewForm(request.POST,instance=review)
            form.save()
            return redirect('movie-details', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html', {'review': review, 'form': form, 'error': 'Bad data in form'})
        
@login_required
def deleteReview(request,review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('movie-details', review.movie.id)