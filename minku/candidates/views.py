from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import UploadFileForm, CommentForm
from bs4 import BeautifulSoup  # 导入网页解析库

from .models import Candidate, EduRecords, CompanyRecords, ProjectRecords, Comments


def get_candidate_info_by_id(candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    edu_record_list = EduRecords.objects.all().filter(candidate=candidate_id)
    company_records_list = CompanyRecords.objects.all().filter(candidate=candidate_id)
    project_records_list = ProjectRecords.objects.all().filter(candidate=candidate_id)
    comments_list = Comments.objects.all().order_by('-id').filter(candidate=candidate_id)
    return candidate, edu_record_list, company_records_list, project_records_list, comments_list


@login_required
def add_candidate_comment(request, candidate_id):
    candidate, edu_record_list, company_records_list, project_records_list, comments_list = get_candidate_info_by_id(candidate_id)
    # page_obj = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form)
            print(request.user.username)
            try:
                comment = Comments.objects.create(
                    comment_content=form.cleaned_data['comment_content'],
                    creator=request.user.username,
                    candidate=candidate,
                )
            except Exception as e:
                print(e)
    form = CommentForm()
    return render(request, 'candidates/candidate_detail.html', {'candidate': candidate,
                                                                'edu_record_list': edu_record_list,
                                                                'company_records_list': company_records_list,
                                                                'project_records_list': project_records_list,
                                                                'comments_list': comments_list,
                                                                'form': form,
                                                                'system_user': request.user.username})


def candidate_detail(request, candidate_id):
    form = CommentForm()
    candidate, edu_record_list, company_records_list, project_records_list, comments_list = get_candidate_info_by_id(candidate_id)
    return render(request, 'candidates/candidate_detail.html', {'candidate': candidate,
                                                                'edu_record_list': edu_record_list,
                                                                'company_records_list': company_records_list,
                                                                'project_records_list': project_records_list,
                                                                'comments_list': comments_list,
                                                                'form': form,
                                                                'system_user': request.user.username})


def get_cv_info_dict(request, cv_contents):
    soup = BeautifulSoup(cv_contents, 'lxml')

    # 替换<br> 保留换行
    for elem in soup.find_all("br"):
        elem.replace_with(elem.text + "\n")

    # 基本信息
    basic_username = soup.find(class_="name ellipsis").text if soup.find(class_="name ellipsis") else ""  # 王先生
    basic_user_status = soup.find(class_="user-status-tag").text if soup.find(class_="user-status-tag") else ""  # 方便联系时间：随时联系
    work_position = soup.select('.basic-cont .sep-info')[1].contents[0].string if soup.select('.basic-cont .sep-info')[1].contents[0] else ""
    work_company = soup.select('.basic-cont .sep-info')[1].contents[2].string if soup.select('.basic-cont .sep-info')[1].contents[2] else ""  # 王先生
    self_judgement = soup.select('.resume-detail-self-evaluation-info .resume-detail-template-cont')[0].text if soup.select('.resume-detail-self-evaluation-info .resume-detail-template-cont') else ""
    additional_comments = soup.select('.resume-detail-addition-info .resume-detail-template-cont')[0].text if soup.select('.resume-detail-addition-info .resume-detail-template-cont') else ""

    basic_gender = ''
    basic_age = ''
    basic_edu_degree = ''
    basic_work_years = ''
    person_info_section = soup.select('.basic-cont .sep-info')[0].contents  # 男39岁北京硕士16年工作经验
    work_city = person_info_section[4] if person_info_section[4] else ""
    for info in person_info_section:
        content = info.string
        if content:
            if content in ('男', '女'):
                basic_gender = content  # 男
            elif '岁' in content:
                basic_age = int(content.split('岁')[0])  # 39岁
                basic_born_year = datetime.now().year - basic_age
            # elif content in ('硕士', '本科', '博士', '专科', 'MBA/EMBA'):
            elif content in '硕士本科博士专科MBA/EMBA':
                basic_edu_degree = content  # 硕士
            elif '年' in content:
                basic_work_years = int(content.replace("工作","").split('年')[0])  # 16年工作经验
                basic_work_start_year = datetime.now().year - basic_work_years

    # 工作期望
    work_salary = ''
    work_industry = ''
    expect_position = ''
    expect_salary = ''
    expect_city = ''
    expect_industry = ''
    expect_info_section = soup.select('.resume-detail-template.resume-detail-job-expectancy-info .rd-info-col')
    for info in expect_info_section:
        info_title = info.select('.rd-info-col-title')[0].text.strip()
        if info_title:
            if '目前薪资' in info_title:
                work_salary = info.select('.rd-info-col-cont')[0].text.strip()
            if '目前行业' in info_title:
                work_industry = info.select('.rd-info-col-cont')[0].text.strip()
            if '期望职位' in info_title:
                expect_position = info.select('.rd-info-col-cont .job-name')[0].text.strip()
                expect_salary = info.select('.rd-info-col-cont .salary')[0].text.strip()
                expect_city = info.select('.rd-info-col-cont .address')[0].text.strip()
                expect_industry = info.select('.rd-info-col-cont .industry')[0].text.strip()

    # 工作经验
    company_records_dict = {}
    if soup.select('.resume-detail-template.resume-detail-work-info .rd-work-item-cont'):
        company_records_info_section = soup.select('.resume-detail-template.resume-detail-work-info .rd-work-item-cont')
        for info in company_records_info_section:
            work_company = info.select('.rd-work-comp')[0].text.strip() if info.select('.rd-work-comp')[0] else ""
            work_period = info.select('.rd-work-time ')[0].text.strip() if info.select('.rd-work-time ')[0] else ""
            work_start_date = work_period.split('-')[0][1:].strip() if work_period else ""
            work_end_date = work_period.split('-')[1].split(",")[0].strip() if work_period.split('-')[1] else ""
            work_company_type = info.select('.tags-box')[0].i.text.strip() if info.select('.tags-box')[0] else ""
            work_position = info.select('.job-name')[0].text.strip() if info.select('.job-name')[0] else ""

            work_department = ''
            work_subordinate = ''
            work_report_to = ''
            work_achievements = ''
            position_detail_info_section = info.select('.rd-info-row .rd-info-col')
            for position_detail in position_detail_info_section:
                position_detail_title = position_detail.select('.rd-info-col-title')[0].text.strip()
                if '所在部门' in position_detail_title:
                    work_department = position_detail.select('.rd-info-col-cont')[0].text.strip()
                if '下属人数' in position_detail_title:
                    work_subordinate = position_detail.select('.rd-info-col-cont')[0].text.strip()
                if '汇报对象' in position_detail_title:
                    work_report_to = position_detail.select('.rd-info-col-cont')[0].text.strip()
                if '职责业绩' in position_detail_title:
                    work_achievements = position_detail.select('.rd-info-col-cont')[0].text.strip()

            company_work_detail_dict = {'work_company': work_company,  # 华夏幸福
                                        'work_start_date': work_start_date,  # 2017.10
                                        'work_end_date': work_end_date,  # 至今
                                        'work_company_type': work_company_type,  # 私营·民营企业
                                        'work_position': work_position,  # 集团研发中心副主任（高级总监）
                                        'work_department': work_department,  # 集团设计管理中心
                                        'work_subordinate': work_subordinate,  # 40
                                        'work_report_to': work_report_to,  # 集团副总裁
                                        'work_achievements': work_achievements,
                                        # 负责项目方案设计、扩初及施工图审查、实施效果落地工作，并且负责编制集团设计标准化文件等
                                        }
            company_records_dict[work_company] = company_work_detail_dict

    # 项目经历
    project_records_dict = {}
    if soup.select('.resume-detail-template.resume-detail-project-info .rd-info-tpl-item.rd-project-item-cont'):
        project_records_info_section = soup.select('.resume-detail-template.resume-detail-project-info .rd-info-tpl-item.rd-project-item-cont')
        for info in project_records_info_section:
            project = info.select('.rd-project-name')[0].text.strip() if info.select('.rd-project-name')[0] else ''
            project_period = info.select('.rd-project-time ')[0].text.strip() if info.select('.rd-project-time ')[0] else ''
            project_start_date = project_period.split('-')[0][1:].strip() if project_period else ''
            project_end_date = project_period.split('-')[1].split(",")[0].strip() if project_period.split('-')[1] else ''

            project_company = ''
            project_position = ''
            project_description = ''
            project_responsibility = ''
            project_achievements = ''
            project_detail_section = info.select('.rd-info-row .rd-info-col')
            for project_detail in project_detail_section:
                project_detail_title = project_detail.select('.rd-info-col-title')[0].text.strip()
                if '所在公司' in project_detail_title:
                    project_company = project_detail.select('.rd-info-col-cont')[0].text.strip()
                if '项目职务' in project_detail_title:
                    project_position = project_detail.select('.rd-info-col-cont')[0].text.strip()
                if '项目描述' in project_detail_title:
                    project_description = project_detail.select('.rd-info-col-cont')[0].text.strip()
                if '项目职责：' in project_detail_title:
                    project_responsibility = project_detail.select('.rd-info-col-cont')[0].text.strip()
                if '项目业绩：' in project_detail_title:
                    project_achievements = project_detail.select('.rd-info-col-cont')[0].text.strip()
                    # print(project_achievements)

            project_detail_dict = {'project': project,  # 各类行业标杆产业园区、产业新城公建、公园、大型购物中心、医院、酒店、会展、教育配套等
                                   'project_start_date': project_start_date,  # 2017.10
                                   'project_end_date': project_end_date,  # 至今
                                   'project_company': project_company,
                                   'project_position': project_position,  # 运营管理
                                   'project_description': project_description,  # 负责长三角区域的产业新城、小镇的公建设施，如医院、酒店、会展、教育、产业园等项目设计
                                   'project_responsibility': project_responsibility,
                                   # 负责长三角区域事业部项目从产品立项到最后实施落地全过程设计管理，包含建筑单体、立面深化设计、室内设计、景观设计及泛光照明等设计资源管理。
                                   'project_achievements': project_achievements,  # 负责的项目设计品质较高，业界知名度及口碑较好
                                   # 负责项目方案设计、扩初及施工图审查、实施效果落地工作，并且负责编制集团设计标准化文件等
                                   }
            project_records_dict[project] = project_detail_dict

    # 教育经历
    basic_is_unified = False
    basic_is_985 = False
    basic_is_211 = False
    edu_records_dict = {}
    edu_records_info_section = soup.select(
        '.resume-detail-template.resume-detail-edu-info .rd-edu-info-item')
    for info in edu_records_info_section:
        edu_school = info.select('.school-name')[0].text.strip() if info.select('.school-name')[0] else ""
        edu_major = info.select('.school-special')[0].text.strip() if info.select('.school-special')[0] else ""
        edu_degree = info.select('.school-degree')[0].text.strip() if info.select('.school-degree')[0] else ""
        edu_period = info.select('.school-time')[0].text.strip() if info.select('.school-time')[0] else ""
        edu_start_date = edu_period.split('-')[0].strip() if edu_period else ""
        edu_end_date = edu_period.split('-')[1].strip() if edu_period.split('-')[1] else ""
        # edu_degree_value = info.select('.edu-school-tags')[0].text.strip() if info.select('.edu-school-tags')[0] else ""

        edu_degree_value = ''
        if info.select('.edu-school-tags')[0]:
            for degree in info.select('.edu-school-tags')[0]:
                if "统招" in degree: basic_is_unified = True
                if "985" in degree: basic_is_985 = True
                if "211" in degree: basic_is_211 = True
                edu_degree_value = edu_degree_value + degree.text.strip() + " "

        edu_detail_dict = {'edu_school': edu_school,  # 清华大学
                           'edu_major': edu_major,  # 创新项目管理（澳大利亚国立大学）
                           'edu_degree': edu_degree,  # 硕士
                           'edu_start_date': edu_start_date,  # 2015.07
                           'edu_end_date': edu_end_date,  # 2017.06
                           'edu_degree_value': edu_degree_value,  # 985211
                           }
        edu_records_dict[edu_school] = edu_detail_dict

    info_dict = {'basic_username': basic_username,
                 'basic_user_status': basic_user_status,
                 'basic_gender': basic_gender,
                 'basic_age': basic_age,
                 'basic_born_year': basic_born_year,
                 'basic_edu_degree': basic_edu_degree,
                 'basic_work_years': basic_work_years,
                 'basic_work_start_year': basic_work_start_year,
                 'basic_is_unified': basic_is_unified,
                 'basic_is_985': basic_is_985,
                 'basic_is_211': basic_is_211,
                 'work_position': work_position,
                 'work_city': work_city,
                 'work_company': work_company,
                 'work_salary': work_salary,
                 'work_industry': work_industry,
                 'expect_position': expect_position,
                 'expect_salary': expect_salary,
                 'expect_city': expect_city,
                 'expect_industry': expect_industry,
                 'company_records_dict': company_records_dict,
                 'project_records_dict': project_records_dict,
                 'edu_records_dict': edu_records_dict,
                 'self_judgement': self_judgement,
                 'additional_comments': additional_comments,
                 }

    # 插入数据
    try:
        candidate = Candidate.objects.create(
            basic_username=basic_username,
            basic_user_status=basic_user_status,
            basic_gender=basic_gender,
            basic_age=basic_age,
            basic_born_year=int(basic_born_year),
            basic_edu_degree=basic_edu_degree,
            basic_work_years=basic_work_years,
            basic_work_start_year=basic_work_start_year,
            basic_is_unified=basic_is_unified,
            basic_is_985=basic_is_unified,
            basic_is_211=basic_is_unified,

            work_position=work_position,
            work_city=work_city,
            work_company=work_company,
            work_salary=work_salary,
            work_industry=work_industry,

            expect_position=expect_position,
            expect_salary=expect_salary,
            expect_city=expect_city,
            expect_industry=expect_industry,

            self_judgement=self_judgement,
            additional_comments=additional_comments,

            creator=request.user.username,
        )

        for company_name, company_record in company_records_dict.items():
            company_record = CompanyRecords.objects.create(
                work_company=company_record['work_company'],
                work_start_date=company_record['work_start_date'],
                work_end_date=company_record['work_end_date'],
                work_company_type=company_record['work_company_type'],
                work_department=company_record['work_department'],
                work_subordinate=company_record['work_subordinate'],
                work_position=company_record['work_position'],
                work_report_to=company_record['work_report_to'],
                work_achievements=company_record['work_achievements'],
                creator=request.user.username,
                candidate=candidate,
            )

        for project_name, project_record in project_records_dict.items():
            project_records = ProjectRecords.objects.create(
                project=project_record['project'],
                project_start_date=project_record['project_start_date'],
                project_end_date=project_record['project_end_date'],
                project_company=project_record['project_company'],
                project_position=project_record['project_position'],
                project_description=project_record['project_description'],
                project_responsibility=project_record['project_responsibility'],
                project_achievements=project_record['project_achievements'],
                creator=request.user.username,
                candidate=candidate,
            )

        for edu_name, edu_record in edu_records_dict.items():
            edu_record = EduRecords.objects.create(
                edu_degree=edu_record['edu_degree'],
                edu_school=edu_record['edu_school'],
                edu_major=edu_record['edu_major'],
                edu_start_date=edu_record['edu_start_date'],
                edu_end_date=edu_record['edu_end_date'],
                edu_degree_value=edu_record['edu_degree_value'],
                creator=request.user.username,
                candidate=candidate,
            )

    except Exception as e:
        print(e)

    return info_dict, candidate.id


def candidates_index(request):
    form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'candidates/index.html', {'form': form, })


def handle_uploaded_file(request, file):
    candidate_info = file.read()
    info, candidate_id = get_cv_info_dict(request, candidate_info)
    return info, candidate_id


def candidate_file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            page_obj, candidate_id = handle_uploaded_file(request, request.FILES['file'])
            # return render(request, 'candidates/index.html', {'page_obj': page_obj, 'form': form, })
            comment_form = CommentForm()
            candidate, edu_record_list, company_records_list, project_records_list, comments_list = get_candidate_info_by_id(candidate_id)
            return render(request, 'candidates/candidate_detail.html', {'candidate': candidate,
                                                                        'edu_record_list': edu_record_list,
                                                                        'company_records_list': company_records_list,
                                                                        'project_records_list': project_records_list,
                                                                        'comments_list': comments_list,
                                                                        'comment_form': comment_form,
                                                                        'system_user': request.user.username})
    else:
        form = UploadFileForm()
    return render(request, 'candidates/index.html', {'form': form})
