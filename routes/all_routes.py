from fastapi import APIRouter
from categories import categories
from comments import testimonials
from courses import featuredcourses_routes, popularcourses_routes, view_course
from contect import contect
from mentors import mentors
from login import google_login, login_auth_routes
from dashboard import hero_section
from ques_ans import ques_ans
from sponsors import sponsors


router = APIRouter()

router.include_router(login_auth_routes.router)
router.include_router(popularcourses_routes.router)
router.include_router(featuredcourses_routes.router)
router.include_router(google_login.router)
router.include_router(hero_section.router)
router.include_router(sponsors.router)
router.include_router(view_course.router)
router.include_router(categories.router)    
router.include_router(mentors.router)
router.include_router(testimonials.router)
router.include_router(ques_ans.router)
router.include_router(contect.router)