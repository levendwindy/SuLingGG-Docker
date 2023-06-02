#!/usr/bin/python
import re
import datetime
import sys
from lanzou.api import LanZouCloud

ylogin = sys.argv[1]
phpdisk_info = sys.argv[2]
cookie = {'ylogin': f'{ylogin}', 'phpdisk_info': f'{phpdisk_info}'}

# LZ_YLOGIN      LZ_PHPDISK
# 通过 id 获取文件夹的绝对路径
def show_progress(file_name, total_size, now_size):
    """显示进度的回调函数"""
    percent = now_size / total_size
    bar_len = 40  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
    if total_size == now_size:
        print('')  # 下载完成换行

def handler(fid, is_file=True):
    if is_file:
        lzy.lanzou.set_desc(fid, '这是文件的描述', is_file)

def exID(folder_name):
    ex = f"FolderId\(name='{folder_name}', id=(\d+)\)"
    return ex

class lanzou(object):
    def __init__(self):
        self.lzy = LanZouCloud()
        res = self.lzy.login_by_cookie(cookie)
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
    def get_FOLDER_ID(self,name):
        folders = self.lzy.get_move_folders()
        return folders.find_by_name(name)


    # 移动文件夹(id=1384074)到文件夹(id=879591)内
        #       lzy.move_file(12741016, 1037083)
    def MOVE_folder(self, folder_ID,parent_folder_id):
        try:
            res = self.lzy.move_folder(int(folder_ID), int(parent_folder_id))
        except TypeError:
            print(f'文件夹并未改变位置，移动失败\nparent_folder_id: {parent_folder_id}')
        except Exception as result:
            print("未知错误 %s" % result)
        else:
            if res == 0:
                print(f'已将文件夹 {folder_ID} 移至 {parent_folder_id}')
            elif res == -1:
                print(f'移动失败 文件夹 {folder_ID} 位于同级目录')
            else:
                print(f'移动失败 res： {res}')

    # 移动文件(id=12741016) 到文件夹(id=1037083)
    #    lzy.move_file(12741016, 1037083) == LanZouCloud.SUCCESS
    def MOVE_file(self, folder_id, parent_folder_id):
        if self.lzy.move_file(int(folder_id), int(parent_folder_id)) == 0:
            print(f'已将文件 {int(folder_id)} 移动至 {int(parent_folder_id)}')
        else:
            print(f'移动文件错误，res: {self.lzy.move_file(int(folder_id), int(parent_folder_id))}')

    # 创建文件夹并返回id
    #        lzy.mkdir(-1, 'my_music', '音乐分享')
    def MKDIR_folder(self,parent_id, folder_name, desc):
        fid = self.lzy.mkdir(self,parent_id, folder_name, desc)
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
    def SET_passwd(self, fid, passwd, is_file=False):
        if self.lzy.set_passwd(int(fid), passwd, is_file) == 0:
            print(f'修改文件(夹) {int(fid)} 提取码为 {passwd}')

    def UPLOAD_file(self, file_path, folder_id, callback=show_progress, uploaded_handler=handler):
        if self.lzy.upload_file(file_path, int(folder_id), callback, uploaded_handler) == 0:
            print(f'上传文件{file_path}成功')



    # 上传一个文件夹  本地文件夹路径(dir_path必填)  网盘文件夹id(folder_id)
    # 进度回调函数(callback)  失败处理回调函数(failed_callback)   上传回调函数(uploaded_handler)
    def UPLOAD_dir(self, dir_path, folder_id='-1', callback=None, failed_callback=None, uploaded_handler=None):
        self.upload_dir(dir_path, folder_id, callback, failed_callback, uploaded_handler)
        code = lzy.upload_dir(r"D:\test", dir_path, callback=show_progress, failed_callback=show_failed, uploaded_handler=handler)

    # 重命名 并 移动这个文件夹
    #                             文件名      新文件名           父级文件名    修改描述信息   是否为文件
    def get_FOLDER_ID_move(self,folder_name, new_folder_name, parent_name, desc, is_file=False):
        ex = exID(folder_name)
        folder_ID = re.findall(ex, str(self.get_FOLDER_ID(folder_name)), re.S)[0]
        ex = exID(parent_name)
        print(f'ex parent_name: {ex}')
        parent_folder_id = re.findall(ex, str(self.get_FOLDER_ID(parent_name)), re.S)[0]
        print(f'folder_ID: {folder_ID}')
        print(f'parent_folder_id: {parent_folder_id}')
        ## 重命名
        self.RENAME_dir(folder_ID,new_folder_name)

        ## 修改信息
        # lzy.set_desc(1083604, '批量上传的音乐', is_file=False)
        self.SET_desc(folder_ID, desc, is_file)

        # new_folder_ID = re.findall(exID(new_folder_name), str(self.get_FOLDER_ID(new_folder_name)), re.S)[0]
        # print(f'new_folder_ID: {new_folder_ID}')
        ## 移动
        self.MOVE_folder(folder_ID, parent_folder_id)

def test(lz):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    #                             文件名      新文件名       父级文件名    修改描述信息   是否为文件
    lz.get_FOLDER_ID_move('HISTORY', 'HISTORY1', '360T7', f'360T7_固件_{nowtime}', False)
    # 移动文件夹
    # lz.get_FOLDER_ID_move('latest', f'{nowtime}', 'HISTORY', f'360T7_固件_{nowtime}', False)






def main():
    lz = lanzou()
    # old_latest = lz.get_FOLDER_ID('latest')
    # print(f"old_latest: {old_latest}")
    # ex = "FolderId\(name='latest', id=(\d+)\)"
    # #   # re.S 单行匹配  re.M多行匹配
    # old_latest_ID = re.findall(ex, str(old_latest), re.S)[0]
    # print(f"resFOLDERS: {type(old_latest_ID)} {old_latest_ID}")
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # # 重命名
    # print(nowtime,type(nowtime))

    test(lz)
    # 命名文件夹
    # lz.RENAME_dir(old_latest_ID,nowtime)

    # 移动
    # lz.MOVE_folder(old_latest_ID,)

    #old_latestId = re.findall(r"name='latest', ", resFOLDERS)
    # print(old_latestId)


if __name__=='__main__':
    main()
