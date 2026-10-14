[app]
title = Mani Labs Solution
package.name = manilabssolution
package.domain = com.manilabs.solution

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,db

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.ant = auto

[buildozer]
log_level = 2
warn_on_root = 1
