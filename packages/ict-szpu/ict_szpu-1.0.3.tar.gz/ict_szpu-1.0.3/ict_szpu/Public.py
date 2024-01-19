import time
import ict_szpu.core
from ict_szpu.core import MyWS


class audio:

    def __init__(self):
        pass

    def audio_load(self, file_name: str):
        """
        加载音频
        :param file_name:
        :return:
        """
        # MyWS.do_immediately(
        #     {'type': 'other', 'commond': 'audio_load', 'file_name': file_name})

        result =MyWS.do_wait_return( {'type': 'other', 'commond': 'audio_load', 'file_name': file_name})
        if result['result'] == ict_szpu.core.SUCCESS:
            return True
        else:
            print(result['msg'])
            return False

    def audio_play(self):
        """
        播放音频
        :return:
        """
        MyWS.do_immediately({'type': 'other', 'commond': 'audio_play'})
        return

    def audio_pause(self):
        """
        暂停音频播放
        :return:
        """
        MyWS.do_immediately({'type': 'other', 'commond': 'audio_pause'})
        return

    def audio_stop(self):
        """
        关闭音频
        :return:
        """
        MyWS.do_immediately({'type': 'other', 'commond': 'audio_stop'})
        return

    def audio_set_volume(self,volume:float):
        """
        设置音量
        :param volume: 音量大小(0~1)
        :return:
        """
        MyWS.do_immediately({'type': 'other', 'commond': 'audio_set_volume','volume':volume})
        return


def screen_shot(isStep:bool, stepName:str=''):
    """
    截图
    :param isStep: False:整个任务截图，True:单个步骤截图
    :param stepName: 填写对应步骤名，用于对应步骤
    :return:
    """
    if isStep==True:
        if stepName=='':
            print('截图步骤时步骤名称不能为空')
            return

    MyWS.do_immediately({'type': 'other', 'commond': 'screen_shot','isStep':isStep,'stepName':stepName})
    return