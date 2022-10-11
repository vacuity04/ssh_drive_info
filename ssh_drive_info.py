from tkinter import *
import paramiko

root = Tk()  # calls the 'root' widget which is the main app window
root.title('SSH Drive Info')

drives = ['/dev/ada0', '/dev/ada1', '/dev/ada2', '/dev/ada3', '/dev/ada4', '/dev/ada5']
results = []


def open_ssh(host, user, passw):
    global results
    global entry_drive0
    global entry_drive1
    global entry_drive2
    global entry_drive3
    global entry_drive4
    global entry_drive5

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host,
                       port=22,
                       username=user,
                       password=passw)

    # Drive status commands cycled via for loop
    for drive in drives:
        stdin, stdout, stderr = ssh_client.exec_command(command=f'sudo smartctl -H {drive}', get_pty=True)
        stdin.write(passw+"\n")
        stdin.flush()

        if stdout.channel.recv_exit_status() == 0:
            # print(f'STDOUT: {stdout.read().decode("utf8")}')
            output = stdout.read().decode("utf8")
            # print(output)
            if output.find("PASSED") != -1:
                results.append("PASSED")
            elif output.find("FAILED!") != -1:
                results.append("FAILED!")
            else:
                results.append("ERROR")
        else:
            results.append(f'STDERR: {stderr.read().decode("utf8")}')

    entry_drive0.insert(0, results[0])
    entry_drive1.insert(0, results[1])
    entry_drive2.insert(0, results[2])
    entry_drive3.insert(0, results[3])
    entry_drive4.insert(0, results[4])
    entry_drive5.insert(0, results[5])

    stdin.close()
    stdout.close()
    stderr.close()

    ssh_client.close()


def fill_info():
    global entry_hostname
    global entry_username
    global entry_password

    entry_hostname.insert(0, "192.168.0.4")
    entry_username.insert(0, "(enter username)")
    entry_password.insert(0, "(enter password)")


frame_connection = LabelFrame(root, text="Connection", padx=10, pady=10)
frame_results = LabelFrame(root, text="Results", padx=10, pady=10)

label_hostname = Label(frame_connection, text="Enter hostname: ")
label_username = Label(frame_connection, text="Enter username: ")
label_password = Label(frame_connection, text="Enter password: ")

entry_hostname = Entry(frame_connection, width=30)
entry_username = Entry(frame_connection, width=30)
entry_password = Entry(frame_connection, width=30)

button_run = Button(root, text="Run", pady=20,
                    command=lambda: open_ssh(entry_hostname.get(), entry_username.get(), entry_password.get()))
button_fill = Button(root, text="Fill", pady=20, command=fill_info)

label_drive0 = Label(frame_results, text=drives[0])
label_drive1 = Label(frame_results, text=drives[1])
label_drive2 = Label(frame_results, text=drives[2])
label_drive3 = Label(frame_results, text=drives[3])
label_drive4 = Label(frame_results, text=drives[4])
label_drive5 = Label(frame_results, text=drives[5])

entry_drive0 = Entry(frame_results, width=30, bg="light gray")
entry_drive1 = Entry(frame_results, width=30, bg="light gray")
entry_drive2 = Entry(frame_results, width=30, bg="light gray")
entry_drive3 = Entry(frame_results, width=30, bg="light gray")
entry_drive4 = Entry(frame_results, width=30, bg="light gray")
entry_drive5 = Entry(frame_results, width=30, bg="light gray")

frame_connection.grid(row=0, column=0, padx=10, pady=10)
frame_results.grid(row=1, column=0, padx=10, pady=10)
label_hostname.grid(row=0, column=0)
label_username.grid(row=1, column=0)
label_password.grid(row=2, column=0)
entry_hostname.grid(row=0, column=1)
entry_username.grid(row=1, column=1)
entry_password.grid(row=2, column=1)
button_run.grid(row=0, column=2, padx=5)
button_fill.grid(row=0, column=3, padx=5)

label_drive0.grid(row=0, column=0)
label_drive1.grid(row=1, column=0)
label_drive2.grid(row=2, column=0)
label_drive3.grid(row=3, column=0)
label_drive4.grid(row=4, column=0)
label_drive5.grid(row=5, column=0)
entry_drive0.grid(row=0, column=1)
entry_drive1.grid(row=1, column=1)
entry_drive2.grid(row=2, column=1)
entry_drive3.grid(row=3, column=1)
entry_drive4.grid(row=4, column=1)
entry_drive5.grid(row=5, column=1)

root.mainloop()  # create the main loop that monitors for I/O in the window
