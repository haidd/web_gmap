# -*- coding: utf-8 -*-
# Copyright 2018 Hai Dinh <haidd.uit@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_map_url_config_param(self):
        '''
        Get google map url
        :return api_keyir_config_parameter_data
        '''
        parameter_model = self.env['ir.config_parameter']
        map_url = \
            parameter_model.get_param('google_map_url', False)
        if not map_url:
            raise exceptions.Warning(_('No page prefix parameter specified!'))
        return map_url

    @api.model
    def _get_api_key_config_param(self):
        '''
        Get google map api key
        :return api_key
        '''
        parameter_model = self.env['ir.config_parameter']
        api_key = \
            parameter_model.get_param('google_map_api_key', False)
        if not api_key:
            raise exceptions.Warning(_('No page prefix parameter specified!'))
        return api_key

    @api.multi
    def button_show_map(self):
        for partner in self:
            if not partner.date_localization:
                # Set latitude and longitude
                partner.geo_localize()
        return {
            'type': 'ir.actions.act_url',
            'url': '/webgmap/show_map/' + str(self.ids),
            'target': 'new',
        }
