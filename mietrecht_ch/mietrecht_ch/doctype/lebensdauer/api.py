import frappe
from mietrecht_ch.models.calculatorMasterResult import CalculatorMasterResult
from mietrecht_ch.models.calculatorResult import CalculatorResult
from mietrecht_ch.models.lebensdauer import LebensdauerEntry, LebensdauerRemedy, LebensdauerResult

@frappe.whitelist(allow_guest=True)
def get_all_by_group(groupId):
    return CalculatorMasterResult( 
        {'groupId':groupId}, 
        [CalculatorResult(get_fake_data(), None)]
    )


@frappe.whitelist(allow_guest=True)
def get_all_by_keyword(keyword):
    return CalculatorMasterResult( 
        {'keyword':keyword}, 
        [CalculatorResult(get_fake_data(), None)]
    )


def get_fake_data():
    agregateChildren = [
        LebensdauerEntry('für Warmluftcheminée', lifetime=20),
        LebensdauerEntry('zur Wärmerückgewinnung', lifetime=20),
    ]

    chemineeChildren = [
        LebensdauerEntry('Cheminée, Cheminéeofen, Schwedenofen', lifetime=25),
        LebensdauerEntry('Schamottsteinauskleidung', lifetime=15, remedy=LebensdauerRemedy('Neuauskleidung', 'm²', 800))
    ]

    entries = [
        LebensdauerEntry('Aggregate', agregateChildren),
        LebensdauerEntry('Cheminéeabschluss', comment="Metallgitter, Glas"),
        LebensdauerEntry('Cheminées', chemineeChildren),
        LebensdauerEntry('Ventilator', comment='Zu Rauchabzug', lifetime=20),
    ]
    return LebensdauerResult('Cheminée', entries)