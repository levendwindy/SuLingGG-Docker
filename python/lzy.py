#!/usr/bin/python
#
# Copyright (c) 2023
#

import re
import datetime
import sys
import os
from lanzou.api import LanZouCloud


ylogin = sys.argv[1]
phpdisk_info = sys.argv[2]

# 新建的目录所在文件夹
LZ_folder_name = sys.argv[3]
# 移动当前目录所有的文件
MOVE_dir = sys.argv[4]
# GitHub 上传路径
Github_path = sys.argv[5]


cookie = {'ylogin': f'{ylogin}', 'phpdisk_info': f'{phpdisk_info}'}


# LZ_YLOGIN      LZ_PHPDISK
# 通过 id 获取文件夹的绝对路径


def exID(folder_name):
    ex = f"FolderId\(name='{folder_name}', id=(\d+)\)"
    return ex


def show_progress(file_name, total_size, now_size):
    """显示进度的回调函数"""
    percent = now_size / total_size
    bar_len = 40  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
    if total_size == now_size:
        print('')  # 下载完成换行


class lanzou(object):
    def __init__(self):
        self.lzy = LanZouCloud()
        res = self.lzy.login_by_cookie(cookie)
        self._now_size = 0
        self._total_size = 1
        self._uploaded_handler = None
        if res == 0:
            print(f'蓝奏云登录成功')
        else:
            print(f'蓝奏云登录 failed！\nERROR：  res= {res}')

    def __del__(self):
        pass
        # 注销
        # if self.lzy.logout() == 0:
        #    print(f'蓝奏云注销成功')

        # 获取网盘全部文件夹(用于移动文件)

    def get_FOLDERS(self):
        folders = self.lzy.get_move_folders()
        return folders

        # 获取文件夹ID(用于移动文件)

    def get_FOLDER_ID(self, folder_name):
        folders = self.lzy.get_move_folders()
        ex = exID(folder_name)
        folder_id = int(re.findall(ex, str(folders.find_by_name(folder_name)), re.S)[0])
        return folder_id

    # 获取某文件夹下的文件列表
    # .get_file_list(folder_id)
    def get_FILE_list(self, folder_name):
        folder_id = self.get_FOLDER_ID(folder_name)
        file_list = self.lzy.get_file_list(folder_id)
        if len(str(file_list)) <= 7:
            # print(f'文件夹 {folder_name} 没有文件')
            return False
        else:
            # print(f'file_list: {file_list} 长度: {len(str(file_list))}')
            file_id = int(re.findall('id=(\d+),', str(file_list), re.S)[0])
            # print(f'file_id: {file_id}')
            return file_id

    # 移动文件夹(id=1384074)到文件夹(id=879591)内
    #       lzy.move_file(12741016, 1037083)
    def MOVE_folder(self, folder_ID, parent_folder_id):
        try:
            res = self.lzy.move_folder(int(folder_ID), int(parent_folder_id))
        except TypeError:
            print(f'文件夹并未改变位置，移动失败\nparent_folder_id: {parent_folder_id}')
        except Exception as result:
            print("未知错误 %s" % result)
        else:
            if res == 0:
                print(f'已将文件夹 {folder_ID} 成功转义')
            elif res == -1:
                print(f'移动失败 文件夹 {folder_ID} 位于同级目录')
            else:
                print(f'移动失败 res： {res}')

    # 移动文件(id=12741016) 到文件夹(id=1037083)
    #    lzy.move_file(12741016, 1037083) == LanZouCloud.SUCCESS
    def MOVE_file(self, folder_id, parent_folder_id):
        res = self.lzy.move_file(int(folder_id), int(parent_folder_id))
        if res == 0:
            # print(f'已将文件 {int(folder_id)} 移动至 {int(parent_folder_id)}')
            print(f'文件 {int(folder_id)} 已成功转移')
        else:
            print(f'移动文件错误，res: {res}')

    def MKDIR_files_from_folder(self, folder_name, new_folder_name):
        while True:
            file_id = self.get_FILE_list(folder_name)
            if file_id == False:
                print(f'文件夹 {folder_name} 内的文件已转移完毕')
                break
            new_folder_id = self.get_FOLDER_ID(new_folder_name)
            print(f'文件夹名{folder_name} 文件id {file_id}  新文件夹名 {new_folder_name}  新文件id {new_folder_id}')
            self.MOVE_file(file_id, new_folder_id)

    # 创建文件夹并返回id
    #        lzy.mkdir(-1, 'my_music', '音乐分享')
    def MKDIR_folder(self, parent_id, folder_name, desc=''):
        fid = self.lzy.mkdir(parent_id, folder_name, desc)
        if fid == False:
            print('创建文件夹失败')
        else:
            return fid

    # 重命名文件夹
    #        lzy.rename_dir(1037070, 'soft_music')
    def RENAME_dir(self, folder_id, folder_name):
        if self.lzy.rename_dir(int(folder_id), folder_name) == 0:
            print(f'已将 {int(folder_id)} 重命名为 {folder_name}')

    # 修改文件(夹)描述信息                       是否为文件id，默认 is_file=True
    # lzy.set_desc(1083604, '批量上传的音乐', is_file=False)
    def SET_desc(self, fid, desc, is_file=False):
        if self.lzy.set_desc(int(fid), desc, is_file) == 0:
            print(f'修改文件(夹) {int(fid)} 描述信息为 {desc}')

    # 设置文件(夹)提取码 is_file	bool	是否为文件id	N	默认True
    # lzy.set_share_info(1033203必填, 'fuck')   密码(默认空)
    def SET_passwd(self, fid, passwd='', is_file=False):
        if self.lzy.set_passwd(int(fid), passwd, is_file) == 0:
            print(f'修改文件(夹) {int(fid)} 提取码为 {passwd}')

        """显示失败文件的回调函数"""

    def show_failed(self, code, filename):
        print(f"下载失败,错误码: {code}, 文件名: {filename}")

    def _after_uploaded(self, fid, is_file):
        """上传完成自动设置提取码, 如果有其它回调函数就调用"""
        if is_file:
            self.lzy.set_passwd(fid, '', is_file=True)
        else:
            self.lzy.set_passwd(fid, '', is_file=False)

        if self._uploaded_handler is not None:
            self._uploaded_handler(fid, is_file)

    def set_uploaded_handler(self, handler):
        """设置上传完成后的回调函数"""
        if handler is not None:
            self._uploaded_handler = self.handler

    def handler(self, fid, is_file, desc=''):
        if is_file:
            self.lzy.set_desc(fid, desc, is_file=True)
            self.lzy.set_passwd(fid, '', is_file=True)

    def UPLOAD_file(self, file_path, parent_name):
        folder_id = self.get_FOLDER_ID(parent_name)
        file_name = file_path.split("/")[-1]
        # code = self.lzy.upload_file(file_path, folder_id, callback=show_progress, uploaded_handler=self.handler)
        # show_progress  进度回调函数: 该函数用于跟踪上传进度
        # uploaded_handler 上传回调函数: 该函数用于上传完成后进一步处理文件(设置提取码, 描述信息等)
        code = self.lzy.upload_file(file_path, folder_id, callback=None, uploaded_handler=self.handler)
        if code == 0:
            print(f'上传文件 {file_name} 成功')

    # 上传一个文件夹  本地文件夹路径(dir_path必填)  网盘文件夹id(folder_id)
    # 进度回调函数(callback)  失败处理回调函数(failed_callback)   上传回调函数(uploaded_handler)
    def UPLOAD_dir(self, dir_path, parent_name, callback=None, failed_callback=None, uploaded_handler=None):
        folder_id = self.get_FOLDER_ID(parent_name)
        print(f'dir_path: {dir_path}\nfolder_id: {folder_id}\nfolder_name:  {parent_name}')
        handler = lanzou._handler(folder_id, False)
        code = self.lzy.upload_dir(dir_path, int(folder_id), callback=show_progress, uploaded_handler=self.handler)
        if code == 0:
            print(f'上传 {dir_path} 成功 folder_id:{folder_id}')

    # 重命名 并 移动这个文件夹
    #                             文件名      新文件名           父级文件名    修改描述信息   是否为文件
    def get_FOLDER_ID_move(self, folder_name, new_folder_name, parent_name, desc, is_file=False):
        folder_ID = self.get_FOLDER_ID(folder_name)
        ex = exID(parent_name)
        print(f'ex parent_name: {ex}')
        parent_folder_id = self.get_FOLDER_ID(parent_name)
        print(f'folder_ID: {folder_ID}')
        print(f'parent_folder_id: {parent_folder_id}')
        ## 重命名
        # self.RENAME_dir(folder_ID,new_folder_name)

        ## 修改信息
        # lzy.set_desc(1083604, '批量上传的音乐', is_file=False)
        # self.SET_desc(folder_ID, desc, is_file)

        ## 移动
        # self.MOVE_folder(folder_ID, parent_folder_id)

        # 上传

    def UPLOAD_files_from_DIR(self, file_dir, parent_name):
        for root, dirs, files_list in os.walk(file_dir):
            print("files_list", files_list)  # 当前路径下所有非目录子文件
        for i in files_list:
            file_path = file_dir + '/' + i
            print(file_path)
            self.UPLOAD_file(file_path, parent_name)


