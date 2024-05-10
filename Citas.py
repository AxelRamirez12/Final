import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar

class ClinicaMedicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modulo de Citas - Clinica Medica")
        
        # Variables para almacenar datos
        self.nombres = tk.StringVar()
        self.apellidos = tk.StringVar()
        self.dpi = tk.StringVar()
        self.fecha_nacimiento = tk.StringVar()
        self.telefono = tk.StringVar()
        self.usuario = tk.StringVar()
        self.correo_electronico = tk.StringVar()
        self.contrasena = tk.StringVar()
        self.confirmar_contrasena = tk.StringVar()

        # Crear etiquetas y campos de entrada   
        tk.Label(root, text="Nombres:").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.nombres).grid(row=0, column=1)
        
        tk.Label(root, text="Apellidos:").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable=self.apellidos).grid(row=1, column=1)
        
        tk.Label(root, text="Numero de DPI (13 números):").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.dpi).grid(row=2, column=1)
        
        tk.Label(root, text="Fecha de nacimiento:").grid(row=3, column=0, sticky="e")
        tk.Entry(root, textvariable=self.fecha_nacimiento).grid(row=3, column=1)
        
        tk.Label(root, text="Telefono:").grid(row=4, column=0, sticky="e")
        tk.Entry(root, textvariable=self.telefono).grid(row=4, column=1)
        
        tk.Label(root, text="Nombre de usuario:").grid(row=5, column=0, sticky="e")
        tk.Entry(root, textvariable=self.usuario).grid(row=5, column=1)
        
        tk.Label(root, text="Correo electronico:").grid(row=6, column=0, sticky="e")
        tk.Entry(root, textvariable=self.correo_electronico).grid(row=6, column=1)
        
        tk.Label(root, text="Contraseña:").grid(row=7, column=0, sticky="e")
        tk.Entry(root, textvariable=self.contrasena, show="*").grid(row=7, column=1)
        
        tk.Label(root, text="Confirmar contraseña:").grid(row=8, column=0, sticky="e")
        tk.Entry(root, textvariable=self.confirmar_contrasena, show="*").grid(row=8, column=1)

        # Botón para guardar y mostrar datos
        tk.Button(root, text="Guardar", command=self.guardar_datos).grid(row=9, column=1, pady=10)

    def guardar_datos(self):
        # Obtener los valores ingresados por el usuario
        nombres = self.nombres.get()
        apellidos = self.apellidos.get()
        dpi = self.dpi.get()
        fecha_nacimiento = self.fecha_nacimiento.get()
        telefono = self.telefono.get()
        usuario = self.usuario.get()
        correo_electronico = self.correo_electronico.get()
        contrasena = self.contrasena.get()
        confirmar_contrasena = self.confirmar_contrasena.get()

        # Verificar que la contraseña coincida con la confirmación
        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Verificar si el DPI tiene 13 números
        if len(dpi) != 13 or not dpi.isdigit():
            messagebox.showerror("Error", "El número de DPI debe contener 13 números.")
            return

        # Guardar los datos en un archivo de texto
        with open("datos_pacientes.txt", "a") as file:
            file.write(f"Nombres: {nombres}\n")
            file.write(f"Apellidos: {apellidos}\n")
            file.write(f"DPI: {dpi}\n")
            file.write(f"Fecha de nacimiento: {fecha_nacimiento}\n")
            file.write(f"Telefono: {telefono}\n")
            file.write(f"Nombre de usuario: {usuario}\n")
            file.write(f"Correo electronico: {correo_electronico}\n")
            file.write("---------------------------------------------------\n")

        # Mostrar mensaje de éxito
        messagebox.showinfo("Datos Guardados", "Los datos han sido guardados exitosamente.")

        # Mostrar ventana para ingresar usuario y contraseña
        self.mostrar_ventana_login()

    def mostrar_ventana_login(self):
        usuario = simpledialog.askstring("Inicio de Sesión", "Ingrese su usuario:")
        contrasena = simpledialog.askstring("Inicio de Sesión", "Ingrese su contraseña:", show="*")

        # Aquí podrías agregar la lógica de verificación de usuario y contraseña
        if usuario == "admin" and contrasena == "1234":
            self.mostrar_calendario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def mostrar_calendario(self):
        top = tk.Toplevel(self.root)
        top.title("Seleccione una fecha")

        cal = Calendar(top, selectmode="day", year=2024, month=5, day=7)
        cal.pack(padx=20, pady=20)

        tk.Button(top, text="Seleccionar Fecha", command=lambda: self.verificar_disponibilidad(cal.get_date())).pack(pady=10)

    def verificar_disponibilidad(self, fecha):
        # Aquí agregarías la lógica para verificar si la fecha está disponible
        # Por ahora, simplemente mostraremos un mensaje de éxito
        messagebox.showinfo("Fecha Disponible", f"La fecha {fecha} está disponible para agendar cita.")

# Crear la ventana principal
root = tk.Tk()
app = ClinicaMedicaApp(root)
root.mainloop()


