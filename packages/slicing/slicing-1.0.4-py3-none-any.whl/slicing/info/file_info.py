from dataclasses import dataclass


@dataclass
class FileInfo:
    sql_type: str
    name: str
    table: str
    id: str
    size: int # 单位字节
    no: int # 顺序编号