def test(lz):
    #                             文件名      新文件名       父级文件名    修改描述信息   是否为文件
    # lz.get_FOLDER_ID_move('HISTORY', 'HISTORY1', '360T7', f'360T7_固件_{nowtime}', False)
    # 移动文件夹
    # lz.get_FOLDER_ID_move('latest', f'{nowtime}', 'HISTORY', f'{nowtime}', False)
    # 上传文件夹
    # lz.UPLOAD_dir(r'/volume3/test1/360T7', 'HISTORY1',show_progress, None, None)
    pass
    # 上传文件
    # lz.UPLOAD_file(r"/volume3/test1/id1.rar", 'HISTORY1')


'''
    def login_by_cookie(self, cookie: dict) -> int:
        """通过cookie登录"""
        self._session.cookies.update(cookie)
        html = self._get(self._account_url)

    def get_file_list(self, folder_id=-1) -> FileList:
        """获取文件列表"""
        page = 1
        file_list = FileList()
        while True:
            post_data = {'task': 5, 'folder_id': folder_id, 'pg': page, 'vei': 'vei'}
'''


def main():
    lz = lanzou()
    # old_latest = lz.get_FOLDER_ID('latest')
    # print(f"old_latest: {old_latest}")
    # ex = "FolderId\(name='latest', id=(\d+)\)"
    # #   # re.S 单行匹配  re.M多行匹配
    # old_latest_ID = re.findall(ex, str(old_latest), re.S)[0]
    # print(f"resFOLDERS: {type(old_latest_ID)} {old_latest_ID}")
    nowtime = str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M.%S'))
    # # 重命名
    # print(nowtime,type(nowtime))

    test(lz)
    # 命名文件夹
    # lz.RENAME_dir(old_latest_ID,nowtime)

    # 移动
    # lz.MOVE_folder(old_latest_ID,)

    # old_latestId = re.findall(r"name='latest', ", resFOLDERS)
    # print(old_latestId)


    # # 创建文件夹 放在哪个目录    文件夹名称
    father_id = lz.get_FOLDER_ID(LZ_folder_name)
    lz.MKDIR_folder(father_id, nowtime, f'历史资料')

    # # 移动文件夹下所有的文件  到新文件夹
    lz.MKDIR_files_from_folder(MOVE_dir, nowtime)

    # 上传Github_path目录下的所有文件 到 MOVE_dir
    lz.UPLOAD_files_from_DIR(Github_path, MOVE_dir)


if __name__ == '__main__':
    main()

