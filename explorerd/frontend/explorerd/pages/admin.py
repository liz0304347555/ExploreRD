import reflex as rx
from typing import List, Dict, Any

# ==========================================
# 1. ESTADO DE LA ADMINISTRACIÓN (AdminState)
# ==========================================
class AdminState(rx.State):
    # Listas de datos principales
    reservas: List[Dict[str, Any]] = [
        {"id": 7, "cliente": "alejandro_jimenez", "email": "alejandroy134@gmail.com", "telefono": "+1 809 555 6669", "fecha": "2026-06-25", "personas": 4, "metodo": "tarjeta", "notas": ""},
        {"id": 6, "cliente": "alejandro_jimenez", "email": "alejandroy134@gmail.com", "telefono": "+1 809 555 8889", "fecha": "2026-06-25", "personas": 4, "metodo": "tarjeta", "notas": ""},
        {"id": 5, "cliente": "alejandro_jimenez", "email": "alejandroy134@gmail.com", "telefono": "+1 809 555 6669", "fecha": "2026-06-25", "personas": 4, "metodo": "tarjeta", "notas": ""},
        {"id": 4, "cliente": "alejandro_jimenez", "email": "alejandroy134@gmail.com", "telefono": "+1 809 555 8889", "fecha": "2026-06-25", "personas": 4, "metodo": "tarjeta", "notas": ""},
        {"id": 3, "cliente": "alejandro_jimenez", "email": "alejandroy134@gmail.com", "telefono": "+1 809 555 6669", "fecha": "2026-06-25", "personas": 4, "metodo": "tarjeta", "notas": ""},
        {"id": 2, "cliente": "massiel torres", "email": "massiel06@gmail.com", "telefono": "+1 809 333 6663", "fecha": "2026-06-08", "personas": 2, "metodo": "tarjeta", "notas": ""},
        {"id": 1, "cliente": "alejandro_jimenez", "email": "alejandroalex@gmail.com", "telefono": "+1 829 888 9009", "fecha": "2026-05-31", "personas": 2, "metodo": "tarjeta", "notas": ""}
    ]
    mensajes: List[Dict[str, Any]] = []
    ofertas: List[Dict[str, Any]] = [
        {"id": 1, "titulo": "Aventura en Jarabacoa", "destino": "Jarabacoa", "duracion": "3 días", "precio": 2800, "imagen": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9"},
        {"id": 2, "titulo": "Paraíso en Bahía de las Águilas", "destino": "Pedernales", "duracion": "2 días", "precio": 4500, "imagen": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"},
        {"id": 3, "titulo": "Escape a Las Terrenas", "destino": "Samaná", "duracion": "4 días", "precio": 3900, "imagen": "https://images.unsplash.com/photo-1540206351-d6465b3ac5c1"}
    ]
    
    # Control de la pestaña activa en el panel
    tab_actual: str = "reservas"
    
    # Variables de control del formulario de edición/creación
    form_titulo: str = ""
    form_destino: str = ""
    form_duracion: str = ""
    form_precio: str = ""
    form_imagen: str = ""
    dialog_abierto: bool = False

    # SETTERS MANUALES BLINDADOS (Evitan fallos de AttributeError al escribir en inputs)
    def set_form_titulo(self, valor: str): self.form_titulo = valor
    def set_form_destino(self, valor: str): self.form_destino = valor
    def set_form_duracion(self, valor: str): self.form_duracion = valor
    def set_form_precio(self, valor: str): self.form_precio = valor
    def set_form_imagen(self, valor: str): self.form_imagen = valor
    def set_dialog_abierto(self, abierto: bool): self.dialog_abierto = abierto

    def cambiar_tab(self, tab: str):
        self.tab_actual = tab

    def cargar_datos(self):
        """Método ejecutado al cargar la página (Sustituye al on_mount problemático)"""
        pass

    def abrir_modal_editar(self, oferta: Dict[str, Any]):
        self.form_titulo = oferta["titulo"]
        self.form_destino = oferta["destino"]
        self.form_duracion = oferta["duracion"]
        self.form_precio = str(oferta["precio"])
        self.form_imagen = oferta["imagen"]
        self.dialog_abierto = True

    def guardar_oferta(self):
        # Lógica para guardar o simular la actualización
        self.dialog_abierto = False

    def eliminar_oferta(self, id_oferta: int):
        self.ofertas = [o for o in self.ofertas if o["id"] != id_oferta]


# ==========================================
# 2. COMPONENTES DE DISEÑO AUXILIARES
# ==========================================
def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading("ExploreRD", size="6", color="#1a5c3a", font_weight="bold"),
        rx.spacer(),
        rx.hstack(
            rx.link("Inicio", href="/", color="#2d3748"),
            rx.link("Destinos", href="/destinos", color="#2d3748"),
            rx.button("Reservar", color_scheme="green", variant="solid"),
            spacing="4",
        ),
        padding="1rem 2rem",
        background="white",
        width="100%",
        border_bottom="1px solid #e2e8f0"
    )

def footer() -> rx.Component:
    return rx.box(
        rx.center(
            rx.text("© 2026 ExploreRD. Todos los derechos reservados.", color="#a0aec0", font_size="0.85rem"),
        ),
        background="#1a202c",
        padding="2rem",
        width="100%",
    )

def tarjeta_metrica(titulo: str, valor: str, icono: str, color_linea: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(titulo.upper(), font_size="0.75rem", font_weight="700", color="#718096"),
                rx.text(valor, font_size="2rem", font_weight="800", color="#1a202c"),
                align_items="start",
                spacing="1"
            ),
            rx.spacer(),
            rx.text(icono, font_size="2rem"),
            align_items="center",
            width="100%"
        ),
        padding="1.5rem",
        background="white",
        border_radius="12px",
        border_left=f"4px solid {color_linea}",
        box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
        width="100%"
    )

