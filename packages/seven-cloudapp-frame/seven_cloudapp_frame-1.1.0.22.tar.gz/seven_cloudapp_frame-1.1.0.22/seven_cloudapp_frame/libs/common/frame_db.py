# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-03-06 23:17:54
@LastEditTime: 2024-01-18 17:56:55
@LastEditors: HuangJianYi
:Description: 框架DB操作类
"""
from seven_framework.base_model import *
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *

class FrameDbModel(BaseModel):

    def __init__(self, model_class, sub_table):
        """
        :Description: 框架DB操作类
        :param model_class: 实体对象类
        :param sub_table: 分表标识
        :last_editors: HuangJianYi
        """
        super(FrameDbModel,self).__init__(model_class, sub_table)

    def get_business_sub_table(self, table_name, param_dict):
        """
        :description: 获取分表名称(目前框架支持的分表prize_order_tb、prize_roster_tb、stat_log_tb、task_count_tb、user_asset_tb、asset_log_tb、user_info_tb)
        :param table_name:表名
        :param param_dict:参数字典
        :return:
        :last_editors: HuangJianYi
        """
        if not param_dict or not table_name:
            return None    
        sub_table_config = share_config.get_value("sub_table_config",{})
        table_config = sub_table_config.get(table_name, None)
        if not table_config:
            return None
        return SevenHelper.get_sub_table(param_dict.get("app_id", 0), table_config.get("sub_count", 10))
    

