from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Profile
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, "network/index.html", {
        "posts": posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request, username):
    
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        users_profile = Profile.objects.get(user=request.user)
    except:
        return render(request, "network/profile.html", {"error": True})
    
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
            
    else:
        posts = paginator.page(1)
        
    for i in users_profile.follower.all():
        print(i)
        
    context = {
        "users_profile": users_profile,
        "user": user,
        "profile": profile,
        "posts": posts,
    }
    return render(request, "network/profile.html", context)


@login_required
def following(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
            
    else:
        posts = paginator.page(1)
    return render(request, "network/following.html", {
        "posts": posts,
    })


@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        is_liked = request.POST.get("is_liked")
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == "no":
                post.like.add(request.user)
                is_liked = "yes"
            elif is_liked == "yes":
                post.like.remove(request.user)
                is_liked = "no"
            post.save()

            return JsonResponse({
                "like_count": post.like.count(),
                "is_liked": is_liked,
                "status": 201})
        except:
            return JsonResponse({
                "error": "Post not found",
                "status": 404})
    return JsonResponse({}, status=400)


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get("user")
        action = request.POST.get("action")

        if action == "Follow":
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.add(user)
                profile.save()

                # add current user to  user's follower list
                profile = Profile.objects.get(user=user)
                profile.follower.add(request.user)
                profile.save()
                return JsonResponse({
                    "status": 301,
                    "action": "Unfollow",
                    "follower_count": profile.follower.count()}, status=201)
            except:
                return JsonResponse({}, status=404)
        else:
            try:

                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.remove(user)
                profile.save()


                profile = Profile.objects.get(user=user)
                profile.follower.remove(request.user)
                profile.save()
                return JsonResponse({'status': 201, 'action': "Follow", "follower_count": profile.follower.count()}, status=201)
            except:
                return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)


@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.post = new_post.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)


@login_required
@csrf_exempt
def addpost(request):
    if request.method == "POST":
        post = request.POST.get("post")
        if len(post) != 0:
            obj = Post()
            obj.post = post
            obj.user = request.user
            obj.save()
            context = {
                "status": 201,
                "post_id": obj.id,
                "username": request.user.username,
                "timestamp": obj.timestamp.strftime("%B %d, %Y, %I:%M %p"),
            }
            return JsonResponse(context, status=201)
    return JsonResponse({}, status=400)




