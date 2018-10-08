
command = data.get("command")
arguments = data.get("data")
if command == 'say':
    subprocess.check_output('ssh ipad say {}'.format(arguments), shell=True)
elif command == 'siri':
    subprocess.check_output("ssh ipad say hey siri, {}".format(arguments), shell=True)
elif command == 'remote':
    subprocess.check_output("ssh ipad activator send com.apple.mobilesafari", shell=True)
elif command == 'sleep':
    subprocess.check_output("ssh ipad activator send libactivator.system.sleepbutton", shell=True)
elif command == 'ringtone':
    # News Flash, New Mail, Update, Ladder, Calypso, Minuet, Descent, Suspense, Bloom, Glass, Tri-tone, Choo Choo, Chime, Electronic
    # Bell, Telegraph, Anticipate, Sherwood Forest, Noir, Tiptoes, Typewriters, Calendar Alert, Sent Mail, Fanfare, Sent Tweet, Horn
    # Spell, Alarm, Ascending, Bark, Bell Tower, Blues, Boing, Crickets, Digital, Doorbell, Duck, Harp, Motorcycle, Old Car Horn
    # Old Phone, Piano Riff, Pinball, Robot, Sci-Fi, Sonar, Strum, Timba, Time Passing, Trill, Xylophone
    if arguments.lower() == 'tri-tone':
        arguments = 'Tri-tone'
    else:
        arguments = arguments.title()
    subprocess.check_output("ssh ipad activator send libactivator.ringtone.system:{}".format(arguments), shell=True)
elif command == "test":
    subprocess.Popen(["ssh", "-i /data/.ssh/id_rsa root@ipad", "say hello world"], shell=True) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.warning("Yes")
