from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('TR_SNP', base=base)
]

setup(name='TR_test1',
      version = '1.0',
      description = 'test version of TRONE',
      options = dict(build_exe = buildOptions),
      executables = executables)
