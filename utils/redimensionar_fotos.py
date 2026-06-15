from PIL import Image
from pathlib import Path

pasta = Path("assets/avatars")

for foto in pasta.glob("*.jpg"):
    img = Image.open(foto)
    img = img.resize((200, 200))

    novo_nome = foto.stem + ".png"
    img.save(pasta / novo_nome, "PNG")

    print(f"✅ {foto.name} -> {novo_nome}")