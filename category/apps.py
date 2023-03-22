from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'
    verbose_name='دسته بندی'
    
    def ready(self):
        import category.signals
    