def fila_reserva(reserva: rx.Var) -> rx.Component:
    return rx.table.row(
        rx.table.cell(reserva["id"].to_string()),
        rx.table.cell(reserva["cliente"]),
        rx.table.cell(reserva["email"]),
        rx.table.cell(reserva["telefono"]),
        rx.table.cell(reserva["fecha"]),
        rx.table.cell(reserva["personas"].to_string()),
        rx.table.cell(rx.badge(reserva["metodo"], color_scheme="green", variant="soft")),
        rx.table.cell(reserva["notas"]),
        rx.table.cell(
            rx.button("🗑️", size="1", color_scheme="red", variant="ghost")
        ),
    )

def tarjeta_oferta(oferta: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            # Solución al error de strings: rx.image nativo sin concatenaciones complejas
            rx.image(
                src=oferta["imagen"],
                width="100%",
                height="140px",
                object_fit="cover",
                border_radius="12px 12px 0 0",
            ),
            rx.vstack(
                rx.text(oferta["titulo"], font_weight="700", font_size="1.1rem", color="#1a202c"),
                rx.hstack(
                    rx.badge(oferta["destino"], color_scheme="blue", variant="surface"),
                    rx.badge(oferta["duracion"], color_scheme="orange", variant="surface"),
                ),
                rx.hstack(
                    rx.text("RD$ ", font_size="0.85rem", color="#718096", font_weight="600"),
                    rx.text(oferta["precio"].to_string(), font_size="1.2rem", font_weight="800", color="#1a5c3a"),
                    align_items="baseline"
                ),
                rx.divider(margin_y="0.2rem"),
                rx.hstack(
                    rx.button("✏️ Editar", size="1", color_scheme="blue", variant="soft", cursor="pointer", on_click=lambda: AdminState.abrir_modal_editar(oferta)),
                    rx.button("🗑️ Eliminar", size="1", color_scheme="red", variant="soft", cursor="pointer", on_click=lambda: AdminState.eliminar_oferta(oferta["id"].to(int))),
                    justify="between",
                    width="100%",
                    padding_top="0.2rem"
                ),
                width="100%",
                padding="1rem",
                spacing="2",
                align_items="start",
            ),
            spacing="0",
        ),
        border="1px solid #e2e8f0",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 6px -1px rgba(0,0,0,0.02)",
        width="100%"
    )


