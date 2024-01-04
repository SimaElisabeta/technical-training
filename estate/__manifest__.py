{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0",  # Version
    "category": "Real Estate/Brokerage", # Category for security
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        # "data/estate.property.type.csv",
        # "data/estate.property.tag.csv",

        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
        "views/extend_users_views.xml",

        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
    ],
    "demo": [
        "data/estate_demo.xml",
        # "demo/demo_data.xml",
        # "demo/demo_data_offers.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
