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


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Set default values for approval status
        food_approval_status = 'Not Requested'
        hall_approval_status = 'Not Requested'
        activity_approval_status = 'Not Requested'

        if self.request.user.is_authenticated and self.request.user.is_organizer:
            try:
                organization = self.request.user.organizer.organization

                # Fetch approval status for each feature (food, hall, activity)
                food_approval_status = self.get_approval_status(organization, 'food_and_beverage')
                hall_approval_status = self.get_approval_status(organization, 'conversation_hall')
                activity_approval_status = self.get_approval_status(organization, 'fun_and_activities')

            except AttributeError:
                pass  # Handle case if the user does not have an associated organization

        context['food_approval_status'] = food_approval_status
        context['hall_approval_status'] = hall_approval_status
        context['activity_approval_status'] = activity_approval_status

        return context

    def get_approval_status(self, organization, tag):
        """
        Helper function to get the approval status for a feature (food, hall, or activity)
        """
        approval_request = AdminApprovalRequest.objects.filter(
            organization=organization, tag=tag
        ).first()

        if approval_request:
            if approval_request.is_approved:
                return 'Approved'
            return 'Pending'
        return 'Not Requested'