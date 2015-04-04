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
from datetime import date, datetime, time, timedelta
from openerp.addons.base.ir.ir_cron import _intervalTypes
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
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
                self.save_session(request.cr, uid, request.context)
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = 'Login failed due to one of the following reasons'
            values['reason1'] = '- Wrong login/password'
            values['reason2'] = '- User not allowed to have multiple logins'
            values['reason3'] = '- User not allowed to login at this specific time or day'
        return request.render('web.login', values)
        
    # insert session_id and session expiry into res.users
    def save_session(self, cr, uid, context=None):
        if isinstance(uid, list): user_id = uid[0]
        user_obj = request.registry.get('res.users')
        session_obj = request.registry.get('ir.sessions')
        user_id = user_obj.browse(cr, SUPERUSER_ID, uid, context=context)
        g_exp_date = datetime.now() + _intervalTypes['months'](3)
#         fields.datetime.context_timestamp(cr, SUPERUSER_ID, 
#                 datetime.strptime(fields.datetime.now(),
#                 DEFAULT_SERVER_DATETIME_FORMAT)) + _intervalTypes['months'](3)
        if uid != SUPERUSER_ID or 1:
            if user_id.interval_type:
                u_exp_date = datetime.now() + _intervalTypes[user_id.interval_type](user_id.interval_number)
#                 fields.datetime.context_timestamp(cr, SUPERUSER_ID,
#                     datetime.strptime(fields.datetime.now(),
#                     DEFAULT_SERVER_DATETIME_FORMAT)) + _intervalTypes[user_id.interval_type](user_id.interval_number)
            else:
                u_exp_date = g_exp_date
            g_no_multiple_sessions = False
            u_no_multiple_sessions = user_id.no_multiple_sessions
            for group in user_id.groups_id:
                if group.no_multiple_sessions:
                    g_no_multiple_sessions = True
                if group.interval_type:
                    t_exp_date = datetime.now() + _intervalTypes[group.interval_type](group.interval_number)
#                     fields.datetime.context_timestamp(cr, SUPERUSER_ID,
#                         datetime.strptime(fields.datetime.now(),
#                         DEFAULT_SERVER_DATETIME_FORMAT)) + _intervalTypes[group.interval_type](group.interval_number)
                    if t_exp_date < g_exp_date:
                        g_exp_date = t_exp_date
            if g_no_multiple_sessions:
                u_no_multiple_sessions = True
            if g_exp_date < u_exp_date:
                u_exp_date = g_exp_date
        else:
            u_exp_date = g_exp_date
        sid = request.httprequest.session.sid
        return session_obj.create(cr, SUPERUSER_ID, {'user_id': uid,
            'session_id': sid,
            'expiration_date': datetime.strftime(u_exp_date, DEFAULT_SERVER_DATETIME_FORMAT),
            'date_login': fields.datetime.now(),
            'logged_in': True},
            context=context)


