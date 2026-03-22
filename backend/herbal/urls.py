from django.urls import path

from .views.subjects.lists.subject_list_view import subject_list_view
from .views.subjects.creates.subject_create_view import subject_create_view
from .views.subjects.details.subject_detail_view import subject_detail_view
from .views.subjects.updates.subject_update_view import subject_update_view
from .views.subjects.form_view.subject_form_view import subject_form_view

from .views.visits.visit_dashboard_view import visit_dashboard_view
from .views.visits.visit_mark_missed_view import visit_mark_missed
from .views.visits.visit_mark_pending import visit_mark_pending

from .views.screening.screening_form_view import screening_form_view
from .views.screening.screening_update_view import screening_update_view

from .views.enrollments.enrollment_create_view import enrollment_create_view
from .views.enrollments.enrollment_form_view import enrollment_form_view


from .views.visits.unscheduled_create_view import unscheduled_create_view
from .views.visits.unscheduled_update_view import unscheduled_update_view
from .views.visits.visit_start_view import visit_start_view
from .views.visits.visit_update_view import visit_update_view
from .views.crfs.crf1.crf1_create_view import crf1_create_view
from .views.crfs.crf1.crf1_update_view import crf1_update_view
from .views.crfs.crf2.crf2_create_view import crf2_create_view
from .views.crfs.crf2.crf2_update_view import crf2_update_view
from .views.crfs.crf3.crf3_create_view import crf3_create_view
from .views.crfs.crf3.crf3_update_view import crf3_update_view
from .views.crfs.crf4.crf4_create_view import crf4_create_view
from .views.crfs.crf4.crf4_update_view import crf4_update_view
from .views.crfs.crf5.crf5_create_view import crf5_create_view
from .views.crfs.crf5.crf5_update_view import crf5_update_view
from .views.crfs.crf6.crf6_create_view import crf6_create_view
from .views.crfs.crf6.crf6_update_view import crf6_update_view
from .views.crfs.crf7.crf7_create_view import crf7_create_view
from .views.crfs.crf7.crf7_update_view import crf7_update_view

# QUERIES
from. views.queries.query_create_view import query_create_view
from. views.queries.query_response_view import query_response_view
from. views.queries.query_close_view import query_close_view

app_name = "herbal"

urlpatterns = [
    # SUBJECTS
    path("subjects/", subject_list_view, name="subjects-list"),
    # path("subjects/create/", subject_create_view, name="subject-create"),
    path("subjects/<int:pk>/", subject_detail_view, name="subjects-detail"),
    # path("subjects/<int:pk>/edit/", subject_update_view, name="subjects-update"),
    
    path("subjects/create/", subject_form_view, name="subject-create"),
    path("subjects/<int:pk>/edit/", subject_form_view, name="subject-update"),
    
    # SCREENING
    # path("screening/<int:pk>/", screening_form_view, name="screening-create"),
    # path("screening/<int:pk>/update/", screening_form_view, name="screening-update"),
    path("screening/<int:pk>/", screening_form_view, name="screening-form"),
    # ENROLLMENT
    path("enrollment/<int:pk>/", enrollment_form_view, name="enrollment-create"),
    path(
        "enrollment/<int:pk>/update/", enrollment_form_view, name="enrollment-update"
    ),
    # VISITS
    path("visits/dashboard/", visit_dashboard_view, name="visit-dashboard"),
    path("visits/<int:pk>/missed/", visit_mark_missed, name="visit-mark-missed"),
    path("visits/<int:pk>/pending/", visit_mark_pending, name="visit-mark-pending"),
    path("unscheduled/create/<int:pk>/", unscheduled_create_view, name="unscheduled-create"),
    path("unscheduled/update/<int:pk>/", unscheduled_update_view, name="unscheduled-update"),
    path("visits/<int:pk>/start/", visit_update_view, name="visit-start"),
    path("visits/<int:pk>/update/", visit_update_view, name="visit-update"),
    # CRFS
    # CRF1
    path("crf1/<int:pk>/", crf1_create_view, name="crf1-create"),
    path("crf1/<int:pk>/update/", crf1_update_view, name="crf1-update"),
    # CRF2
    path("crf2/<int:pk>/", crf2_create_view, name="crf2-create"),
    path("crf2/<int:pk>/update/", crf2_update_view, name="crf2-update"),
    # CRF3
    path("crf3/<int:pk>/", crf3_create_view, name="crf3-create"),
    path("crf3/<int:pk>/update/", crf3_update_view, name="crf3-update"),
    # CRF4
    path("crf4/<int:pk>/", crf4_create_view, name="crf4-create"),
    path("crf4/<int:pk>/update/", crf4_update_view, name="crf4-update"),
    # CRF5
    path("crf5/<int:pk>/", crf5_create_view, name="crf5-create"),
    path("crf5/<int:pk>/update/", crf5_update_view, name="crf5-update"),
    # CRF6
    path("crf6/<int:pk>/", crf6_create_view, name="crf6-create"),
    path("crf6/<int:pk>/update/", crf6_update_view, name="crf6-update"),
    # CRF7
    path("crf7/<int:pk>/", crf7_create_view, name="crf7-create"),
    path("crf7/<int:pk>/update/", crf7_update_view, name="crf7-update"),
    
    # QUERIES
    path("query/<int:visit_id>/create/", query_create_view, name="query-create"),
    path("query/<int:pk>/response/", query_response_view, name="query-response"),
    path("query/<int:pk>/close/", query_close_view, name="query-close"),
]
