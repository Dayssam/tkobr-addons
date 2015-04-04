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
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

LOGOUT_TYPES = [('ur', 'User Request'),
                ('to', 'Timeout'),
                ('re', 'Rule enforcing')]

class ir_sessions(osv.osv):
    _name = 'ir.sessions'
    _description = "Sessions"
    
    _columns = { 
        'user_id' : fields.many2one('res.users', 'User', ondelete='cascade',
            required=True),
        'session_id' : fields.char('Session ID', size=100, required=True),
        'expiration_date' : fields.datetime('Expiration Date', required=True,
            index=True),
        'logged_in': fields.boolean('Logged in', required=True, index=True),
        'date_login': fields.datetime('Login', required=True),
        'date_logout': fields.datetime('Logout'),
        'logout_type': fields.selection(LOGOUT_TYPES, 'Logout Type'),
        }

    # scheduler function to validate users session
    def validate_sessions(self, cr, uid):
#         ids = self.search(cr, SUPERUSER_ID,
#             [('expiration_date', '<=', datetime.strftime(fields.datetime.context_timestamp(cr, SUPERUSER_ID,
#                     datetime.strptime(fields.datetime.now(),
#                     DEFAULT_SERVER_DATETIME_FORMAT)), DEFAULT_SERVER_DATETIME_FORMAT)),
#             ('logged_in', '=', True)])
#         session_ids = self.browse(cr, SUPERUSER_ID, ids)
#         for session in session_ids:
#             self.user_id.clear_session(cr, session.user_id.id)
        return True
