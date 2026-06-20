import mistune
from django.conf import settings
from django.utils.module_loading import import_string


class Renderer(mistune.HTMLRenderer):
    def link(self, text, url, title=None):
        if url in settings.MKDN:
            fn = import_string(settings.MKDN[url])
            result = fn(text)
            if result:
                url = result

        return super().link(text, url, title)


markdown = mistune.create_markdown(
    escape=False, renderer=Renderer(), plugins=["strikethrough", "footnotes", "table", "speedup"]
)
