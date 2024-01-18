import logging

from werkzeug.exceptions import BadRequest, NotFound

from odoo import _

from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component

from odoo.addons.sm_maintenance.models.models_api_services_utils import api_services_utils

from . import schemas

_logger = logging.getLogger(__name__)


class ResPartnerService(Component):
    _inherit = "emc.rest.service"
    _name = "res.partner.services"
    _usage = "res-partner"
    _description = """
    Subscription Request Services
  """

    def get(self, _id):
        partner = self.env["res.partner"].search(
            [("id", "=", _id)]
        )
        if partner:
            return self._to_dict(partner)
        else:
            raise wrapJsonException(
                NotFound(_("No partner for id %s") % _id)
            )

    def search(self, vat=None, email=None, phone=None, member=None, coop_candidate=None):
        _logger.info(f"search by VAT: {vat}, email: {email}, phone: {phone}, member: {member}, cooperator candidate: {coop_candidate}")

        domain = []

        if vat:
            domain.append(("vat", "=", vat))
        if email:
            domain.append(("email", "=", email))
        if phone:
            domain.append(("phone", "=", phone))
        if member == "true":
            domain.append(("member", "=", True))
        elif member == "false":
            domain.append(("member", "=", False))
        if coop_candidate == "true":
            domain.append(("coop_candidate", "=", True))
        elif coop_candidate == "false":
            domain.append(("coop_candidate", "=", False))

        if not domain:
            return {"count": 0, "rows": []}

        partners = self.env["res.partner"].search(domain)

        response = {
            "count": len(partners),
            "rows": [self._to_dict(p) for p in partners],
        }
        return response

    def validate(self, _id, **params):
        partner = self.env["res.partner"].search(
            [("_api_external_id", "=", _id)]
        )
        if not partner:
            raise wrapJsonException(
                NotFound(_("No partner for id %s") % _id)
            )
        partner.validate_res_partner()
        return self._to_dict(partner)

    def _to_dict(self, record):
        record.ensure_one()
        utils = api_services_utils.get_instance()
        address_attributes = {
            "street",
            "zip",
            "city",
            "state_id",
            "country_id"
        }
        rel_address_attributes = {
            "state_id": "code",
            "country_id": "code"
        }
        address_dict = utils.generate_get_dictionary(
            record, address_attributes, rel_address_attributes)
        attributes = {
            "name",
            "email",
            "lang"
        }
        record_dict = utils.generate_get_dictionary(record, attributes)
        record_dict['address'] = address_dict
        return record_dict

    def _validator_get(self):
        return schemas.S_RES_PARTNER_GET

    def _validator_return_get(self):
        return schemas.S_RES_PARTNER_RETURN_GET

    def _validator_validate(self):
        return schemas.S_RES_PARTNER_VALIDATE

    def _validator_return_validate(self):
        return schemas.S_RES_PARTNER_RETURN_GET

    def _validator_search(self):
        return schemas.S_RES_PARTNER_SEARCH

    def _validator_return_search(self):
        return schemas.S_RES_PARTNER_RETURN_SEARCH
