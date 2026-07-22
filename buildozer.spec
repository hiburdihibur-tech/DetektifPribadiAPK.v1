[app]

title = DetektifPribadi

package.name = detektifpribadi

package.domain = com.hiburdihibur

source.dir = .

source.include_exts = py,kv,json,png,jpg,txt

version = 1.0

requirements = python3,kivy,requests

orientation = portrait

fullscreen = 0

#
# Android
#

android.api = 34

android.minapi = 24

android.ndk = 25b

android.accept_sdk_license = True

p4a.branch = develop

android.archs = arm64-v8a, armeabi-v7a

#
# Include Folder
#

source.include_patterns = assets/*,data/*,kv/*,core/*

#
# Android Permission
#

android.permissions = INTERNET

#
# Log
#

log_level = 2

#
# End
#
