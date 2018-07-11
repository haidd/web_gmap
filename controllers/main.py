# -*- coding: utf-8 -*-
# Copyright 2018 Hai Dinh <haidd.uit@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class WebGmap(http.Controller):

    @http.route('/webgmap/show_map/<string:partner_str_ids>',
                type='http', auth="user", website=True)
    def show_map(self, partner_str_ids, **kw):
        partner_ids = eval(partner_str_ids)
        partner_obj = request.env['res.partner']
        partners = partner_obj.browse(partner_ids)

        api_key = partners._get_api_key_config_param()
        map_url = partners._get_map_url_config_param()
        link_script = '<script async defer src="%s?key=%s"></script>' % (
            map_url, api_key)

        lst_info = []
        for partner in partners:
            latitude = partner.partner_latitude
            longitude = partner.partner_longitude
            infomation = \
                partner.with_context(show_address=True).name_get()[0][1]
            infomation = infomation.encode(
                'utf-8') and infomation.encode('utf-8').replace('\n', ', ')

            lst_info.append([latitude, longitude, infomation])

        return http.request.render('web_gmap.show_map_template_website', {
            'link_script': link_script,
            'lst_info': lst_info,
        })
