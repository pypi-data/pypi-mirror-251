from odoo import models, fields, api

class AssetAsset(models.Model):
    _inherit = 'account.asset'

    current_depreciated_amount = fields.Float(compute='_compute_current_depreciated_amount', string='Amortizació actual', store=False)
    current_depreciated_amount_to_show = fields.Float(compute='_compute_current_depreciated_amount_to_show', string='Amortizació actual', store=True)

    @api.depends('current_depreciated_amount')
    def _compute_current_depreciated_amount_to_show(self):
        for asset in self:
            asset.current_depreciated_amount_to_show = asset.current_depreciated_amount
    
    @api.depends('depreciation_line_ids.amount', 'depreciation_line_ids.line_date')
    def _compute_current_depreciated_amount(self):
        """
        It will retrieve the closest of the asset line entries from today up to the future.
        The value returned will be the amount field of that line.
        """
        for asset in self:
            if asset.depreciation_line_ids:
                following_asset_line = asset.depreciation_line_ids.search(          # Get the first line starting from today ordered based on line_date
                    [
                        ('asset_id', '=', asset.id),                                # Very important part of the domain since search() will look among all the records, not only depreciation_line_ids
                        ('line_date', '>=', fields.Date.today())
                    ],
                    order='line_date asc',
                    limit=1
                )
                if following_asset_line:
                    asset.current_depreciated_amount = following_asset_line.amount
                else:
                    asset.current_depreciated_amount = 0.0
            else:
                asset.current_depreciated_amount = 0.0
