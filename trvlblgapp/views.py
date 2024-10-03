from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.
def index(re):
    return render(re,'index.html')
def about(re):
    return render(re,'about.html')
def home(re):
    return redirect(index)
def feedback(re):
    return render(re,'contact.html')
def user_home(re):
    user = Register.objects.get(username=re.session.get('uid'))
    return render(re, 'user_home.html', {'user': user})

# ------------------------------ GALLERY ------------------------------
# ------------------- All data view -------------------
def gallery(re):
    data =BlogPost.objects.all()
    return render(re,'gallery.html',{'data':data})

# ------------------- Single data view -------------------
def single_view(request, post_id):
   post = get_object_or_404(BlogPost, id=post_id)
   return render(request, 'single_post_view.html', {'post': post})

# ------------------------------ GALLERY ------------------------------
def view_feedback(request):
    feedback = Feedback.objects.all()
    return render(request, 'contact.html', {'feedback': feedback})

# ------------------------------ REGISTER ------------------------------
def register(re):
    if re.method == 'POST':
        first_name = re.POST.get('first_name')
        last_name = re.POST.get('last_name', '')  # Optional
        email = re.POST.get('email')
        mob_no = re.POST.get('mob_no')
        username = re.POST.get('username')
        password = re.POST.get('password')
        confirm_password = re.POST.get('confirm_password')
        pro_pic = re.FILES.get('pro_pic', None)  # Optional

        if password != confirm_password:
            messages.error(re, "Passwords do not match!")
            return redirect(register)

        # Check if the username or email already exists
        if Register.objects.filter(username=username).exists():
            messages.error(re, "Username already exists!")
            return redirect(register)

        if Register.objects.filter(email=email).exists():
            messages.error(re, "Email already exists!")
            return redirect(register)

        # Create the user
        user = Register(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mob_no=mob_no,
            username=username,
            password=password,
            pro_pic=pro_pic
        )
        user.save()
        messages.success(re, "Registration successful!")
        return redirect(login)

    return render(re, 'user_registration.html')


# ------------------------------ LOGIN/LOGOUT ------------------------------
def login(re):
    if re.method == 'POST':
        identifier = re.POST['identifier']  # Can be either username or email
        password = re.POST['password']
        try:
            data = Register.objects.get(Q(username=identifier) | Q(email=identifier))
            if (identifier == data.username or identifier == data.email) and password == data.password:
                re.session['uid'] = data.username
                return redirect(user_home)
            else:
                messages.error(re, 'Invalid Username/Email or Password')
        except Register.DoesNotExist:
            messages.error(re, 'User does not exist.')
    return render(re, 'user_login.html')

def logout(re):
    if 'uid' in re.session:
        re.session.flush()
        return redirect(home)

# ------------------------------ PROFILE ------------------------------
def user_profile(re):
    if 'uid' in re.session:
        u = Register.objects.get(username=re.session['uid'])
        return render(re,'profile_view.html',{'user':u})

def pro_edit(re,id):
    if 'uid' in re.session:
        user = Register.objects.get(pk=id)
        if re.method == 'POST':
            user.first_name = re.POST['fname']
            user.last_name = re.POST['lname']
            user.email = re.POST['email']
            user.mob_no = re.POST['nmbr']
            user.address = re.POST['address']
            user.state = re.POST['state']
            user.country = re.POST['country']
            user.username = re.POST['username']
            try:
                user.pro_pic = re.FILES['img']
                import os
                os.remove()
                user.save()
            except:
                user.save()
                return redirect(update_profile,id)
        return render(re,'profile_update.html',{'user':user})

def update_profile(re,id):
    if 'uid' in re.session:
        if re.method == 'POST':
            form = Profile(re.POST,re.FILES)
            if form.is_valid():
                a = form.cleaned_data['fname']
                b = form.cleaned_data['lname']
                c = form.cleaned_data['email']
                d = form.cleaned_data['nmbr']
                e = form.cleaned_data['address']
                f = form.cleaned_data['state']
                g = form.cleaned_data['country']
                h = form.cleaned_data['username']
                i = form.cleaned_data['img']
                Register.objects.filter(pk=id).update(first_name=a,last_name=b,email=c,mob_no=d,addrress=e,state=f,country=g,username=h,pro_pic=i)
                messages.success(re,'Profile Updated Successfully')
                return redirect(user_profile)
            data = Register.objects.all()
            return render(re,'profile_update.html',{'user':data})
            form = Profile()
            return render(re,'profile_update.html',{'form',form})
        return redirect(user_profile)

# ------------------------------ POST CREATION ------------------------------
def create(re):
    if 'uid' in re.session:
        if re.method == 'POST':
            user_details = Register.objects.get(username=re.session['uid'])
            title = re.POST.get('title')
            description = re.POST.get('description')
            place = re.POST.get('place')
            picture = re.FILES.get('picture')

            post = BlogPost(user_details=user_details, title=title,place=place, content=description, image=picture)
            post.save()

            re.session['message'] = "Post created"
            return redirect(create)

        return render(re, 'post_creation.html')

@api_view(['POST'])
def create_post_api(request):
    if 'uid' in request.session:
        if request.method == 'POST':
            serializer = BlogPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_details=Register.objects.get(id=request.session.get('uid')))
                return Response({"message": "Post created"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------ POST VIEW ------------------------------
def view(re):
    if 'uid' in re.session:
        user = get_object_or_404(Register, username=re.session['uid'])
        data = BlogPost.objects.filter(user_details=user.id)  # Use user.id to filter BlogPost
        return render(re, 'post_view.html', {'data': data})
    else:
        return redirect(login)

# ------------------------------ DELETE POST ------------------------------
@api_view(['DELETE'])
def delete_post_api(request, post_id):
    if 'uid' in request.session:
        try:
            post = BlogPost.objects.get(id=post_id)
            post.delete()
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------ UPDATE POST ------------------------------
def update_post(request, post_id):
    if 'uid' in request.session:
        post = get_object_or_404(BlogPost, id=post_id)

        if request.method == 'POST':
            post.title = request.POST.get('title')
            post.content = request.POST.get('description')
            post.place = request.POST.get('place')
            if request.FILES.get('picture'):
                post.image = request.FILES.get('picture')

            post.save()

            request.session['message'] = "Post updated successfully"
            return redirect(view)

        return render(request, 'post_update.html', {'post': post})


@api_view(['PUT'])
def update_post_api(request, post_id):
    if 'uid' in request.session:
        post = get_object_or_404(BlogPost, id=post_id)
        serializer = BlogPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

# ------------------------------ USER FEEDBACK ------------------------------
def user_feedback(re):
    if 'uid' in re.session:  # Ensure user is logged in
        user = Register.objects.get(username=re.session['uid'])
        if re.method == 'POST':
            msg = re.POST['message']
            Feedback.objects.create(user_details=user, feedback=msg)
            messages.success(re, 'Thank you for your feedback! Feedback submitted successfully.')
            return redirect(user_feedback)
        return render(re, 'user_feedback.html', {'user': user})
    return redirect(login)