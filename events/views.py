from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q
from .models import (
    FoodAndBeveragePost, ConversationHallPost, FunAndActivitiesPost,
    AdminApprovalRequest, Organization
)
from .forms import FoodAndBeveragePostForm, ConversationHallPostForm, FunAndActivitiesPostForm

# Create Post View
def create_post(request, post_type):
    if post_type == 'food_and_beverage':
        form = FoodAndBeveragePostForm(request.POST or None, request.FILES or None)
        template = 'create_food_post.html'
    elif post_type == 'conversation_hall':
        form = ConversationHallPostForm(request.POST or None, request.FILES or None)
        template = 'create_hall_post.html'
    elif post_type == 'fun_and_activities':
        form = FunAndActivitiesPostForm(request.POST or None, request.FILES or None)
        template = 'create_activity_post.html'
    else:
        messages.error(request, "Invalid post type!")
        return redirect('home')

    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.organization = request.user.organizer.organization
        post.save()
        messages.success(request, "Post created successfully!")
        return redirect('home')

    return render(request, template, {'form': form})

# Update Post View
def update_post(request, post_id, post_type):
    if post_type == 'food_and_beverage':
        post = get_object_or_404(FoodAndBeveragePost, id=post_id)
        form = FoodAndBeveragePostForm(request.POST or None, request.FILES or None, instance=post)
        template = 'update_food_post.html'
    elif post_type == 'conversation_hall':
        post = get_object_or_404(ConversationHallPost, id=post_id)
        form = ConversationHallPostForm(request.POST or None, request.FILES or None, instance=post)
        template = 'update_hall_post.html'
    elif post_type == 'fun_and_activities':
        post = get_object_or_404(FunAndActivitiesPost, id=post_id)
        form = FunAndActivitiesPostForm(request.POST or None, request.FILES or None, instance=post)
        template = 'update_activity_post.html'
    else:
        messages.error(request, "Invalid post type!")
        return redirect('home')

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Post updated successfully!")
        return redirect('home')

    return render(request, template, {'form': form, 'post': post})

# Delete Post View
def delete_post(request, post_id, post_type):
    if post_type == 'food_and_beverage':
        post = get_object_or_404(FoodAndBeveragePost, id=post_id)
    elif post_type == 'conversation_hall':
        post = get_object_or_404(ConversationHallPost, id=post_id)
    elif post_type == 'fun_and_activities':
        post = get_object_or_404(FunAndActivitiesPost, id=post_id)
    else:
        messages.error(request, "Invalid post type!")
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('home')

    return render(request, 'delete_post.html', {'post': post})

# Admin Approval Request View
class RequestAdminApprovalView(View):
    template_name = 'request_approval.html'

    def get(self, request, *args, **kwargs):
        try:
            organization = request.user.organizer.organization
        except AttributeError:
            messages.error(request, "You need to be an organizer with an associated organization.")
            return redirect('home')

        # Fetch the approval status for each feature
        food_approval_status = self.get_approval_status(organization, 'food_and_beverage')
        hall_approval_status = self.get_approval_status(organization, 'conversation_hall')
        activity_approval_status = self.get_approval_status(organization, 'fun_and_activities')

        context = {
            'food_approval_status': food_approval_status,
            'hall_approval_status': hall_approval_status,
            'activity_approval_status': activity_approval_status
        }
        return render(request, self.template_name, context)

    def get_approval_status(self, organization, tag):
        approval_request = AdminApprovalRequest.objects.filter(organization=organization, tag=tag).first()
        if approval_request:
            if approval_request.is_approved:
                return 'Approved'
            return 'Pending'
        return 'Not Requested'

# Some view to pass the approval statuses to the navbar template
def organizer_dashboard(request):
    if request.user.is_organizer:
        # Get the associated organization for the logged-in user
        organization = request.user.organizer.organization
        
        # Fetch the approval status for each feature
        food_approval_status = 'Approved' if organization.is_active_food_and_beverage else 'Not Approved'
        hall_approval_status = 'Approved' if organization.is_active_conversation_hall else 'Not Approved'
        activity_approval_status = 'Approved' if organization.is_active_fun_and_activities else 'Not Approved'
        
        # Pass approval statuses to navbar or the view that renders the navbar
        context = {
            'food_approval_status': food_approval_status,
            'hall_approval_status': hall_approval_status,
            'activity_approval_status': activity_approval_status
        }
        return render(request, 'organizer_dashboard.html', context)
    else:
        messages.error(request, "You are not an organizer.")
        return redirect('home')



# display after vesion updated at 10.15 PM monday 12-30-2024

from django.db.models import Q
from .models import FoodAndBeveragePost, ConversationHallPost, FunAndActivitiesPost
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FoodAndBeveragePost, ConversationHallPost, FunAndActivitiesPost

from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import FoodAndBeveragePost, ConversationHallPost, FunAndActivitiesPost



class AllPostsView(TemplateView):
    template_name = 'all_posts.html'

    def get(self, request, *args, **kwargs):
        # Fetch posts from each category
        food_posts = FoodAndBeveragePost.objects.all()
        hall_posts = ConversationHallPost.objects.all()
        activity_posts = FunAndActivitiesPost.objects.all()

        # Normalize data across different models
        posts = []

        # Food & Beverage
        for post in food_posts:
            posts.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'image': post.image.url if post.image else None,
                'price': post.price,  # Assuming 'price' is directly available
                'type': 'Food & Beverage',
            })

        # Conversation Hall
        for post in hall_posts:
            posts.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'image': post.images.url if post.images else None,
                'price': post.price_per_hour,  # Map price_per_hour to 'price'
                'type': 'Conversation Hall',
            })

        # Fun & Activities
        for post in activity_posts:
            posts.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'image': post.image.url if post.image else None,
                'price': post.price,
                'type': 'Fun & Activities',
            })

        # Pagination
        paginator = Paginator(posts, 6)  # Show 6 posts per page
        page = request.GET.get('page')
        paginated_posts = paginator.get_page(page)

        context = {
            'posts': paginated_posts,
        }
        return render(request, self.template_name, context)