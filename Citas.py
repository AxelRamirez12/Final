import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
import re

class ClinicaMedicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio")
        
        # Botón para iniciar sesión
        tk.Button(root, text="Ingresa usuario y contraseña", command=self.mostrar_ventana_login).pack(pady=10)
        
        # Botón para crear un nuevo usuario
        tk.Button(root, text="Crear usuario", command=self.mostrar_modulo_citas).pack(pady=10)

    def mostrar_ventana_login(self):
        usuario = simpledialog.askstring("Inicio de Sesion", "Ingrese su usuario:")
        contrasena = simpledialog.askstring("Inicio de Sesion", "Ingrese su contraseña:", show="*")

        # Aquí podrías agregar la lógica de verificación de usuario y contraseña
        if self.verificar_credenciales(usuario, contrasena):
            if usuario == "admin":
                self.mostrar_buscar_registros()
            else:
                self.mostrar_calendario()
        else:
            respuesta = messagebox.askyesno("Usuario no registrado", "¿Aún no tienes una cuenta? ¿Deseas registrarte?")
            if respuesta:
                self.mostrar_modulo_citas()

    def verificar_credenciales(self, usuario, contrasena):
        # Verificar las credenciales en el archivo de usuarios registrados
        if usuario == "admin" and contrasena == "admin123":
            return True
        else:
            with open("datos_pacientes.txt", "r") as file:
                lines = file.readlines()
                for i in range(0, len(lines), 9):
                    saved_user = lines[i + 5].split(":")[1].strip()
                    if saved_user == usuario:
                        saved_pass = lines[i + 7].split(":")[1].strip()
                        if saved_pass == contrasena:
                            return True
        return False

    def mostrar_modulo_citas(self):
        root = tk.Toplevel()
        app = ClinicaMedicaNuevoUsuario(root)

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

    def mostrar_buscar_registros(self):
        root = tk.Toplevel(self.root)
        root.title("Buscar/Eliminar Registros")

        tk.Label(root, text="Buscar/Eliminar por Nombres:").grid(row=0, column=0, sticky="e")
        self.entry_nombres = tk.Entry(root)
        self.entry_nombres.grid(row=0, column=1)
        
        tk.Label(root, text="Buscar/Eliminar por Apellidos:").grid(row=1, column=0, sticky="e")
        self.entry_apellidos = tk.Entry(root)
        self.entry_apellidos.grid(row=1, column=1)
        
        tk.Label(root, text="Buscar/Eliminar por DPI:").grid(row=2, column=0, sticky="e")
        self.entry_dpi = tk.Entry(root)
        self.entry_dpi.grid(row=2, column=1)

        tk.Button(root, text="Buscar", command=self.buscar_registros).grid(row=3, columnspan=2, pady=5)
        

    def buscar_registros(self):
        # Lógica para buscar los registros según los filtros de nombres, apellidos y DPI
        nombres = self.entry_nombres.get()
        apellidos = self.entry_apellidos.get()
        dpi = self.entry_dpi.get()

        # Verificar si los campos están vacíos
        if not nombres and not apellidos and not dpi:
            messagebox.showwarning("Campos Vacios", "Por favor, ingrese al menos un campo para buscar.")
            return

        with open("datos_pacientes.txt", "r") as file:
            lines = file.readlines()
            found = False
            for i in range(0, len(lines), 9):
                if i + 2 < len(lines):
                    saved_nombres = lines[i].split(":")[1].strip()
                    saved_apellidos = lines[i + 1].split(":")[1].strip()
                    saved_dpi = lines[i + 2].split(":")[1].strip()
                
                    if nombres.lower() in saved_nombres.lower() and apellidos.lower() in saved_apellidos.lower() and dpi.lower() in saved_dpi.lower():
                        found = True
                        datos_usuario = ""
                        for j in range(i, i + 9):
                            datos_usuario += lines[j]
                        messagebox.showinfo("Datos del Usuario", datos_usuario)
                        # Agregar la opción de eliminar el usuario
                        respuesta = messagebox.askyesno("Eliminar Usuario", "¿Desea eliminar este usuario?")
                        if respuesta:
                            self.eliminar_usuario(i)
            if not found:
                messagebox.showinfo("Usuario no encontrado", "No se encontraron usuarios con los filtros especificados.")

    def eliminar_usuario(self, index):
        # Eliminar el usuario del archivo
        with open("datos_pacientes.txt", "r") as file:
            lines = file.readlines()
        with open("datos_pacientes.txt", "w") as file:
            for i, line in enumerate(lines):
                if i < index or i >= index + 9:
                    file.write(line)
class ClinicaMedicaNuevoUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Modulo de Citas - Nuevo Usuario")
        
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
        
        tk.Label(root, text="Número de DPI (13 numeros):").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.dpi).grid(row=2, column=1)
        
        tk.Label(root, text="Fecha de nacimiento:").grid(row=3, column=0, sticky="e")
        tk.Entry(root, textvariable=self.fecha_nacimiento).grid(row=3, column=1)
        
        tk.Label(root, text="Telefono:").grid(row=4, column=0, sticky="e")
        tk.Entry(root, textvariable=self.telefono).grid(row=4, column=1)
        
        tk.Label(root, text="Nombre de usuario:").grid(row=5, column=0, sticky="e")
        tk.Entry(root, textvariable=self.usuario).grid(row=5, column=1)
        
        tk.Label(root, text="Correo electronico:").grid(row=6, column=0, sticky="e")
        tk.Entry(root, textvariable=self.correo_electronico).grid(row=6, column=1)
        
        tk.Label(root, text="Contrasena:").grid(row=7, column=0, sticky="e")
        tk.Entry(root, textvariable=self.contrasena, show="*").grid(row=7, column=1)
        
        tk.Label(root, text="Confirmar contrasena:").grid(row=8, column=0, sticky="e")
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

        # Validar que en las casillas de "Nombres" y "Apellidos" solo se puedan escribir letras
        if not re.match("^[A-Za-z ]+$", nombres) or not re.match("^[A-Za-z ]+$", apellidos):
            messagebox.showerror("Error", "Por favor, ingrese solo letras en los campos de nombres y apellidos.")
            return

        # Validar que en las casillas de "DPI" y  no se puedan escribir letras
        if not dpi.isdigit() :
            messagebox.showerror("Error", "Por favor, ingrese solo numeros en los campos de DPI ")
            return

        # Verificar que la contraseña coincida con la confirmación
        if contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contrasenas no coinciden.")
            return

        # Verificar si el DPI tiene 13 números
        if len(dpi) != 13:
            messagebox.showerror("Error", "El numero de DPI debe contener 13 números.")
            return

        # Verificar que cada usuario sea único
        with open("datos_pacientes.txt", "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 9):
                saved_user = lines[i + 5].split(":")[1].strip()
                if saved_user == usuario:
                    messagebox.showerror("Error", "El nombre de usuario ya esta en uso.")
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
            file.write(f"Contrasena: {contrasena}\n")  # Guardar la contraseña en el archivo
            file.write("---------------------------------------------------\n")

        # Mostrar mensaje de éxito
        messagebox.showinfo("Datos Guardados", "Los datos han sido guardados exitosamente.")

        # Cerrar la ventana después de guardar los datos
        self.root.destroy()

# Crear la ventana principal
root = tk.Tk()
app = ClinicaMedicaApp(root)
root.mainloop()


