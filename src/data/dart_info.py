
'''
@reference https://dart-fss.readthedocs.io/en/latest/
'''

import requests
from io import BytesIO
import zipfile
import xmltodict
import requests
import pandas as pd
import io
import zipfile
import xml.etree.ElementTree as et
import json
import dart_fss as df

'''
@Brief process except via inner exception class 
@TODO 사용자 정의 예외 클래스 추가 필요 (ex DB API)
'''
def process_exception_func(func):
    def wrapper(*args, **kargs):
        try:
            retval = func(*args, **kargs)
        except ZeroDivisionError as zd:
            print('[error] ZeroDivision value :{0}'.format(zd.value))
            return None
        except IndexError as ie:
            print('[error] IndexError value :{0}'.format(ie.value))
            return None
        except FileNotFoundError as ff:
            print('[error] FileNotFoundError value :{0}'.format(ff.value))
            return None
        except TypeError as te:
            print('[error] TypeError value :{0}'.format(te.value))
            return None
        except Exception as e:
            print ('{0}'.format(e))
            return None
        else:
            return retval

    return wrapper

def process_exception_class_func(func):
    def wrapper(self, *args, **kargs):
        try:
            retval = func(self, *args, **kargs)
        except ZeroDivisionError as zd:
            print('[error] ZeroDivision value :{0}'.format(zd.value))
            return None
        except IndexError as ie:
            print('[error] IndexError value :{0}'.format(ie.value))
            return None
        except FileNotFoundError as ff:
            print('[error] FileNotFoundError value :{0}'.format(ff.value))
            return None
        except TypeError as te:
            print('[error] TypeError value :{0}'.format(te.value))
            return None
        except Exception as e:
            print ('{0}'.format(e))
            return None
        else:
            return retval

    return wrapper


@process_exception_func
def get_crtfc_key(path):
    print("{0}".format(path))
    f = open(path, 'r')
    line = f.readline()
    print("{0}".format(line))
    return line

@process_exception_func
def get_corp_code_zip_file(crtfc_key):
    corp_code_url = 'https://opendart.fss.or.kr/api/corpCode.xml'
    res = requests.get(corp_code_url, params={'crtfc_key': crtfc_key})
    data_xml = zipfile.ZipFile(BytesIO(res.content))
    # 파일 경로 리턴
    return data_xml

@process_exception_func
def convert_xml_to_dict(z, xml_path):
    data_xml = z.read(xml_path).decode('utf-8')
    data_odict = xmltodict.parse(data_xml)
    data_dict = json.loads(json.dumps(data_odict))
    data = data_dict.get('result', {}).get('list')

class dart_stock_info():
    __crtfc_key = None

    def __init__(self, api_key):
        self.__crtfc_key = api_key
        df.set_api_key(api_key=api_key)
        self.__corp_list = df.get_corp_list()

    # 기업 리스트 리턴
    @process_exception_class_func
    def get_corp_list(self):
        return self.__corp_list

    # 회사 정보 리턴
    @process_exception_class_func
    def get_corp_basic_info(self, corp_code):
        basic_info = self.__corp_list.find_by_crp_cd(corp_code)
        return basic_info

    # 회사 이름으로 연결 재무제표 검색
    @process_exception_class_func
    def get_fs_by_corp_name(self, corp_name):
        corp_fs = self.__corp_list.find_by_corp_name(corp_name, exactly=True)[0]
        fs = corp_fs.extract_fs(bgn_de='20200101')
        return fs

    # 엑셀 파일로 지정된 경로에 저장
    @process_exception_class_func
    def save_fs(self, fs, filename, dir_path):
        fs.save(filename=filename, path=dir_path)


    @process_exception_class_func
    '''
    def get_financial_reports(self, corp_name, *during):
        corp_fs = self.__corp_list.find_by_corp_name(corp_name, exactly=True)
        for date in range(*during):
            financial_reports = basic_info.get_financial_statement(start_dt=date)
            return financial_reports['fs'[0]]
    '''
    def __del__(self):
        pass
