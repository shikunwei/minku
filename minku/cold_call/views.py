import csv
import codecs
from django.shortcuts import render

from .forms import UploadFileForm
from .models import ColdCall


def cold_call_index(request):
    form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'cold_call/index.html', {'form': form, })


def handle_uploaded_file(file):
    print("aaaaaaaaaaaaaaaaaaaaaaa")
    info_dict = {}
    info_dict["info_dict_title"] = []
    info_dict["info_dict_title"].append("公司")

    file_name = str(file).rstrip(".csv").split("-")
    company_name = file_name[0]
    if len(file_name) > 1:
        district_name = file_name[1]
        info_dict["info_dict_title"].append("城市区域")
    else:
        district_name = ""
    print("bbbbbbbbbbbbbbbbbbbbbb")

    reader = csv.DictReader(codecs.iterdecode(file, 'gb18030'))
    for call_infos in reader:
        basic_username = call_infos['姓名'] if "姓名" in call_infos else ""
        basic_gender = call_infos['性别'] if "性别" in call_infos else ""
        basic_phone = call_infos['电话'] if "电话" in call_infos else ""
        basic_email = call_infos['邮箱'] if "邮箱" in call_infos else ""
        basic_edu_school = call_infos['毕业院校'] if "毕业院校" in call_infos else ""
        work_depart = call_infos['部门'] if "部门" in call_infos else ""
        work_position = call_infos['职位'] if "职位" in call_infos else ""
        additional_comments = call_infos['备注'] if "备注" in call_infos else ""

        info_dict[call_infos["姓名"]] = {}
        info_dict[call_infos["姓名"]]["公司"] = company_name
        info_dict[call_infos["姓名"]]["城市区域"] = district_name

        print("ccccccccccccccccccccccccc")
        if district_name:
            info_dict[call_infos["姓名"]]["城市区域"] = district_name

        for call_info_key, call_info_val in call_infos.items():
            if call_info_val:
                if call_info_key not in info_dict["info_dict_title"]:
                    info_dict["info_dict_title"].append(call_info_key)
                info_dict[call_infos["姓名"]][call_info_key] = call_info_val

        try:
            cold_call = ColdCall.objects.create(
                basic_username=basic_username,
                basic_gender=basic_gender,
                basic_region=district_name,
                basic_phone=basic_phone,
                basic_email=basic_email,
                basic_edu_school=basic_edu_school,
                work_company=company_name,
                work_depart=work_depart,
                work_position=work_position,
                additional_comments=additional_comments,
            )
            print(cold_call)
        except Exception as e:
            print(e)

    print(info_dict)
    return info_dict


def cold_call_file_upload(request):
    page_obj = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            page_obj = handle_uploaded_file(request.FILES['file'])
            return render(request, 'cold_call/index.html', {'page_obj': page_obj, 'form': form, })
    else:
        form = UploadFileForm()
    return render(request, 'cold_call/index.html', {'form': form})
