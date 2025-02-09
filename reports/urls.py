from django.urls import path
from .views import (
    issue_list,
    issue_detail,
    report_issue,
    admin_dashboard,
    admin_login,
    update_issue_status,
    vote_issue,
    add_comment,
)

urlpatterns = [
    path("", issue_list, name="issue_list"),
    path('admin/login/', admin_login, name='admin_login'),  # Login page for the admin
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),  # Admin dashboard
    path("<int:issue_id>/", issue_detail, name="issue_detail"),  # Issue detail page
    path("report/", report_issue, name="report_issue"),  # Report an issue page
    path("admin/update/<int:issue_id>/", update_issue_status, name="update_issue_status"),  # Admin updates issue status
    path("vote/<int:issue_id>/", vote_issue, name="vote_issue"),  # User voting on an issue
    path("comment/<int:issue_id>/", add_comment, name="add_comment"),  # Adding a comment to an issue
]
