from like2price.models import core


class Artist(core.Artist):
    class Meta(core.Artist.Meta):
        app_label = 'core'


class Item(core.Item):
    class Meta(core.Item.Meta):
        app_label = 'core'


class Sign(core.Sign):
    class Meta(core.Sign.Meta):
        app_label = 'core'
