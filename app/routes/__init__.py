from .auth import router as auth_router
from .competitions import router as competitions_router
from .matches import router as matches_router
from .reservations import router as reservations_router
from .users import router as users_router
from .notifications import router as notifications_router 
from .rooms import router as rooms_router  
from .admin import router as admin_router  

routers = [
    auth_router,
    competitions_router,
    matches_router,
    reservations_router,
    users_router,
    notifications_router, 
    rooms_router,
    admin_router,
]
