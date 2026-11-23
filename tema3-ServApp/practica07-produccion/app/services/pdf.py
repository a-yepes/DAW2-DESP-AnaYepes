from fpdf import FPDF


def texto_pdf(texto):
    """Las fuentes básicas de PDF solo admiten caracteres latinos (latin-1):
    quitamos los emojis y símbolos especiales para que no den error."""
    return str(texto).encode("latin-1", "ignore").decode("latin-1")


def certificado_capsula(c, autor):
    """Genera el PDF de una cápsula y devuelve sus bytes.
    Si está abierta incluye el mensaje; si está sellada, solo el certificado."""
    pdf = FPDF()
    pdf.set_margins(15, 15)                           # márgenes de 15 mm
    pdf.add_page()

    # Franja superior de color con el nombre de la app
    pdf.set_fill_color(36, 28, 79)                    # violeta (el --tarjeta del CSS)
    pdf.rect(0, 0, 210, 30, "F")                      # A4 mide 210 mm de ancho
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 10)
    pdf.cell(0, 10, texto_pdf("TimeFlies · Cápsulas del tiempo"))

    # Título del documento
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(15, 45)
    pdf.set_font("Helvetica", "B", 18)
    titulo = "Carta abierta del pasado" if c["abierta"] else "Certificado de cápsula sellada"
    pdf.cell(0, 10, texto_pdf(titulo), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Datos de la cápsula (etiqueta en negrita + valor)
    datos = [
        ("Título", c["titulo"]),
        ("Autor/a", autor),
        ("Sellada el", c["creado_en"].strftime("%d/%m/%Y %H:%M")),
        ("Se abre el", c["fecha_apertura"].strftime("%d/%m/%Y %H:%M")),
        ("Estado", "Abierta" if c["abierta"] else "Sellada"),
    ]
    for etiqueta, valor in datos:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(40, 8, texto_pdf(etiqueta + ":"))
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, texto_pdf(valor), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    if c["abierta"]:
        pdf.set_font("Times", "I", 13)
        pdf.multi_cell(0, 7, texto_pdf(c["mensaje"]))   # multi_cell: texto largo con saltos de línea
    else:
        pdf.set_font("Helvetica", "I", 12)
        pdf.multi_cell(0, 7, texto_pdf("El contenido de esta cápsula permanece sellado en la base de datos "
                                       "y no podrá leerse hasta su fecha de apertura."))

    return bytes(pdf.output())