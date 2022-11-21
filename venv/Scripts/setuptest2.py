from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('TR_SNP.py', base=base)
]

setup(name='TR_SNP_test',
      version = '1.0',
      description = 'none',
      options = dict(build_exe = buildOptions),
      executables = executables)
