# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import openerp
from openerp.osv import fields, osv, orm
from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp import http

_logger = logging.getLogger(__name__)


class Home_tkobr(openerp.addons.web.controllers.main.Home):
    
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        openerp.addons.web.controllers.main.ensure_db()
        
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
        
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID
        
        values = request.params.copy()
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect
        
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None
        
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db,
                request.params['login'], request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = 'Login failed due to one of the following reasons'
            values['reason1'] = '- Wrong login/password'
            values['reason2'] = '- User not allowed to have multiple logins'
            values['reason3'] = '- User not allowed to login at this specific time or day'
        return request.render('web.login', values)


class Session_tkobr(openerp.addons.web.controllers.main.Session):
    
    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID
        res_user = request.registry.get('res.users').browse(request.cr, request.uid,
            request.session.uid, context=request.context)
        # Update session
#         if res_user:
#             res_user.write(request.cr, request.uid,
#             {'logged_in': False, 'expiration_date': None, 'session_id': None}, context=request.context)
#         request.session.logout(keep_db=True)
#         return werkzeug.utils.redirect(redirect, 303)
        return super(Session_tkobr, self).logout(redirect)

