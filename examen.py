
# main.py
# Ecommerce CLI con POO y roles - Módulo 4
 
 
import datetime
 
 
# ── Excepciones personalizadas ────────────────────────────────────────────────
 
class ProductoNoEncontradoError(Exception):
    pass
 
class CantidadInvalidaError(Exception):
    pass
 
 
# ── Clases principales ────────────────────────────────────────────────────────
 
class Producto:
    def __init__(self, id_producto, nombre, categoria, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
 
    def __str__(self):
        return f"[{self.id_producto}] {self.nombre} | {self.categoria} | ${self.precio:.2f}"
 
 
class Catalogo:
    """Contiene una colección de productos (composición)."""
 
    def __init__(self):
        self.productos = []
        # Cargamos algunos productos de ejemplo al inicio
        self.productos.append(Producto("P001", "oro 14", "14", 749990))
        self.productos.append(Producto("P002", "oro 16", "16", 34990))
        self.productos.append(Producto("P003", "oro 18", "18", 259990))
        self.productos.append(Producto("P004", "oro 22", "22", 89990))
        self.productos.append(Producto("P005", "plata", "Audio", 79990))
 
    def buscar_por_id(self, id_producto):
        for p in self.productos:
            if p.id_producto == id_producto:
                return p
        raise ProductoNoEncontradoError(f"No existe producto con ID '{id_producto}'")
 
    def listar(self):
        if not self.productos:
            print("El catálogo está vacío.")
            return
        print(f"\n{'ID':<8} {'Nombre':<25} {'Categoría':<15} {'Precio':>10}")
        print("-" * 62)
        for p in self.productos:
            print(f"{p.id_producto:<8} {p.nombre:<25} {p.categoria:<15} ${p.precio:>9.2f}")
        print()
 
    def guardar_en_archivo(self):
        try:
            with open("catalogo.txt", "w", encoding="utf-8") as f:
                for p in self.productos:
                    f.write(f"{p.id_producto},{p.nombre},{p.categoria},{p.precio}\n")
            print("Catálogo guardado en 'catalogo.txt'.")
        except OSError as e:
            print(f"Error al guardar el archivo: {e}")
 
 
class Carrito:
    """Contiene los productos que el cliente quiere comprar (composición)."""
 
    def __init__(self):
        self.items = []  # cada ítem es una tupla (producto, cantidad)
 
    def agregar(self, producto, cantidad):
        if cantidad <= 0:
            raise CantidadInvalidaError(f"La cantidad debe ser mayor a 0, recibiste: {cantidad}")
        self.items.append((producto, cantidad))
        print(f"  Agregado: {cantidad}x {producto.nombre}")
 
    def ver(self):
        if not self.items:
            print("El carrito está vacío.")
            return
        print(f"\n{'Producto':<25} {'Cant':>5} {'P.Unit':>10} {'Subtotal':>10}")
        print("-" * 54)
        for producto, cantidad in self.items:
            subtotal = producto.precio * cantidad
            print(f"{producto.nombre:<25} {cantidad:>5} ${producto.precio:>9.2f} ${subtotal:>9.2f}")
        print("-" * 54)
        print(f"{'TOTAL':>42} ${self.calcular_total():>9.2f}\n")
 
    def calcular_total(self):
        return sum(p.precio * c for p, c in self.items)
 
    def vaciar(self):
        self.items = []
 
 
# ── Usuarios (herencia) ───────────────────────────────────────────────────────
 
class Usuario:
    """Clase base para Admin y Cliente."""
 
    def __init__(self, nombre, catalogo):
        self.nombre = nombre
        self.catalogo = catalogo
 
    def mostrar_menu(self):
        raise NotImplementedError("Cada subclase debe definir su menú.")
 
 
class Admin(Usuario):
    """Hereda de Usuario. Gestiona el catálogo de productos."""
 
    def mostrar_menu(self):
        while True:
            print(f"\n=== MENÚ ADMIN ({self.nombre}) ===")
            print("1. Listar productos")
            print("2. Crear producto")
            print("3. Eliminar producto")
            print("4. Guardar catálogo en archivo")
            print("0. Salir")
 
            opcion = input("Opción: ").strip()
 
            if opcion == "1":
                self.catalogo.listar()
 
            elif opcion == "2":
                id_producto = input("ID del producto: ").strip()
                nombre = input("Nombre: ").strip()
                categoria = input("Categoría: ").strip()
                try:
                    precio = float(input("Precio: ").strip())
                    nuevo = Producto(id_producto, nombre, categoria, precio)
                    self.catalogo.productos.append(nuevo)
                    print(f"Producto '{nombre}' creado.")
                except ValueError:
                    print("Error: el precio debe ser un número.")
 
            elif opcion == "3":
                id_producto = input("ID del producto a eliminar: ").strip()
                try:
                    producto = self.catalogo.buscar_por_id(id_producto)
                    self.catalogo.productos.remove(producto)
                    print(f"Producto '{producto.nombre}' eliminado.")
                except ProductoNoEncontradoError as e:
                    print(f"Error: {e}")
 
            elif opcion == "4":
                self.catalogo.guardar_en_archivo()
 
            elif opcion == "0":
                print("Cerrando sesión de Admin.")
                break
            else:
                print("Opción inválida.")
 
 
class Cliente(Usuario):
    """Hereda de Usuario. Navega el catálogo y realiza compras."""
 
    def __init__(self, nombre, catalogo):
        super().__init__(nombre, catalogo)
        self.carrito = Carrito()  # composición: el cliente tiene un carrito
 
    def mostrar_menu(self):
        while True:
            print(f"\n=== MENÚ CLIENTE ({self.nombre}) ===")
            print("1. Ver catálogo")
            print("2. Buscar producto por nombre o categoría")
            print("3. Agregar producto al carrito")
            print("4. Ver carrito")
            print("5. Confirmar compra")
            print("0. Salir")
 
            opcion = input("Opción: ").strip()
 
            if opcion == "1":
                self.catalogo.listar()
 
            elif opcion == "2":
                texto = input("Buscar: ").strip().lower()
                resultados = [p for p in self.catalogo.productos
                              if texto in p.nombre.lower() or texto in p.categoria.lower()]
                if resultados:
                    for p in resultados:
                        print(f"  {p}")
                else:
                    print("Sin resultados.")
 
            elif opcion == "3":
                self.catalogo.listar()
                id_producto = input("ID del producto: ").strip()
                try:
                    producto = self.catalogo.buscar_por_id(id_producto)
                    cantidad = int(input("Cantidad: ").strip())
                    self.carrito.agregar(producto, cantidad)
                except ProductoNoEncontradoError as e:
                    print(f"Error: {e}")
                except CantidadInvalidaError as e:
                    print(f"Error: {e}")
                except ValueError:
                    print("Error: la cantidad debe ser un número entero.")
 
            elif opcion == "4":
                self.carrito.ver()
 
            elif opcion == "5":
                if not self.carrito.items:
                    print("No puedes confirmar la compra: el carrito está vacío.")
                else:
                    self.carrito.ver()
                    confirmar = input("¿Confirmar compra? (s/n): ").strip().lower()
                    if confirmar == "s":
                        self._registrar_orden()
                        self.carrito.vaciar()
                        print("¡Compra confirmada!")
 
            elif opcion == "0":
                print("Cerrando sesión.")
                break
            else:
                print("Opción inválida.")
 
    def _registrar_orden(self):
        """Guarda la orden en un archivo de texto."""
        try:
            with open("ordenes.txt", "a", encoding="utf-8") as f:
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n--- Orden de {self.nombre} | {fecha} ---\n")
                for producto, cantidad in self.carrito.items:
                    subtotal = producto.precio * cantidad
                    f.write(f"  {producto.nombre} x{cantidad} = ${subtotal:.2f}\n")
                f.write(f"  TOTAL: ${self.carrito.calcular_total():.2f}\n")
            print("Orden registrada en 'ordenes.txt'.")
        except OSError as e:
            print(f"Error al guardar la orden: {e}")
        finally:
            print("Proceso de compra finalizado.")
 
 
# ── Inicio del programa ───────────────────────────────────────────────────────
 
def main():
    catalogo = Catalogo()
 
    print("=== BIENVENIDO AL ECOMMERCE ===")
    print("1. Ingresar como ADMIN")
    print("2. Ingresar como CLIENTE")
 
    rol = input("¿Qué rol eres? (1/2): ").strip()
    nombre = input("Tu nombre: ").strip()
 
    if rol == "1":
        usuario = Admin(nombre, catalogo)
    elif rol == "2":
        usuario = Cliente(nombre, catalogo)
    else:
        print("Rol inválido. Cerrando programa.")
        return
 
    usuario.mostrar_menu()
 
 
if __name__ == "__main__":
    main()