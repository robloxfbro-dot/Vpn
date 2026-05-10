[app]
title = Swill Way VPN
package.name = swillwayvpn
package.domain = org.swillway
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = libs/*,service/*
version = 1.1
requirements = python3,kivy==2.2.1,pyjnius,requests,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, BIND_VPN_SERVICE, FOREGROUND_SERVICE
android.services = {"org.swillway.PythonService": "service/main.py"}
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
