from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback


# ✅ User gives new feedback
@login_required
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('profile')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})


#  View all feedback submitted by the current user
@login_required
def my_feedback_view(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'feedback/my_feedback.html', {'feedbacks': feedbacks})


#  Edit feedback
@login_required
def edit_feedback_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, user=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your feedback has been updated!')
            return redirect('my_feedback')
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'feedback/edit_feedback.html', {'form': form})


#  Delete feedback
@login_required
def delete_feedback_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, user=request.user)
    feedback.delete()
    messages.success(request, 'Your feedback has been deleted.')
    return redirect('my_feedback')