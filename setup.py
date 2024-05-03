from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('gui.py', base=base, target_name = 'ABLE-Generator')
]

setup(name='ABLEBadgeGenerator',
      version = '1.0',
      description = 'Badge pdf generator for the ABLE Organization',
      options = {'build_exe': build_options},
      executables = executables)
