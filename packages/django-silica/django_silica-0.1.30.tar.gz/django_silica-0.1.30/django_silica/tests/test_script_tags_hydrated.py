import time

from selenium.webdriver.common.by import By

from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest, SilicaBrowserTestCase
from django_silica.SilicaComponent import SilicaComponent


class Component(SilicaComponent):
    show_content = False

    def inline_template(self):
        return """
            <div>
                {% if show_content %}
                    <script>
                        console.log('yoo')
                    </script>
                {% endif %}
                <button silica:click.prevent="show_content = True" id="button">Show content</button>
            </div>
        """


class ScriptHydrationTestCase(SilicaBrowserTestCase):
    def test_script_tag_is_hydrated(self):
        self.selenium.get(self.live_server_url + "/silica/tests/script-tags-are-hydrated")

        self.selenium.find_element(By.ID, 'button').click()
        time.sleep(0.2)

        # # print the returned source
        # print(self.selenium.page_source)

        # # print the js console
        console_logs = self.selenium.get_log('browser')
        self.assertTrue(len(console_logs) == 1)
        self.assertTrue("yoo" in console_logs[0]['message'])




