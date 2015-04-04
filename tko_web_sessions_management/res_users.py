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

import openerp
from openerp.osv import fields, osv, orm
from datetime import date, datetime, time, timedelta
from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.addons.base.ir.ir_cron import _intervalTypes
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class res_users(osv.osv):
    _inherit = 'res.users'
    
    _columns = {
        'login_calendar_id': fields.many2one('resource.calendar', 'Allowed Login', company_dependent=True),
        'no_multiple_sessions': fields.boolean('No Multiple Sessions', company_dependent=True),
        'interval_number': fields.integer('Default Session Duration', company_dependent=True),
        'interval_type': fields.selection([('minutes', 'Minutes'),
            ('hours', 'Hours'), ('work_days', 'Work Days'),
            ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')],
            'Interval Unit', company_dependent=True),
        'session_ids': fields.one2many('ir.sessions', 'user_id', 'User Sessions')
        }
    
#    def _login(self, db, login, password):
#        uid = super(res_users, self)._login(db, login, password)
#        if not uid:
#            return uid
#        else:
#            try:
#                session_id = request.httprequest.session.sid
#                sessions_obj = self.pool.get('ir.sessions')
#                user_obj = self.pool.get('res.users')
#                session_ids = sessions_obj.search(request.cr, SUPERUSER_ID,
#                    [('user_id', '=', uid),
#                     ('logged_in', '=', True),
#                     ('expiration_date', '>', fields.datetime.now())],
#                    context=request.context)
#                user_id = user_obj.browse(request.cr, SUPERUSER_ID, uid,
#                    context=request.context)
#                if session_ids and user_id.no_multiple_sessions:
#                    raise openerp.exceptions.AccessDenied()
#                else:
#                    self.save_session(request.cr, uid, request.context)
#            except openerp.exceptions.AccessDenied:
#                uid = False
#                _logger.warn("Multiple sessions are not allowed for security reasons.")
#                _logger.warn("User login calendar doesn't allow for security reasons")
#        return uid
    
    # clears session_id and session expiry from res.users
    def clear_session(self, cr, uid):
        if isinstance(uid, list): user_id = uid[0]
        self._logout(cr, uid)
        self.write(cr, SUPERUSER_ID, uid, {'logged_in': False})
    
    def _logout(self, cr, uid):
        if isinstance(user_id, list): user_id = uid[0]
        session_id = request.httprequest.session
        session_id.logout(self)
        
        