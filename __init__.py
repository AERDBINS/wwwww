from .start_handler import router as start_router
from .menu_about import router as about_router
from .menu_courses import router as courses_router
from .language_handler import router as lang_router
from .course_enroll import router as enroll_router
from .registration import router as registration_router
from .admin import router as admin_router
from .test import router as test_router
from .settings import router as settings_router

routers = [
    start_router,
    about_router,
    courses_router,
    lang_router,
    enroll_router,
    registration_router,
    admin_router,
    test_router,
    settings_router
]
