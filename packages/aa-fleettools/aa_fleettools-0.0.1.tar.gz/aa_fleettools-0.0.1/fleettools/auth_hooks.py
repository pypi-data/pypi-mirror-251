from allianceauth import hooks
from allianceauth.services.hooks import UrlHook, MenuItemHook

from . import urls


class FleettoolsMenuItemHook(MenuItemHook):
    def __init__(self):
        super().__init__("Fleet Tools", "fas fa-space-shuttle", "fleettools:index", navactive=['fleettools:'])


@hooks.register('menu_item_hook')
def register_menu():
    return FleettoolsMenuItemHook()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'fleettools', 'fleettools/')
