from kitano.bash.termux import ShellRun

def test_shell_termux():
    sr = ShellRun()

    sr.prt = True

    print('android' in sr.checkLine('uname -a'))
    sr.runLine('''apt update
    apt list''')

