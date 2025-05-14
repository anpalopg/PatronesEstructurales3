from abc import ABC, abstractmethod

# === 1. Adapter: Integrar API externa de pago con interfaz interna ===
class ExternalPaymentAPI:
    def send_payment(self, amount):
        print(f"[API Externa] Pago enviado por ${amount}")

class PaymentInterface(ABC):
    @abstractmethod
    def pay(self, amount): pass

class PaymentAdapter(PaymentInterface):
    def __init__(self, external_api):
        self.external_api = external_api

    def pay(self, amount):
        print("[Adapter] Adaptando interfaz interna a API externa...")
        self.external_api.send_payment(amount)

# === 2. Facade: Simplificar el módulo de facturación ===
class InvoiceGenerator:
    def generate(self, user, amount):
        print(f"[Factura] Generando factura para {user} por ${amount}")

class Database:
    def save_invoice(self, user, amount):
        print(f"[BD] Guardando factura de {user} por ${amount}")

class MessageSender:
    def send(self, message):
        print(f"[Mensaje] Enviado: {message}")

class BillingFacade:
    def __init__(self):
        self.generator = InvoiceGenerator()
        self.database = Database()
        self.sender = MessageSender()

    def process_billing(self, user, amount):
        print("[Fachada] Procesando facturación...")
        self.generator.generate(user, amount)
        self.database.save_invoice(user, amount)
        self.sender.send(f"Factura generada para {user} por ${amount}")

# === 3. Decorator: Envío de mensajes con funcionalidades extendidas ===
class MessageComponent(ABC):
    @abstractmethod
    def send(self, message): pass

class BasicMessage(MessageComponent):
    def send(self, message):
        print(f"[Mensaje] {message}")

class EncryptionDecorator(MessageComponent):
    def __init__(self, component):
        self.component = component

    def send(self, message):
        encrypted = f"<encriptado>{message[::-1]}</encriptado>"
        self.component.send(encrypted)

class CompressionDecorator(MessageComponent):
    def __init__(self, component):
        self.component = component

    def send(self, message):
        compressed = f"<comprimido>{message[:10]}...</comprimido>"
        self.component.send(compressed)

# === 4. Composite: Interfaz gráfica jerárquica ===
class UIComponent(ABC):
    @abstractmethod
    def render(self, depth=0): pass

class Button(UIComponent):
    def __init__(self, label): self.label = label
    def render(self, depth=0): print(" " * depth + f"[Botón: {self.label}]")

class TextField(UIComponent):
    def __init__(self, name): self.name = name
    def render(self, depth=0): print(" " * depth + f"[Campo de Texto: {self.name}]")

class Panel(UIComponent):
    def __init__(self):
        self.children = []

    def add(self, component): self.children.append(component)

    def render(self, depth=0):
        print(" " * depth + "[Panel]")
        for c in self.children:
            c.render(depth + 2)

# === 5. Proxy: Control de acceso a base de datos ===
class RealDatabase:
    def read(self): print("[BD] Leyendo datos...")
    def write(self): print("[BD] Escribiendo datos...")

class DatabaseProxy:
    def __init__(self, user_type):
        self.user_type = user_type
        self.database = RealDatabase()

    def read(self):
        print(f"[Proxy] Usuario '{self.user_type}' accediendo a lectura.")
        self.database.read()

    def write(self):
        if self.user_type == "admin":
            print(f"[Proxy] Usuario '{self.user_type}' escribiendo...")
            self.database.write()
        else:
            print("[Proxy] Acceso denegado para escritura.")

# === Prueba del sistema unificado ===
if __name__ == "__main__":
    print("\n--- Pago con Adapter ---")
    external_api = ExternalPaymentAPI()
    payment = PaymentAdapter(external_api)
    payment.pay(100)

    print("\n--- Facturación con Facade ---")
    facade = BillingFacade()
    facade.process_billing("Alice", 100)

    print("\n--- Envío de mensajes con Decorators ---")
    message = BasicMessage()
    encrypted = EncryptionDecorator(message)
    compressed = CompressionDecorator(encrypted)
    compressed.send("Factura lista y enviada correctamente")

    print("\n--- Interfaz gráfica con Composite ---")
    main_panel = Panel()
    main_panel.add(Button("Pagar"))
    sub_panel = Panel()
    sub_panel.add(TextField("Nombre"))
    sub_panel.add(TextField("Correo"))
    main_panel.add(sub_panel)
    main_panel.render()

    print("\n--- Acceso a base de datos con Proxy ---")
    guest_db = DatabaseProxy("invitado")
    admin_db = DatabaseProxy("admin")
    guest_db.read()
    guest_db.write()
    admin_db.write()
