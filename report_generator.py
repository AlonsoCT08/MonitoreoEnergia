# report_generator.py
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class ReportGenerator:
    def set_summary(self, test_records=None):
        # Recibe únicamente la lista de registros
        self.test_records = test_records if test_records else []

    def generate_pdf(self, filename="reporte_consumo.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Reporte de Consumo de Energía", styles['Title']))
        elements.append(Spacer(1, 12))

        if self.test_records:
            # Encabezados de tabla con solo los campos solicitados
            data = [
                ["Fecha y Hora", "Tiempo (s)", "Voltaje (V)",
                 "Corriente Min (A)", "Corriente Max (A)", "Corriente Prom (A)",
                 "Energía (mWh)", "N° de Muestras"]
            ]

            for r in self.test_records:
                data.append([
                    r["fecha_hora"],
                    f"{r['tiempo_segundos']:.0f}",
                    f"{r['voltage']:.6f}",
                    f"{r['corriente_min']:.6f}",
                    f"{r['corriente_max']:.6f}",
                    f"{r['corriente_prom']:.6f}",
                    f"{r['energia_mwh']:.4f}",
                    str(r["num_muestras"])
                ])

            table = Table(data, colWidths=[120, 60, 70, 80, 80, 90, 90, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1976D2")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ]))

            elements.append(Paragraph("Resultados de Pruebas (Checkpoints)", styles['Heading2']))
            elements.append(Spacer(1, 12))
            elements.append(table)

        doc.build(elements)
        print(f"Reporte PDF generado: {filename}")

