# path_config.py

import os


# path to this file
module_file = os.path.abspath(__file__)
# path to directory
module_path = os.path.dirname(module_file)

## path containing font_hyper sub directory and run.sh
## compute relative:
font_hyper_module_path = os.path.join( module_path, "../")
font_hyper_module_path = os.path.abspath (font_hyper_module_path)
## or set directly:
#font_hyper_module_path = "~/apps/font_hyper_manager/" # TODO: make cross platform
##
print ( f"font_hyper , assumed installation directory: {font_hyper_module_path}") 


home_dir = os.path.expanduser('~')  # TODO: make cross platform
print (f"assumed user directory base: {home_dir}")

# Font installation paths by platform
font_install_path_windows = '~/AppData/Local/Microsoft/Windows/Fonts'
font_install_path_mac = '~/Library/Fonts'
font_install_path_linux = '~/.local/share/fonts/font_hyper'
font_install_path_android = '/data/fonts'
font_install_path_bsd = '~/.local/share/fonts'

#############
## IMPORTANT: the font_install_path should not be a sub-path of
## font_sys_paths lists (nor font_manager.user_paths lists), 
## nor be included in any these lists
## obviously we want no recursion, where install path is equal to source path

# System font search paths by platform
font_sys_paths_windows = [
    'C:\\Windows\\Fonts',
    'C:\\Program Files\\Common Files\\Microsoft\\Shared\\Fonts',
    'C:\\Program Files (x86)\\Common Files\\Microsoft\\Shared\\Fonts'
]

font_sys_paths_mac = [
    '/Library/Fonts',
    '/System/Library/Fonts',
    '/System/Library/Fonts/Supplemental'
]

font_sys_paths_linux = [
    '/usr/share/fonts',
    '/usr/local/share/fonts',
    '/usr/share/fonts/truetype',
    '/usr/share/fonts/opentype',
    '/usr/share/fonts/TTF',
    '/usr/share/fonts/OTF'
]

font_sys_paths_android = [
    '/system/fonts',
    '/system/font',
]

font_sys_paths_bsd = [
    '/usr/local/share/fonts',
    '/usr/X11R6/lib/X11/fonts'
]

# Configuration base paths by platform
config_base_path_windows = os.path.expanduser("~/AppData/Roaming/")
config_base_path_mac = os.path.expanduser("~/Library/Application Support/")
config_base_path_linux = "~/.config/"
config_base_path_android = "/data/data/com.your.app/files/"  # Typically app-specific on Android
config_base_path_bsd = "~/.config/"  # BSD typically follows Linux XDG convention

# Application specific config directory name
APP_CONFIG_DIR = "font_hyper_conf"

def get_system_paths():
    """Returns appropriate system font paths based on platform."""
    import platform
    system = platform.system().lower()
    
    if system == 'windows':
        return font_sys_paths_windows
    elif system == 'darwin':
        return font_sys_paths_mac
    elif system == 'linux':
        return font_sys_paths_linux
    elif system == 'android':
        return font_sys_paths_android
    elif 'bsd' in system:
        return font_sys_paths_bsd
    else:
        return []

def get_install_path():
    """Returns appropriate font installation path based on platform."""
    import platform
    system = platform.system().lower()
    
    if system == 'windows':
        return font_install_path_windows
    elif system == 'darwin':
        return font_install_path_mac
    elif system == 'linux':
        return font_install_path_linux
    elif system == 'android':
        return font_install_path_android
    elif 'bsd' in system:
        return font_install_path_bsd
    else:
        return '~/.fonts'  # fallback to XDG standard

def get_config_base_path():
    """Returns appropriate configuration base path based on platform."""
    import platform
    system = platform.system().lower()
    
    if system == 'windows':
        return config_base_path_windows
    elif system == 'darwin':
        return config_base_path_mac
    elif system == 'linux':
        return config_base_path_linux
    elif system == 'android':
        return config_base_path_android
    elif 'bsd' in system:
        return config_base_path_bsd
    else:
        return '~/.config/'  # fallback to XDG standard

def get_config_path():
    """Returns the full configuration path for the application based on platform.
    
    Returns:
        str: Full path to the application's configuration directory
    """
    base_path = get_config_base_path()
    return os.path.join(os.path.expanduser(base_path), APP_CONFIG_DIR)
#
