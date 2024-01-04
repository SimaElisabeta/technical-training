{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["estate", "account"],  # dependencies
    "data": [
        "report/estate_property_templates.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
