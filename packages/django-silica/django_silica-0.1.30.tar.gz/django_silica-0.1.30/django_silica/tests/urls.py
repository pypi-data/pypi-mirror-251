from django.urls import path
from django.views.generic import TemplateView

from django_silica.silica.tests.ConcurrencyTest import ConcurrencyTest
from django_silica.silica.tests.Lifecycle import Lifecycle
from django_silica.silica.tests.TagProps import TagProps

class ConcurrencyTestView(TemplateView):
    template_name = "concurrency_test_view.html"

class TagPropsView(TemplateView):
    template_name = "tag_props_view.html"

class ComponentTagTest(TemplateView):
    template_name = "component_tag_test.html"

class ComponentSubfolderTest(TemplateView):
    template_name = "component_subfolder_test.html"

class QueryParamsTestView(TemplateView):
    template_name = "query_params_test_view.html"

class CachePersistTestView(TemplateView):
    template_name = "cache_persist_test_view.html"

class ScriptHydratedView(TemplateView):
    template_name = "script_hydrated_test_view.html"

urlpatterns = [
    path("lifecycle", Lifecycle.as_view(), name="lifecycle"),
    path("silica/tests/concurrency", ConcurrencyTestView.as_view()),
    path("silica/tests/tag-props", TagPropsView.as_view()),
    path("silica/tests/component-tag-test", ComponentTagTest.as_view()),
    path("silica/tests/component-subfolder-test", ComponentSubfolderTest.as_view()),
    path("silica/tests/query-params", QueryParamsTestView.as_view()),
    path("silica/tests/cache-persist", CachePersistTestView.as_view()),
    path("silica/tests/script-tags-are-hydrated", ScriptHydratedView.as_view()),
    # ... add more testing URLs as needed
]
