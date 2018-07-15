"""
Text-to-speech over SSH


{"text": "Hello world"}

"""

#import subprocess

text = data.get("text")
if text:
    subprocess.check_output('ssh ipad "say {}"'.format(text))
