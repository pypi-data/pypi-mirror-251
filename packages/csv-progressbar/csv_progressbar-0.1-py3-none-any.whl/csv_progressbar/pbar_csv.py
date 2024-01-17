import os
from typing import TypeAlias
from io import TextIOWrapper
import csv
from csv import Dialect

from .pbar_protocol import PbarProtocol

_DialectLike: TypeAlias = str | Dialect | type[Dialect]
_QuotingType: TypeAlias = int


def read_with_pbar(csvfile: TextIOWrapper,
        pbar: PbarProtocol,
        update_rate: int = 32768,
        dialect: _DialectLike = "excel",
        *,
        delimiter: str = ",",
        quotechar: str | None = '"',
        escapechar: str | None = None,
        doublequote: bool = True,
        skipinitialspace: bool = False,
        lineterminator: str = "\r\n",
        quoting: _QuotingType = 0,
        strict: bool = False):
    
    """
    csv reader as from the original library, 
    additionally gets a progress bar object 
    and the number of rows after which the update occurs

    ProgressBar object must have `update` method
    ```
    pbar = MyPbar(...) 
    with open('my_file.csv') as csvfile:
        reader = read_with_pbar(csvfile, pbar)
        for row in reader:
            ...
    ```
    
    """
    
    fd = csvfile.fileno()
    readed_rows = 0
    last_pos = 0
    reader = csv.reader(csvfile, 
                                 dialect, 
                                 delimiter= delimiter,
                                 quotechar= quotechar,
                                 escapechar= escapechar,
                                 doublequote= doublequote,
                                 skipinitialspace= skipinitialspace,
                                 lineterminator = lineterminator,
                                 quoting= quoting,
                                 strict= strict)
    
    for row in reader:
        readed_rows += 1
        if readed_rows == update_rate:
            readed_rows = 0
            pos = os.lseek(fd, 0, os.SEEK_CUR)
            if last_pos != pos:
                pbar.update(pos - last_pos)
                last_pos = pos
        yield row
        
    if readed_rows != 0:
        pos = os.lseek(fd, 0, os.SEEK_CUR)
        last_pos = last_pos
        if last_pos != pos:
            pbar.update(pos - last_pos)

        
        