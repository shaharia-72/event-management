from django.views.generic import TemplateView
from django.shortcuts import render

from django.views.generic import TemplateView

from accounts.models import Organizer

from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from accounts.models import Organizer  # Import Organizer model

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from accounts.models import Organizer
from events.models import AdminApprovalRequest  # Assuming this model exists for approval status


from django.shortcuts import redirect
from django.views.generic import TemplateView
# from .models import AdminApprovalRequest

class HomePageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        # If the user is authenticated and is an organizer, check the organization and redirect
        if self.request.user.is_authenticated and self.request.user.is_organizer:
            # Try to fetch the organization for the user
            organization = self.request.user.organizer.organization
            if organization:
                # Check approval status and redirect to all_posts if valid
                return redirect('all_posts')  # Redirect to the all_posts view if an organizer has an organization

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Default approval statuses
        food_approval_status = 'Not Requested'
        hall_approval_status = 'Not Requested'
        activity_approval_status = 'Not Requested'

        # Check if the user is authenticated and an organizer
        if self.request.user.is_authenticated and self.request.user.is_organizer:
            try:
                # Try to get the organization of the authenticated user
                organization = self.request.user.organizer.organization

                # Fetch approval statuses for each feature (food, hall, activity)
                food_approval_status = self.get_approval_status(organization, 'food_and_beverage')
                hall_approval_status = self.get_approval_status(organization, 'conversation_hall')
                activity_approval_status = self.get_approval_status(organization, 'fun_and_activities')

            except AttributeError:
                # In case of any issues (e.g., no organization linked to the user)
                pass

        # Pass the approval statuses to the template
        context['food_approval_status'] = food_approval_status
        context['hall_approval_status'] = hall_approval_status
        context['activity_approval_status'] = activity_approval_status

        return context

    def get_approval_status(self, organization, tag):
        """
        Helper function to get the approval status for a feature (food, hall, or activity).
        """
        approval_request = AdminApprovalRequest.objects.filter(
            organization=organization, tag=tag
        ).first()

        # Return the status based on the approval request
        if approval_request:
            if approval_request.is_approved:
                return 'Approved'
            return 'Pending'
        return 'Not Requested'
