from django.apps import AppConfig


class GeneratorConfig(AppConfig):
    name = 'page_generator'

    def ready(self):
        import page_generator.signals
