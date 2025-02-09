from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Issue
from .models import Issue, Comment, Vote
from .forms import IssueForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

VULGAR_WORDS = ['badword1', 'badword2', 'badword3']

def issue_list(request):
    issues = Issue.objects.all().order_by('-created_at')
    # Prepare JSON data for map integration
    issues_json = list(issues.values("id", "title", "status", "lat", "lng", "location"))
    return render(request, "reports/issue_list.html", {"issues": issues, "issues_json": issues_json})

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    comment_form = CommentForm()
    return render(request, "reports/issue_detail.html", {"issue": issue, "comment_form": comment_form})

def report_issue(request):
    if request.method == 'POST':
        # Extract the data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        lat = request.POST.get('lat')  # Latitude
        lng = request.POST.get('lng')  # Longitude

        # If the user is logged in, use their user ID; otherwise, it will be None
        user = request.user if request.user.is_authenticated else None

        # Ensure lat/lng are present (they should be coming from the map or user)
        if not lat or not lng:
            return JsonResponse({'error': 'Location is required.'}, status=400)

        # Create the issue and save it
        new_issue = Issue(
            title=title,
            description=description,
            category=category,
            location=location,
            image=image,
            user=user,  # Use user if logged in
            lat=lat,  # Store latitude
            lng=lng,  # Store longitude
        )
        new_issue.save()

        return JsonResponse({'message': 'Issue reported successfully'}, status=200)

    return render(request, 'reports/report_issue.html')

# views.py

def add_comment(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == "POST":
        comment_text = request.POST.get('comment_text')
        if comment_text:
            # Save the comment to the database (make sure the model and form are set up)
            comment = Comment(issue=issue, text=comment_text)
            comment.save()
            return redirect('issue_detail', issue_id=issue.id)  # Redirect back to issue detail page
    return redirect('issue_detail', issue_id=issue.id)

def vote_issue(request, issue_id):
    if request.method == "POST":
        vote_type = request.POST.get("vote_type")
        issue = get_object_or_404(Issue, id=issue_id)
        user = request.user

        # Ensure the user can vote only once per issue
        if Vote.objects.filter(issue=issue, user=user).exists():
            return JsonResponse({"error": "You have already voted on this issue."}, status=400)

        # Create or update the vote
        vote, created = Vote.objects.get_or_create(issue=issue, user=user, defaults={"vote_type": vote_type})
        if not created and vote.vote_type != vote_type:
            vote.vote_type = vote_type
            vote.save()

        # Update aggregated vote count
        upvotes = issue.votes.filter(vote_type="Upvote").count()
        downvotes = issue.votes.filter(vote_type="Downvote").count()
        issue.votes_count = upvotes - downvotes
        issue.save()

        return JsonResponse({"votes_count": issue.votes_count})

    return JsonResponse({"error": "Invalid request method."}, status=405)

# Define the admin_dashboard view (you can customize it)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

# Define the update_issue_status view (you can customize it)
def update_issue_status(request, issue_id):
    # Add logic to update issue status
    return render(request, 'update_issue_status.html', {'issue_id': issue_id})