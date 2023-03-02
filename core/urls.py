from django.urls import path,include
from rest_framework_nested import routers
from . import  views



router = routers.DefaultRouter()

router.register('products' , views.ProductViewSet , basename='products')
router.register("customers" , views.CustomerViewSet , basename="customers")
router.register('category' , views.CategoryViewSet)
router.register('stkpush' , views.STKPushViewSet, basename="stkush")
router.register('wallets' , views.WalletViewSet , basename="wallets")
router.register('referrals' , views.ReferralViewSet , basename="referrals")
router.register('loans' , views.LoanViewSet , basename="loans")
router.register(r'stk-push-callback', views.STKPushCallbackViewSet, basename='stk-push-callback')

# router.register('login', views.LoginViewSet, basename='login')
# products_router = routers.NestedDefaultRouter(router , 'products' , lookup='product')
# products_router.register('reviews' , views.ReviewViewSet , basename='product-reviews')


# urlpatterns = router.urls + products_router.urls
urlpatterns = router.urls 
# router.register("")
# urlpatterns = [
#     path('', views.index , name="index.html"),
#     router.urls,
# ]

# urlpatterns = router.urls

# urlpatterns = [
#     # ...
#     path('api/', include(router.urls)),
# ]