from unfold.components import register_component, BaseComponent
from unfold.components import ComponentRegistry



@register_component
class Components(BaseComponent):
    template_name = "/unfold/helpers/header.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "some_variable": [
                {
                    "title": "dark mode",
                },
                {
                    "title": "light mode",
                }
            ]
        })
        return context
    
