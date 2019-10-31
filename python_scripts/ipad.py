import subprocess

host = "root@10.10.10.3"
key = "home/romanpeters/.ssh/id_rsa.pub"

command = data.get("command")
arguments = data.get("data")
if command == 'say':
    x = subprocess.check_output(f'ssh -i {key} -o StrictHostKeyChecking=no {host} say {arguments}', shell=True)
    logger.warning(x)
elif command == 'siri':
    subprocess.check_output(f"ssh {host} -i {key} -o StrictHostKeyChecking=no say hey siri, {arguments}", shell=True)
elif command == 'on':
    subprocess.check_output(f"ssh {host} -i {key} -o StrictHostKeyChecking=no activator send com.realvnc.VNCViewer", shell=True)
elif command == 'sleep':
    subprocess.check_output(f"ssh {host} -i {key} -o StrictHostKeyChecking=no activator send libactivator.system.sleepbutton", shell=True)
elif command == 'ringtone':
    # News Flash, New Mail, Update, Ladder, Calypso, Minuet, Descent, Suspense, Bloom, Glass, Tri-tone, Choo Choo, Chime, Electronic
    # Bell, Telegraph, Anticipate, Sherwood Forest, Noir, Tiptoes, Typewriters, Calendar Alert, Sent Mail, Fanfare, Sent Tweet, Horn
    # Spell, Alarm, Ascending, Bark, Bell Tower, Blues, Boing, Crickets, Digital, Doorbell, Duck, Harp, Motorcycle, Old Car Horn
    # Old Phone, Piano Riff, Pinball, Robot, Sci-Fi, Sonar, Strum, Timba, Time Passing, Trill, Xylophone
    if arguments.lower() == 'tri-tone':
        arguments = 'Tri-tone'
    else:
        arguments = arguments.title()
    subprocess.check_output(f"ssh {host} -i {key} -o StrictHostKeyChecking=no activator send libactivator.ringtone.system:{arguments}", shell=True)
elif command == "test":
    subprocess.Popen([f"ssh {host} -i {key} -o StrictHostKeyChecking=no say 'hello world'"], shell=True) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.warning("Yes")
