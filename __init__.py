from flask import Flask

import os
import subprocess
import time

# import markisol
# import atexit
#
# I don't know why calling the funcs from the file
# doesn't work when called from a Flask handler,


dir_path = os.path.dirname(os.path.realpath(__file__))


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # markisol.init()
    # atexit.register(markisol.cleanup)

    @app.route('/up')
    def shadeUp():
        # markisol.send('up')
        subprocess.call(['%s/markisol.py' % dir_path, 'up'])
        return "OK"

    @app.route('/down')
    def shadeDown():
        # markisol.send('down')
        subprocess.call(['%s/markisol.py' % dir_path, 'down'])
        return "OK down"

    @app.route('/stop')
    def shadeStop():
        # markisol.send('stop')
        subprocess.call(['%s/markisol.py' % dir_path, 'stop'])
        return "OK"

    @app.route('/ir/activities/off')
    def ir_activities_off():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_POWER2'])
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        time.sleep(1)
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        time.sleep(2)
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        return "OK" 

    @app.route('/ir/activities/music')
    def ir_activities_music():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_PROG1'])
        return "OK"

    @app.route('/ir/activities/movies')
    def ir_activities_movies():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_PROG1'])
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER'])
        return "OK"

    @app.route('/ir/activities/switch')
    def ir_activities_switch():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_PROG2'])
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER'])
        return "OK"

    @app.route('/ir/activities/ps4')
    def ir_activities_ps4():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_PROG3'])
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER'])
        return "OK"

    @app.route('/ir/devices/optoma/on')
    def ir_devices_optoma_on():
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER'])
        return "OK"

    @app.route('/ir/devices/optoma/off')
    def ir_devices_optoma_off():
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        time.sleep(1)
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        time.sleep(2)
        subprocess.call(['irsend', 'SEND_ONCE', 'optoma', 'KEY_POWER2'])
        return "OK"

    @app.route('/ir/devices/denon/on')
    def ir_devices_denon_on():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_POWER'])
        return "OK"

    @app.route('/ir/devices/denon/off')
    def ir_devices_denon_off():
        subprocess.call(['irsend', 'SEND_ONCE', 'denon', 'KEY_POWER2'])
        return "OK"

    return app
