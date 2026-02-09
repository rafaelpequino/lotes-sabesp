from PIL import Image, ImageDraw
import os

# Criar ícone profissional
size = 256
image = Image.new('RGB', (size, size), color='#2C3E50')
draw = ImageDraw.Draw(image)

# Fundo gradiente simulado
for i in range(size):
    color_value = int(45 + (52 - 45) * (i / size))
    draw.line([(0, i), (size, i)], fill=(color_value, 62, 80))

# Desenhar um documento/arquivo
doc_x = 50
doc_y = 60
doc_width = 156
doc_height = 136

# Corpo do documento
draw.rectangle([doc_x, doc_y, doc_x + doc_width, doc_y + doc_height], fill='#ECF0F1', outline='#3498DB', width=3)

# Linhas do documento
for line_y in range(doc_y + 30, doc_y + doc_height - 20, 20):
    draw.line([(doc_x + 15, line_y), (doc_x + doc_width - 15, line_y)], fill='#BDC3C7', width=2)

# Ícone de cópia (seta)
arrow_x = doc_x + doc_width + 10
arrow_y = doc_y + 40
draw.polygon([(arrow_x, arrow_y), (arrow_x + 30, arrow_y + 15), (arrow_x, arrow_y + 30)], fill='#27AE60')

# Salvar ícone
icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.ico')
image.save(icon_path)
print(f"Ícone criado: {icon_path}")