# from django.contrib.auth import authenticate, login, logout
# from django.db import IntegrityError
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
# from .models import *
# from django import forms
# from django.contrib.auth.decorators import login_required
# import datetime
#
#
# def index(request):
#     # return render(request, "auctions/index.html")
#     all_listings = Auction.objects.all()
#     return render(request, "auctions/index.html", {"all_listings":all_listings})
#
#
# def login_view(request):
#     if request.method == "POST":
#
#         # Attempt to sign user in
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#
#         # Check if authentication successful
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "auctions/login.html", {
#                 "message": "Invalid username and/or password."
#             })
#     else:
#         return render(request, "auctions/login.html")
#
#
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))
#
#
# def register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#
#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(request, "auctions/register.html", {
#                 "message": "Passwords must match."
#             })
#
#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.save()
#         except IntegrityError:
#             return render(request, "auctions/register.html", {
#                 "message": "Username already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "auctions/register.html")
#
#
# CAT_CHOICES =(
#     ("1", "Electronics"),
#     ("2", "Fashion"),
#     ("3", "Books"),
#     ("4", "Furniture"),
#     ("5", "Sports"),
#     ("6", "Instruments"),
# )
#
#
# class CreateListingForm(forms.Form):
#     title = forms.CharField()
#     description = forms.CharField()
#     img_url = forms.CharField()
#     category = forms.MultipleChoiceField(choices=CAT_CHOICES)
#     price = forms.FloatField()
#     date = forms.DateTimeField()
#
#
# @login_required()
# def create_listing(request):
#     if request.method == "POST":
#         form = CreateListingForm(request.POST)
#         if form.is_valid():
#             auction = Auction()
#             auction.title = request.POST.get('title')
#             auction.description = request.POST.get('description')
#             auction.img_url = request.POST.get('img_url')
#             auction.category = request.POST.get('category')
#             auction.price = request.POST.get('price')
#             auction.date = request.POST.get('date')
#             auction.save()
#         else:
#             return render(request, "auctions/create.html", {
#                 "form": form
#             })
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return render(request, "auctions/create.html", {
#             "form": CreateListingForm()
#         })
#
#
# @login_required()
# def categories(request):
#     return render(request, "auctions/categories.html")
#
#
# @login_required()
# def category(request, id):
#     # cat_id = request.GET(id)
#     auction = Auction()
#     filtered_cat = Auction.objects.filter(category=id)
#     # filtered_cat = auction.category.all().filter(category=id)
#     return render(request, "auctions/category.html", {
#         "id": id,
#         "filtered_cat": filtered_cat
#     })
#
#
# @login_required()
# def focus(request, id):
#     focused_product = Auction.objects.get(id=id)
#     comment = Comment.objects.filter(prod_id=id)
#     added = Watchlist.objects.filter(prod_id=id, user=request.user.username)
#     current_user = request.user.username
#     bid = Bid.objects.filter(prod_id=id)
#     return render(request, "auctions/focus.html", {
#         "id": id,
#         "comment": comment,
#         "added": added,
#         "bid": bid,
#         "current_user":current_user,
#         "focused_product": focused_product,
#     })
#
#
# @login_required()
# def bid(request, id):
#     if request.method == "POST":
#         focused_product = Auction.objects.get(id=id)
#         current_price = focused_product.price
#         new_bid = int(request.POST.get('new_bid'))
#         if current_price>new_bid:
#             return render(request, "auctions/focus.html", {
#                 "id": id,
#                 "focused_product": focused_product,
#                 "message": "Bid Amount shall be higher."
#             })
#         else:
#             focused_product.price = new_bid
#             focused_product.save()
#             BID = Bid()
#             BID.user = request.user.username
#             BID.bid = new_bid
#             BID.title = focused_product.title
#             BID.prod_id = focused_product.id
#             BID.save()
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return render("request", "auctions/focus.html")
#
#
# @login_required()
# def comment(request, id):
#     if request.method == "POST":
#         focused_product = Auction.objects.get(id=id)
#         new_comment = request.POST.get('new_comment')
#         COMMENT = Comment()
#         COMMENT.user = request.user.username
#         COMMENT.comment = new_comment
#         COMMENT.prod_id = focused_product.id
#         COMMENT.date = datetime.datetime.now().replace(microsecond=0)
#         COMMENT.save()
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         return render(request, "auctions/focus.html", {
#             "id": id
#         })
#
#
# @login_required()
# def add_watchlist(request, id):
#     focused_product = Auction.objects.get(id=id)
#     added = Watchlist.objects.filter(prod_id=id, user=request.user.username)
#     if request.method == "POST":
#         obj = Watchlist.objects.filter(prod_id=id, user=request.user.username)
#         if obj:
#             obj.delete()
#             focused_product = Auction.objects.get(id=id)
#             added = Watchlist.objects.filter(prod_id=id, user=request.user.username)
#             return render(request, "auctions/focus.html", {
#                 "focused_product": focused_product,
#                 "added": added,
#             })
#         else:
#             obj = Watchlist()
#             obj.user = request.user.username
#             obj.prod_id = id
#             obj.save()
#             # returning the updated content
#             focused_product = Auction.objects.get(id=id)
#             added = Watchlist.objects.filter(prod_id=id, user=request.user.username)
#             return render(request, "auctions/focus.html", {
#                 "focused_product": focused_product,
#                 "added": added,
#             })
#     else:
#         return render(request, "auctions/focus.html", {
#             "focused_product": focused_product,
#             "added": added,
#         })
#
#
# @login_required()
# def watchlist(request):
#     if request.method == "GET":
#         items = Watchlist.objects.filter(user=request.user.username)
#         auctions = Auction.objects.all()
#
#         all_ids = []
#         for item in items:
#             id = item.prod_id
#             all_ids.append(id)
#
#         displays = []
#
#         for id in all_ids:
#             product = Auction.objects.filter(id=id)
#             displays.append(product)
#
#         context = {
#             'items': items,
#             'auctions': auctions,
#             'all_ids':all_ids,
#             'displays':displays,
#         }
#         return render(request, "auctions/watchlist.html", context)
#
#
# @login_required(login_url='/login')
# def closebid(request, id):
#     winobj = Winner()
#     listobj = Auction.objects.get(id=id)
#     # obj = get_object_or_None(Bid, listingid=product_id)
#     obj = Bid.objects.filter(prod_id=id, user=request.user.username)
#     if not obj:
#         message = "Deleting Bid"
#         msg_type = "danger"
#     else:
#         bidobj = Bid.objects.get(prod_id=id)
#         winobj.owner = request.user.username
#         winobj.winner = bidobj.user
#         winobj.prod_id = id
#         winobj.winprice = bidobj.bid
#         winobj.title = bidobj.title
#         winobj.save()
#         message = "Bid Closed"
#         msg_type = "success"
#         # removing from Bid
#         bidobj.delete()
#     # removing from watchlist
#     if Watchlist.objects.filter(prod_id=id):
#         watchobj = Watchlist.objects.filter(prod_id=id)
#         watchobj.delete()
#     # removing from Comment
#     if Comment.objects.filter(prod_id=id):
#         commentobj = Comment.objects.filter(prod_id=id)
#         commentobj.delete()
#     # removing from Listing
#     listobj.delete()
#     # retrieving the new products list after adding and displaying
#     # list of products available in WinnerModel
#     winners = Winner.objects.all()
#     # checking if there are any products
#     empty = False
#     if len(winners) == 0:
#         empty = True
#     return render(request, "auctions/closedlisting.html", {
#         "products": winners,
#         "empty": empty,
#         "message": message,
#         "msg_type": msg_type
#     })
#
#
# # view to see closed listings
# @login_required(login_url='/login')
# def closedlisting(request):
#     # list of products available in WinnerModel
#     winners = Winner.objects.all()
#     # checking if there are any products
#     empty = False
#     if len(winners) == 0:
#         empty = True
#     return render(request, "auctions/closedlisting.html", {
#         "products": winners,
#         "empty": empty
#     })