# ==========================================
# 3. INTERFAZ PRINCIPAL DEL PANEL (PÁGINA)
# ==========================================
@rx.page(route="/admin", title="Panel de Administración - ExploreRD", on_load=AdminState.cargar_datos)
def admin() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            # Banner de Encabezado
            rx.box(
                rx.vstack(
                    rx.badge("🔒 Panel de Control Seguro", color_scheme="yellow", variant="surface", margin_bottom="0.5rem"),
                    rx.heading("Administración Global ExploreRD", size="8", color="white", font_weight="bold", text_align="center"),
                    rx.text("Gestiona de forma cómoda reservas, mensajes de clientes y ofertas turísticas activas en tiempo real.", color="#e2e8f0", text_align="center"),
                    spacing="2",
                    align_items="center",
                    justify_content="center",
                    padding="3rem 2rem",
                ),
                background="linear-gradient(135deg, #1a5c3a 0%, #14452b 100%)",
                width="100%",
            ),
            
            # Contenido Central Ajustado
            rx.vstack(
                # Fila de Métricas (Mapeo Responsivo Corregido)
                rx.grid(
                    tarjeta_metrica("Total Reservas", AdminState.reservas.length().to_string(), "📅", "#3182ce"),
                    tarjeta_metrica("Mensajes Recibidos", AdminState.mensajes.length().to_string(), "📩", "#805ad5"),
                    tarjeta_metrica("Ofertas Destacadas", AdminState.ofertas.length().to_string(), "🗺️", "#dd6b20"),
                    columns={"sm": "1", "md": "3"},
                    spacing="4",
                    width="100%",
                    margin_bottom="2rem"
                ),
                
                # Selectores de Pestañas
                rx.hstack(
                    rx.button("📅 Lista de Reservas", color_scheme="green", variant=rx.cond(AdminState.tab_actual == "reservas", "solid", "outline"), on_click=lambda: AdminState.cambiar_tab("reservas")),
                    rx.button("📩 Mensajes de Contacto", color_scheme="purple", variant=rx.cond(AdminState.tab_actual == "mensajes", "solid", "outline"), on_click=lambda: AdminState.cambiar_tab("mensajes")),
                    rx.button("🗺️ Ofertas Activas", color_scheme="orange", variant=rx.cond(AdminState.tab_actual == "ofertas", "solid", "outline"), on_click=lambda: AdminState.cambiar_tab("ofertas")),
                    spacing="3",
                    width="100%",
                    justify_content="start",
                    margin_bottom="1.5rem"
                ),
                
                # Tablas y Vistas Dinámicas
                rx.cond(
                    AdminState.tab_actual == "reservas",
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Cliente"),
                                    rx.table.column_header_cell("Email"),
                                    rx.table.column_header_cell("Teléfono"),
                                    rx.table.column_header_cell("Fecha Entrada"),
                                    rx.table.column_header_cell("Pers."),
                                    rx.table.column_header_cell("Método"),
                                    rx.table.column_header_cell("Notas Calculadas"),
                                    rx.table.column_header_cell("Acción"),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(AdminState.reservas, fila_reserva)
                            ),
                            variant="surface",
                            width="100%"
                        ),
                        width="100%"
                    )
                ),
                
                rx.cond(
                    AdminState.tab_actual == "ofertas",
                    rx.grid(
                        rx.foreach(AdminState.ofertas, tarjeta_oferta),
                        columns={"sm": "1", "md": "2", "lg": "3"},
                        spacing="4",
                        width="100%"
                    )
                ),
                
                max_width="1200px",
                width="100%",
                padding="2rem",
                spacing="4"
            ),
            spacing="0",
            width="100%"
        ),
        
        # Ventana Emergente de Edición (Modal Dialog)
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Editar Oferta Turística"),
                rx.vstack(
                    rx.text("Título de la Oferta", font_weight="600"),
                    rx.input(value=AdminState.form_titulo, on_change=AdminState.set_form_titulo, width="100%"),
                    rx.text("Destino", font_weight="600"),
                    rx.input(value=AdminState.form_destino, on_change=AdminState.set_form_destino, width="100%"),
                    rx.text("Precio (RD$)", font_weight="600"),
                    rx.input(value=AdminState.form_precio, on_change=AdminState.set_form_precio, width="100%"),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                        rx.button("Guardar Cambios", color_scheme="blue", on_click=AdminState.guardar_oferta),
                        justify="end",
                        width="100%",
                        padding_top="1rem"
                    ),
                    align_items="start",
                    spacing="3"
                )
            ),
            open=AdminState.dialog_abierto,
            on_open_change=AdminState.set_dialog_abierto
        ),
        
        footer(),
        background="#f8fafc",
        font_family="system-ui, -apple-system, sans-serif",
        min_height="100vh"
    )