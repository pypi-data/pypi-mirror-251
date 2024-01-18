from django_silica.tests.SilicaTestCase import SilicaBrowserTestCase
from django_silica.SilicaComponent import SilicaComponent


class CachePersistTestComponent(SilicaComponent):
    items = []

    def mount(self):
        self.items = ["foo", "bar", "baz"]

        # This test should evolve to something like, 'component class properties are not persisted between requests'
        # self.items += ["foo", "bar", "baz"]

    def inline_template(self):
        return """
            <div>
                {% for item in items %}
                    <div>Item count {{ forloop.counter }}</div>
                {% endfor %}
            </div>
        """


class CachePersistTestCase(SilicaBrowserTestCase):
    def test_cache_doesnt_persist_between_requests(self):
        self.selenium.get(self.live_server_url + "/silica/tests/cache-persist")

        # check to see if some text appears on the page
        self.assertTrue("Item count 1" in self.get_page_source())
        self.assertTrue("Item count 4" not in self.get_page_source())

        # refresh the page, mount should be called again, but with a fresh instance of the component,
        # without the items set from the previous mount
        self.selenium.refresh()

        self.assertTrue("Item count 1" in self.get_page_source())
        self.assertTrue("Item count 4" not in self.get_page_source())



