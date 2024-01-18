from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_wallets"
    verbose_name = "Wallets"

    class PretixPluginMeta:
        name = gettext_lazy("Wallets")
        author = "Robin Ferch"
        description = gettext_lazy("Allow users to save the ticket into wallet apps")
        visible = True
        version = __version__
        category = "FORMAT"
        compatibility = "pretix>=2.7.0"
        experimental = True

    def ready(self):
        from . import signals  # NOQA
