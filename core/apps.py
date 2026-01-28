from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        import core.signals  # noqa: F401 - connect post_save signal for Task


class TasksConfig(AppConfig):
    name = "tasks"
