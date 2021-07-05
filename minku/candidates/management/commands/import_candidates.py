from datetime import datetime
from django.core.management import BaseCommand
from candidates.models import Candidate, EduRecords, CompanyRecords, Comments, ProjectRecords
import json
import os

# run command to import candidates:
# python manage.py import_candidates --path C:\Users\joe\Desktop\talent_DB\cv


def create_candidate_from_json(cdi_info_json):
    cdi_dict = json.loads(cdi_info_json)

    # 基本信息
    basic_username = cdi_dict['基本信息']['姓名'] if '姓名' in cdi_dict['基本信息'] else ""
    basic_gender = cdi_dict['基本信息']['性别'] if '性别' in cdi_dict['基本信息'] else ""
    basic_born_year = cdi_dict['基本信息']['出生年份'] if '出生年份' in cdi_dict['基本信息'] else datetime.now().year
    basic_residence_city = cdi_dict['基本信息']['户口'] if '户口' in cdi_dict['基本信息'] else ""
    basic_phone = cdi_dict['基本信息']['手机'] if '手机' in cdi_dict['基本信息'] else ""
    basic_email = cdi_dict['基本信息']['Email'] if 'Email' in cdi_dict['基本信息'] else ""
    basic_marriage_status = cdi_dict['基本信息']['婚姻状况'] if '婚姻状况' in cdi_dict['基本信息'] else ""
    basic_is_unified = True if '统招' in cdi_dict['基本信息']['学历优势'] else False
    basic_is_985 = True if '985' in cdi_dict['基本信息']['学历优势'] else False
    basic_is_211 = True if '211' in cdi_dict['基本信息']['学历优势'] else False

    # 学校与学历信息
    basic_edu_degree = cdi_dict['基本信息']['学历'] if '学历' in cdi_dict['基本信息'] else ""

    # 工作信息
    work_industry = cdi_dict['基本信息']['行业'] if '行业' in cdi_dict['基本信息'] else ""
    basic_work_years = cdi_dict['基本信息']['工作年限'].split('年')[0] if '工作年限' in cdi_dict['基本信息'] else ""

    work_salary = cdi_dict['基本信息']['年薪'].split('万')[0] if '年薪' in cdi_dict['基本信息'] and cdi_dict['基本信息']['年薪'] != '0万' else "保密"
    work_city = cdi_dict['基本信息']['现工作地'] if '现工作地' in cdi_dict['基本信息'] else ""
    work_company = cdi_dict['基本信息']['公司名称'] if '公司名称' in cdi_dict['基本信息'] else ""
    work_position = cdi_dict['基本信息']['职位名称'] if '职位名称' in cdi_dict['基本信息'] else ""

    # 项目经验信息
    project_exp = cdi_dict['项目经验']['详细描述'].replace(' r n', '\n') if '详细描述' in cdi_dict['项目经验'] else ""

    # 教育经历
    degree = []
    school = []
    major = []
    school_start_date = []
    school_end_date = []
    for i in range(0, 5):
        index = str(i) if i != 0 else ''

        if '学位' + index in cdi_dict['教育经历']:
            degree.append(cdi_dict['教育经历']['学位' + index])
        if '学校名称' + index in cdi_dict['教育经历']:
            school.append(cdi_dict['教育经历']['学校名称' + index])
        if '专业' + index in cdi_dict['教育经历']:
            major.append(cdi_dict['教育经历']['专业' + index])
        if '时间' + index in cdi_dict['教育经历']:
            school_start_date.append(cdi_dict['教育经历']['时间' + index].split(" - ")[0])
        if '时间' + index in cdi_dict['教育经历']:
            school_end_date.append(cdi_dict['教育经历']['时间' + index].split(" - ")[1])

    # 工作经历
    company = []
    company_position = []
    achievements = []
    company_start_date = []
    company_end_date = []
    for i in range(0, 10):
        index = str(i) if i != 0 else ''

        if '公司名称' + index in cdi_dict['工作经历']:
            company.append(cdi_dict['工作经历']['公司名称' + index])
        if '职位' + index in cdi_dict['工作经历']:
            company_position.append(cdi_dict['工作经历']['职位' + index])
        if '工作描述' + index in cdi_dict['工作经历']:
            achievements.append(cdi_dict['工作经历']['工作描述' + index].replace(' r n', '\n'))
        if '时间' + index in cdi_dict['工作经历']:
            company_start_date.append(cdi_dict['工作经历']['时间' + index].split(" - ")[0])
        if '时间' + index in cdi_dict['工作经历']:
            company_end_date.append(cdi_dict['工作经历']['时间' + index].split(" - ")[1])

    # 评论
    comments = cdi_dict['联系记录']

    # 录入者信息
    creator = '批量导入'

    # 插入数据
    try:
        candidate = Candidate.objects.create(
            basic_username=basic_username,
            basic_gender=basic_gender,
            basic_born_year=int(basic_born_year),
            basic_residence_city=basic_residence_city,
            basic_marriage_status=basic_marriage_status,
            basic_is_unified=basic_is_unified,
            basic_phone=basic_phone,
            basic_email=basic_email,
            basic_edu_degree=basic_edu_degree,
            work_industry=work_industry,
            basic_work_years=basic_work_years,
            basic_is_985=basic_is_985,
            basic_is_211=basic_is_211,
            work_salary=work_salary,
            work_city=work_city,
            work_company=work_company,
            work_position=work_position,
            creator=creator,
        )

        print(candidate, " <<< candidate.id >>> ", candidate.id, " <<< candidate.age >>> ", candidate.get_age())

        for i in range(0, len(school)):
            edu_record = EduRecords.objects.create(
                edu_degree=degree[i],
                edu_school=school[i],
                edu_major=major[i],
                edu_start_date=school_start_date[i],
                edu_end_date=school_end_date[i],
                candidate=candidate,
                creator=creator,
            )
            # print(edu_record, " <<< edu_record >>> ", degree[i], school[i], major[i], school_start_date[i],
            #       school_end_date[i], candidate.id)

        for i in range(0, len(company)):
            company_record = CompanyRecords.objects.create(
                work_company=company[i],
                work_position=company_position[i],
                work_achievements=achievements[i],
                work_start_date=company_start_date[i],
                work_end_date=company_end_date[i],
                candidate=candidate,
                creator=creator,
            )

        for key in comments:
            comment = Comments.objects.create(
                comment_content=comments[key].split(':', 1)[1],
                created_date=datetime.strptime(key, "%Y-%m-%d %H:%M:%S"),
                candidate=candidate,
                creator=creator,
            )

        project_records = ProjectRecords.objects.create(
            project_description=project_exp,
            candidate=candidate,
            creator=creator,
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
                source_json_file = os.path.join(json_dir, json_file_list[i])
                if os.path.isfile(source_json_file):
                    # # 你想对文件的操作
                    print(i, ": proceeding with", source_json_file)
                    try:
                        with open(source_json_file, encoding='utf-8') as f:
                            cdi_info_json = f.read()
                            create_candidate_from_json(cdi_info_json)
                    except Exception as e:
                        print(e)
