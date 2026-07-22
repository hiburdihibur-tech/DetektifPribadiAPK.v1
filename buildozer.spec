[app]

title = Detektif Pribadi
package.name = detektifpribadi
package.domain = com.hendychinto

source.dir = .
source.include_exts = py,kv,png,jpg,json,ttf

version = 1.0

requirements = python3,kivy==2.3.0,requests

orientation = portrait

fullscreen = 0

icon.filename = assets/icon.png

presplash.filename = assets/splash.png

log_level = 2

#####################################################################
# Android
#####################################################################

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 26b

android.accept_sdk_license = True

android.permissions = INTERNET

android.archs = arm64-v8a

android.allow_backup = False

#####################################################################
# Buildozer
#####################################################################

warn_on_root = 0

build_dir = .buildozer

bin_dir = bin

#####################################################################
# Python-for-Android
#####################################################################

# Jangan gunakan develop
# p4a.branch =
# p4a.commit =

#####################################################################
# Kivy
#####################################################################

osx.python_version = 3

osx.kivy_version = 2.3.0
