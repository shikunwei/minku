default_fieldsets = (
    ("基本信息", {'fields': (
        ("basic_username", "basic_gender", "basic_born_year", "basic_marriage_status"), ("basic_phone", "basic_email", "basic_residence_city"))}),
    ("学历信息", {'fields': (("basic_edu_degree", "basic_is_unified", "basic_is_985", "basic_is_211"),)}),
    ("工作信息", {'fields': (
        ("work_company", "work_position", "basic_work_years",  "work_intention"),
        ("work_city", "work_salary", "work_industry"))}),
    ("期望工作", {'fields': (
        ("expect_city", "expect_salary", "expect_industry"),
        ("expect_position",))}),
    ("自我评价", {'fields': ("self_judgement",)}),
    ("附加消息", {'fields': ("additional_comments",)}),
)
