# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件实现了对bos的封装, 首先安装 bce-python-sdk

Authors: suoyi@baidu.com
Date:    2024/01/03

"""
import logging
import os
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
from baidubce import utils


def sts_client(bos_host, sts_ak, sts_sk, session_token) -> BosClient:
    """
    获取sts client
    """

    bos_client = BosClient(BceClientConfiguration(
                                credentials=BceCredentials(sts_ak, sts_sk),
                                endpoint=bos_host,
                                security_token=session_token))
    return bos_client


def upload_files(bos_client: BosClient, bucket: str, files: list[str], key_prefix=""):
    """
    上传文件
    key_prefix: 上传文件的前缀
    """
    for file in files:
        bos_client.put_super_obejct_from_file(bucket, key_prefix + file, file, chunk_size=5, thread_num=None)

def upload_file(bos_client: BosClient, bucket: str, file, key):
    """
    上传文件
    key: 存储路径
    """

    return bos_client.put_object_from_file(bucket, key, str(file))


def upload_super_file(bos_client: BosClient, bucket: str, file, key):
    """
    上传文件
    key: 存储路径
    """
    chunk_size = int(os.environ.get("AISTUDIO_UPLOAD_CHUNK_SIZE_MB", 5))

    res = bos_client.put_super_obejct_from_file(bucket, key, str(file),
                                                 chunk_size=chunk_size,
                                                 progress_callback=utils.default_progress_callback)
    if not res:
        logging.error("upload file failed: 已经取消或者上传失败，如果上传失败，"
                      "请配置环境变量 AISTUDIO_UPLOAD_CHUNK_SIZE_MB (int类型，默认为5，单位MB)，减小分块大小后重试，"
                      "例如：export AISTUDIO_UPLOAD_CHUNK_SIZE_MB=3 后重新执行")
    return res
