from .home import UserHomeView, home
from .project import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView
)
from .task import (
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskStatusUpdateView
)
from .comment import CommentCreateView
from .developer import (
    DevelopersView,
    DevelopersAjaxDeleteView)
from .time_journal import TimeJournalCreateView
