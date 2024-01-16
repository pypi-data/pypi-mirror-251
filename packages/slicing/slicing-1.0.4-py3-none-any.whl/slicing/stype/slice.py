import abc
import re
import time
import uuid
from pathlib import Path

from slicing.info.file_info_writer import FileInfoWriter
from slicing.stype.line_number import LineNumber
from slicing.writer import Writer


class Slice(abc.ABC):

    def __init__(self):
        self._out_put = "xxxx"
        self.line_no = LineNumber()
        self.writer = None
        self._task_id = None
        self._file_list_writer = None

    def ready(self, out_put):
        """
        指定输出的文件夹路径，并启动写文件的线程
        :param out_put:
        :type out_put:
        :return:
        :rtype:
        """
        self.out_put = out_put
        self.writer = Writer(self, self.line_no)
        self._file_list_writer = FileInfoWriter(Path(self.out_put).joinpath(self.task_id))
        self._file_list_writer.set_id(self.task_id)
        self.writer.start()

    @property
    def out_put(self):
        return self._out_put

    @property
    def file_list_writer(self):
        return self._file_list_writer

    @out_put.setter
    def out_put(self, value):
        self._out_put = value

    @abc.abstractmethod
    def read(self, file: Path):
        ...

    def slice(self, file: Path):
        try:
            self.read(file)
            self.join()
            self.file_list_writer.write()
        except Exception as e:
            self.writer.stop()
            raise e

    def statements(self, file):
        start = time.perf_counter()
        buffer = []

        for line in file:
            if Slice.empty_line(line) or Slice.comment_line(line): continue
            buffer.append(line)
            if line.endswith(b';\n') or line.endswith(b';\n\r') or line.endswith(b';\r\n'):
                self.writer.add_statements(buffer.copy())
                # self.writer.add_statements(buffer)
                buffer = []
        self.writer.finish()
        print("Load File end", time.perf_counter() - start)

    @staticmethod
    def comment_line(line):
        """
        判断是注释行
        :param line:
        :type line:
        :return:
        :rtype:
        """
        if line.startswith(b'--') or line.startswith(b'/*'):
            patterns = [r'\-\-.*', r'\*.*?\*/']
            for pattern in patterns:
                if re.search(re.compile(pattern), line.decode()): return True
        return False

    @staticmethod
    def empty_line(line):
        """
        判断是否是空行
        :param line:
        :type line:
        :return:
        :rtype:
        """
        return line == b'\r\n' or line == b'\n\r' or line == b'\n'

    @property
    def task_id(self):
        if self._task_id is None:
            self._task_id = str(uuid.uuid4()).replace("-", "")
        return self._task_id

    def join(self):
        self.writer.join()
