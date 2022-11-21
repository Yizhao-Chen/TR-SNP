import cx_Freeze
import sys
import os
import traceback

base = None

if sys.platform == "win32":
    base = "Win32GUI"

exe_path = os.getcwd()

os.environ['TCL_LIBRARY'] = r'{0}\tcl\tcl8.6'.format(exe_path)
os.environ['TK_LIBRARY'] = r'{0}\tcl\tk8.6'.format(exe_path)

include_files = [r"{0}\tcl\tcl86t.dll".format(exe_path),
                  r"{0}\tcl\tk86t.dll".format(exe_path)]

packages = ['tkinter','shutil','fnmatch','os','sys','csv','rpy2','tzlocal','matplotlib','numpy','pandas','asyncio']

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
            , 'include_files': ['GFNWE.py','open_metafile.py','plot.py','tcl86t.dll','tk86t.dll','r']
        }
}

executables = [
    cx_Freeze.Executable(
        'TR_SNP.py'
        , base=base
        , targetName='TR_SNP.exe'
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