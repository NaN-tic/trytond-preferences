# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


__all__ = ['OpenUserPreferences']
__metaclass__ = PoolMeta


class OpenUserPreferences(Wizard):
    'Open User Preferences'
    __name__ = 'open.user.preferences'
    start = StateView('res.user',
        'preferences.res_user_form_view', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Save', 'save', 'tryton-ok', default=True),
            ])
    save = StateTransition()

    def default_start(self, action):
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return {
            'name': user.name,
            'login': user.login,
            'cart': getattr(user, 'cart', False) and user.cart.id or None,
            'sale_device': getattr(user, 'sale_device', False)
                and user.sale_device.id or None,
            'shops': getattr(user, 'shops', [])
                and [s.id for s in user.shops] or None,
            'shop': getattr(user, 'shop', False) and user.shop.id or None,
            'subdivisions': getattr(user, 'subdivisions', [])
                and [s.id for s in user.subdivisions] or None,
            'subdivision': getattr(user, 'subdivision', False)
                and user.subdivision.id or None,
            }

    def transition_save(self):
        User = Pool().get('res.user')
        user = User(Transaction().user)
        values = self.start
        User.write([user], {
                'cart': getattr(values, 'cart', False)
                    and values.cart.id or None,
                'sale_device': getattr(values, 'sale_device', False)
                    and values.sale_device.id or None,
                'shop': getattr(values, 'shop', False)
                    and values.shop.id or None,
                'subdivision': getattr(values, 'subdivision', False)
                    and values.subdivision.id or None,
                })
        return 'end'
