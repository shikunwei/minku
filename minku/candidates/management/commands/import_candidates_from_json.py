from datetime import datetime
from django.core.management import BaseCommand
from candidates.models import Candidate, EduRecords, CompanyRecords, Comments, ProjectRecords
import json
import os

# run command to import candidates:
# python manage.py import_candidates_from_json.py --path C:\Users\joe\Desktop\talent_DB\cv


def get_value_from_dict(source_dict, item, default_value=''):
    if item in source_dict.keys():
        return source_dict[item]
    else:
        return default_value


def create_candidate_from_json(cdi_info_json):
    cdi_dict = json.loads(cdi_info_json)

    # basic_info
    basic_username = get_value_from_dict(cdi_dict['basic_info'], 'basic_username', '姓名缺失')
    basic_user_status = get_value_from_dict(cdi_dict['basic_info'], 'basic_user_status')
    basic_gender = get_value_from_dict(cdi_dict['basic_info'], 'basic_gender')
    basic_age = get_value_from_dict(cdi_dict['basic_info'], 'basic_age')
    basic_born_year = get_value_from_dict(cdi_dict['basic_info'], 'basic_born_year')
    basic_residence_city = get_value_from_dict(cdi_dict['basic_info'], 'basic_residence_city')
    basic_phone = get_value_from_dict(cdi_dict['basic_info'], 'basic_phone')
    basic_email = get_value_from_dict(cdi_dict['basic_info'], 'basic_email')
    basic_marriage_status = get_value_from_dict(cdi_dict['basic_info'], 'basic_marriage_status')
    basic_work_start_year = get_value_from_dict(cdi_dict['basic_info'], 'basic_work_start_year')
    basic_work_years = get_value_from_dict(cdi_dict['basic_info'], 'basic_work_years')
    basic_edu_degree = get_value_from_dict(cdi_dict['basic_info'], 'basic_edu_degree')
    basic_is_unified = get_value_from_dict(cdi_dict['basic_info'], 'basic_is_unified', False)
    basic_is_985 = get_value_from_dict(cdi_dict['basic_info'], 'basic_is_985', False)
    basic_is_211 = get_value_from_dict(cdi_dict['basic_info'], 'basic_is_211', False)
    work_industry = get_value_from_dict(cdi_dict['basic_info'], 'work_industry')
    work_city = get_value_from_dict(cdi_dict['basic_info'], 'work_city')
    work_company = get_value_from_dict(cdi_dict['basic_info'], 'work_company')
    work_position = get_value_from_dict(cdi_dict['basic_info'], 'work_position')
    work_salary = get_value_from_dict(cdi_dict['basic_info'], 'work_salary')
    work_salary_structure = get_value_from_dict(cdi_dict['basic_info'], 'work_salary_structure')
    work_intention = get_value_from_dict(cdi_dict['basic_info'], 'work_intention')
    expect_industry = get_value_from_dict(cdi_dict['basic_info'], 'expect_industry')
    expect_city = get_value_from_dict(cdi_dict['basic_info'], 'expect_city')
    expect_position = get_value_from_dict(cdi_dict['basic_info'], 'expect_position')
    expect_salary = get_value_from_dict(cdi_dict['basic_info'], 'expect_salary')
    self_judgement = get_value_from_dict(cdi_dict['basic_info'], 'self_judgement')
    additional_comments = get_value_from_dict(cdi_dict['basic_info'], 'additional_comments')

    # 录入者信息
    creator = '批量导入'

    if basic_phone:
        # 插入数据
        try:
            candidate = Candidate.objects.create(
                basic_username=basic_username,
                basic_user_status=basic_user_status,
                basic_gender=basic_gender,
                basic_age=basic_age,
                basic_born_year=basic_born_year,
                basic_residence_city=basic_residence_city,
                basic_phone=basic_phone,
                basic_email=basic_email,
                basic_marriage_status=basic_marriage_status,
                basic_work_start_year=basic_work_start_year,
                basic_work_years=basic_work_years,
                basic_edu_degree=basic_edu_degree,
                basic_is_unified=basic_is_unified,
                basic_is_985=basic_is_985,
                basic_is_211=basic_is_211,
                work_industry=work_industry,
                work_city=work_city,
                work_company=work_company,
                work_position=work_position,
                work_salary=work_salary,
                work_salary_structure=work_salary_structure,
                work_intention=work_intention,
                expect_industry=expect_industry,
                expect_city=expect_city,
                expect_position=expect_position,
                expect_salary=expect_salary,
                self_judgement=self_judgement,
                additional_comments=additional_comments,
            )

            print(candidate, " <<< candidate.id >>> ", candidate.id, " <<< candidate.age >>> ", candidate.get_age())

            if "edu_record" in cdi_dict.keys():
                for record_value in cdi_dict["edu_record"].values():
                    edu_degree = get_value_from_dict(record_value, 'edu_degree')
                    edu_school = get_value_from_dict(record_value, 'edu_school')
                    edu_major = get_value_from_dict(record_value, 'edu_major')
                    edu_start_date = get_value_from_dict(record_value, 'start_date')
                    edu_end_date = get_value_from_dict(record_value, 'end_date')
                    edu_record = EduRecords.objects.create(
                        edu_degree=edu_degree,
                        edu_school=edu_school,
                        edu_major=edu_major,
                        edu_start_date=edu_start_date,
                        edu_end_date=edu_end_date,
                        candidate=candidate,
                        edu_creator=creator,
                    )

            if "company_record" in cdi_dict.keys():
                for record_value in cdi_dict["company_record"].values():
                    work_company = get_value_from_dict(record_value, 'work_company')
                    work_position = get_value_from_dict(record_value, 'work_position')
                    work_achievements = get_value_from_dict(record_value, 'work_achievements')
                    work_start_date = get_value_from_dict(record_value, 'start_date')
                    work_end_date = get_value_from_dict(record_value, 'end_date')
                    company_record = CompanyRecords.objects.create(
                        work_company=work_company,
                        work_position=work_position,
                        work_achievements=work_achievements,
                        work_start_date=work_start_date,
                        work_end_date=work_end_date,
                        candidate=candidate,
                        work_creator=creator,
                    )

            if "project_record" in cdi_dict.keys():
                for record_value in cdi_dict["project_record"].values():
                    project = get_value_from_dict(record_value, 'project')
                    project_description = get_value_from_dict(record_value, 'project_description')
                    project_start_date = get_value_from_dict(record_value, 'start_date')
                    project_end_date = get_value_from_dict(record_value, 'end_date')
                    project_record = ProjectRecords.objects.create(
                        project=project,
                        project_description=project_description,
                        project_start_date=project_start_date,
                        project_end_date=project_end_date,
                        candidate=candidate,
                        project_creator=creator,
                    )

        except Exception as e:
            print(e)


class Command(BaseCommand):
    help = '从一个Json文件的内容中读取候选人信息，导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        json_dir = kwargs['path']
        json_file_list = os.listdir(json_dir)  # 列出文件夹下所有的目录与文件
        # for i in range(0, len(json_file_list)):
        for i in range(0, len(json_file_list)):
            if json_file_list[i][-4:] == 'json':
                # resume json 文件的完整路径加文件名
                source_json_file = os.path.join(json_dir, json_file_list[i])
                if os.path.isfile(source_json_file):
                    # # 你想对文件的操作
                    print(i, ": proceeding with", source_json_file)
                    try:
                        with open(source_json_file, encoding='utf-8') as f:
                            cdi_info_json = f.read()
                            # print(cdi_info_json)
                            create_candidate_from_json(cdi_info_json)
                    except Exception as e:
                        print(e)
