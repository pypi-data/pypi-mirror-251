# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.work_object",
    ]

    _work_log_create_page = True
