import cx_Freeze
import sys
import os
import traceback

base = None

if sys.platform == "win32":
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r'D:\software\Python3.7.3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\software\Python3.7.3\tcl\tk8.6'

packages = ['tkinter','shutil','fnmatch','os','csv','rpy2','tzlocal','matplotlib','numpy','pandas','asyncio']

for dbmodule in ['win32gui','win32api' ,'win32con' , 'cx_Freeze']:

    try:
            __import__(dbmodule)

    except ImportError:
        pass

    else:
        packages.append(dbmodule)

options = {
    'build_exe':
        {
            'includes': 'atexit'
            , "packages": packages
            , 'include_files': ['GFNWE.py','open_metafile.py','plot.py','tcl86t.dll','tk86t.dll']
        }
}

executables = [
    cx_Freeze.Executable(
        'TR_SNP.py'
        , base=base
        , targetName='TR_SNP.exe'
        # 生成的EXE的图标
        # , icon = "test_32.ico" #图标, 32*32px
    )
]

cx_Freeze.setup(
    name='TR_SNP',
    version='1.0',
    description='Tree ring_search n plot',
    author = 'Yizhao Chen',
    author_email = 'chenyzvest@gmail.com',
    options=options,
    executables = executables
)