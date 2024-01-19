#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
from typing import Tuple
from multiprocessing import Pool

from ykenan_file import StaticMethod
from ykenan_log import Logger
from ykenan_util import Util


class Download:

    def __init__(
        self,
        bulk_file: str,
        output_path: str,
        ukbfetch_file: str = "ukbfetch",
        key_file: str = "ukb.key",
        dir_number: int = 1000,
        number: int = 10,
        region_number: int = 10,
        start: int = 0
    ):
        """
        UK BioBank Download
        :param bulk_file: The specified bulk file
        :param output_path: File Output Path
        :param ukbfetch_file: Executable ukbfetch file
        :param key_file: The key file for the Application ID
        :param dir_number: Download to generate a quantity within a folder
        :param number: Parallel quantity
        :param region_number: The number of downloads in a loop in parallel
        :param start: The first number to start downloading
        """
        # log 日志信息
        self.log = Logger("UK Biobank download", "log")
        # 处理路径和文件的方法
        self.file = StaticMethod(log_file="log")
        self.util = Util(log_file="log")
        self.log_path = "log"
        # self.file.makedirs(self.log_path)

        self.bulk_file = bulk_file
        self.ukbfetch_file = ukbfetch_file
        self.key_file = key_file
        self.start = start

        self.output_path = output_path

        if dir_number % number != 0:
            self.log.error("`dir_number` needs to be a multiple of `number`")
            raise ValueError("`dir_number` needs to be a multiple of `number`")

        self.dir_number = dir_number
        self.number = number
        self.region_number = region_number
        self.region_total = int(self.dir_number / self.region_number)
        self.region_iter = int(self.dir_number / self.number)

    def _exec_(self, param: Tuple):
        start, end, log, output = param
        exec_str: str = f"{self.ukbfetch_file} -b{self.bulk_file} -a{self.key_file} -s{start} -m{self.region_number} -o{log}"
        self.util.exec_command(exec_str)

        # 移动文件
        lsi_log_file_dict: dict = self.file.entry_contents_dict(self.log_path, 1, ".lis")
        lsi_log_file_list: list = lsi_log_file_dict["name"]

        for lsi_log_file in lsi_log_file_list:
            lsi_log_file: str
            # 读取文件
            all_filenames = self.file.read_file_line(lsi_log_file_dict[lsi_log_file])

            filenames = []
            for i in all_filenames:
                if i is not None and i != "":
                    filenames.append(i)

            if len(filenames) > 0:
                # 文件移动
                for filename in filenames:

                    if os.path.exists(filename):
                        try:
                            self.file.move_file(filename, os.path.join(output, filename))
                        except Exception as e:
                            self.log.warn(f"{e.args}")

                if os.path.exists(lsi_log_file_dict[lsi_log_file]):
                    try:
                        self.file.move_file(lsi_log_file_dict[lsi_log_file], os.path.join(self.log_path, f"{lsi_log_file}.log"))
                    except Exception as e:
                        self.log.warn(f"{e.args}")

    def run(self):

        pool = Pool(self.number)

        i = 0

        #  External loop determines the folder
        while True:
            start: int = (i * self.dir_number + 1) + self.start
            end: int = ((i + 1) * self.dir_number) + self.start
            name: str = f"{i}_{start}_{end}"
            self.log.info(f"Start {start} ===> {end}")

            output: str = os.path.join(self.output_path, name)
            self.file.makedirs(output)

            # Identify files in the folder and perform multithreading
            for j in range(self.region_iter):
                self.log.info(f"Start {j}: {start} ===> {end}")

                # Form multi-threaded parameters
                params: list = []
                for z in range(self.number):
                    region_start = (j * self.region_iter) + (z * self.region_number + 1) + self.start
                    region_end = (j * self.region_iter) + ((z + 1) * self.region_number) + self.start
                    log_file: str = os.path.join(self.log_path, f"{name}__{j}_{region_start}_{region_end}.log")

                    self.log.info(f"{log_file}")
                    params.append((region_start, region_end, log_file, output))

                # 执行
                pool.map(self._exec_, params)

            i += 1

        pool.close()


if __name__ == '__main__':
    download = Download(
        ukbfetch_file="/mnt/f/software/ukbiobank/ukbfetch",
        bulk_file="/mnt/f/software/ukbiobank/ukb676745.bulk",
        key_file="/mnt/f/software/ukbiobank/k152703r676745.key",
        output_path="/mnt/h/ukbiobank/download",
        start=20210
    )
    download.run()
