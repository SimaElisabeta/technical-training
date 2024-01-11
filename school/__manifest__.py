{
    "name": "Schools",  # The name that will appear in the App list
    "version": "16.0",  # Version
    # "category": "Real Estate/Brokerage", # Category for security
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/ir.model.access.csv",

        "views/school_views.xml",
        "views/school_res_partner_views.xml",
        "views/school_class_location_views.xml",
        "views/school_class_views.xml",
        "views/school_schedule_views.xml",
        "views/school_courses_views.xml",
        "views/school_courses_teachers_views.xml",
        "views/school_attendance_views.xml",
        "views/school_catalog_views.xml",
        "views/school_menus.xml",
    ],
    "demo": [
       
    ],
    "installable": True,
    'license': 'LGPL-3',
}
