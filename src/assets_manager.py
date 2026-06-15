"""Módulo: assets_manager.py"""
# Em desenvolvimento...
# src/assets_manager.py
"""
Gerenciador de Assets Visuais
- Bandeiras das 48 seleções
- Avatares personalizados dos competidores
"""

import os
import json
import base64
from pathlib import Path
from io import BytesIO
from typing import Dict, Optional, Tuple
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importa PIL para gerar avatares
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow não instalado. Avatares serão gerados sem imagem.")
    print("   Instale com: pip install Pillow")


class AssetsManager:
    """
    Gerencia bandeiras, avatares e elementos visuais

    Uso:
        assets = AssetsManager()

        # Bandeira
        flag = assets.get_flag_base64('Brasil')

        # Avatar
        avatar = assets.create_avatar('João Silva')

        # Info do competidor
        info = assets.get_competitor_info('João')
    """

    def __init__(self):
        """Inicializa o gerenciador de assets"""
        self.assets_path = Path("assets")
        self.flags_path = self.assets_path / "flags"
        self.avatars_path = self.assets_path / "avatars"

        # Cria diretórios se não existirem
        self.flags_path.mkdir(parents=True, exist_ok=True)
        self.avatars_path.mkdir(parents=True, exist_ok=True)

        # Mapeamento de países para códigos de bandeira
        self.country_flags = {
            # Grupo A
            'México': 'mx', 'África do Sul': 'za', 'Coreia do Sul': 'kr', 'República Tcheca': 'cz',
            # Grupo B
            'Canadá': 'ca', 'Bósnia-Herzegovina': 'ba', 'Catar': 'qa', 'Suíça': 'ch',
            # Grupo C
            'Brasil': 'br', 'Marrocos': 'ma', 'Haiti': 'ht', 'Escócia': 'gb-sct',
            # Grupo D
            'Estados Unidos': 'us', 'Paraguai': 'py', 'Austrália': 'au', 'Turquia': 'tr',
            # Grupo E
            'Alemanha': 'de', 'Curaçao': 'cw', 'Costa do Marfim': 'ci', 'Equador': 'ec',
            # Grupo F
            'Holanda': 'nl', 'Japão': 'jp', 'Suécia': 'se', 'Tunísia': 'tn',
            # Grupo G
            'Bélgica': 'be', 'Egito': 'eg', 'Irã': 'ir', 'Nova Zelândia': 'nz',
            # Grupo H
            'Espanha': 'es', 'Cabo Verde': 'cv', 'Arábia Saudita': 'sa', 'Uruguai': 'uy',
            # Grupo I
            'França': 'fr', 'Senegal': 'sn', 'Iraque': 'iq', 'Noruega': 'no',
            # Grupo J
            'Argentina': 'ar', 'Argélia': 'dz', 'Áustria': 'at', 'Jordânia': 'jo',
            # Grupo K
            'Portugal': 'pt', 'RD Congo': 'cd', 'Uzbequistão': 'uz', 'Colômbia': 'co',
            # Grupo L
            'Inglaterra': 'gb-eng', 'Croácia': 'hr', 'Gana': 'gh', 'Panamá': 'pa',
        }

        # Paleta de cores para avatares
        self.avatar_colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
            '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2'
        ]

        # Carrega configuração dos competidores
        self.competitors_config = self.load_competitors_config()

    def load_competitors_config(self) -> Dict:
        """
        Carrega configuração dos competidores do JSON

        Returns:
            Dicionário com configuração
        """
        config_file = self.assets_path / "competitors.json"

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Erro ao carregar configuração: {e}")

        # Configuração padrão
        return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Retorna configuração padrão dos competidores"""
        return {
            "competidores": {
                "competidor_1": {
                    "nome": "Competidor 1",
                    "apelido": "Comp1",
                    "cor": "#FF6B6B",
                    "emoji": "⚽",
                    "ativo": True
                },
                "competidor_2": {
                    "nome": "Competidor 2",
                    "apelido": "Comp2",
                    "cor": "#4ECDC4",
                    "emoji": "🌟",
                    "ativo": True
                },
                "competidor_3": {
                    "nome": "Competidor 3",
                    "apelido": "Comp3",
                    "cor": "#45B7D1",
                    "emoji": "🔥",
                    "ativo": True
                },
                "competidor_4": {
                    "nome": "Competidor 4",
                    "apelido": "Comp4",
                    "cor": "#96CEB4",
                    "emoji": "💫",
                    "ativo": True
                },
                "competidor_5": {
                    "nome": "Competidor 5",
                    "apelido": "Comp5",
                    "cor": "#DDA0DD",
                    "emoji": "🎯",
                    "ativo": True
                }
            },
            "configuracoes_gerais": {
                "nome_bolao": "Bolão Copa 2026",
                "pontos_resultado": 15,
                "pontos_placar": 30
            }
        }

    def save_competitors_config(self, config: Dict):
        """
        Salva configuração dos competidores

        Args:
            config: Dicionário de configuração
        """
        config_file = self.assets_path / "competitors.json"

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        self.competitors_config = config

    def get_flag_path(self, country_name: str) -> Optional[Path]:
        """
        Obtém caminho da bandeira local

        Args:
            country_name: Nome do país

        Returns:
            Caminho do arquivo ou None
        """
        # Normaliza nome
        nome_arquivo = country_name.lower()
        nome_arquivo = nome_arquivo.replace(' ', '_')
        nome_arquivo = nome_arquivo.replace('á', 'a').replace('é', 'e')
        nome_arquivo = nome_arquivo.replace('í', 'i').replace('ó', 'o')
        nome_arquivo = nome_arquivo.replace('ú', 'u').replace('ã', 'a')
        nome_arquivo = nome_arquivo.replace('õ', 'o').replace('ç', 'c')
        nome_arquivo = nome_arquivo.replace('ô', 'o').replace('ê', 'e')
        nome_arquivo = nome_arquivo.replace('â', 'a').replace('î', 'i')

        flag_file = self.flags_path / f"{nome_arquivo}.png"

        if flag_file.exists():
            return flag_file

        return None

    def get_flag_base64(self, country_name: str) -> str:
        """
        Retorna bandeira em formato base64 para uso em HTML

        Args:
            country_name: Nome do país

        Returns:
            String base64 da bandeira
        """
        flag_path = self.get_flag_path(country_name)

        if flag_path and flag_path.exists():
            with open(flag_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()

        # Retorna bandeira genérica
        return self._get_default_flag_base64()

    def _get_default_flag_base64(self) -> str:
        """Cria uma bandeira genérica para países sem bandeira"""
        if PIL_AVAILABLE:
            img = Image.new('RGB', (80, 53), color='#CCCCCC')
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 79, 52], outline='#999999', width=2)

            try:
                font = ImageFont.truetype("arial.ttf", 20)
                draw.text((25, 15), "?", fill='#666666', font=font)
            except:
                draw.text((25, 15), "?", fill='#666666')

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()

        return ""

    def _get_initials(self, name: str) -> str:
        """
        Extrai iniciais do nome

        Args:
            name: Nome completo

        Returns:
            Iniciais (1-2 caracteres)
        """
        parts = name.strip().split()

        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        elif len(parts) == 1:
            return parts[0][:2].upper()

        return "??"

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Converte cor hexadecimal para RGB

        Args:
            hex_color: Cor em hex (#RRGGBB)

        Returns:
            Tupla (R, G, B)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def _create_avatar_image(self, initials: str, color: str,
                             emoji: str = None, size: int = 200) -> str:
        """
        Cria imagem do avatar

        Args:
            initials: Iniciais do competidor
            color: Cor de fundo (hex)
            emoji: Emoji opcional
            size: Tamanho em pixels

        Returns:
            String base64 da imagem
        """
        if not PIL_AVAILABLE:
            return ""

        # Cria imagem
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Converte cor para RGB
        rgb_color = self._hex_to_rgb(color)

        # Desenha círculo de fundo
        margin = 10
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=rgb_color
        )

        # Borda branca
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            outline='white',
            width=5
        )

        # Adiciona iniciais
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Centraliza texto
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) / 2
        y = (size - text_height) / 2 - size * 0.05

        # Sombra
        shadow_offset = 2
        draw.text(
            (x + shadow_offset, y + shadow_offset),
            initials,
            font=font,
            fill=(0, 0, 0, 100)
        )

        # Texto principal
        draw.text((x, y), initials, font=font, fill='white')

        # Emoji (se disponível)
        if emoji:
            try:
                emoji_font = ImageFont.truetype("seguiemj.ttf", size // 5)
                draw.text(
                    (size * 0.65, size * 0.65),
                    emoji,
                    font=emoji_font,
                    fill='white'
                )
            except:
                pass

        # Converte para base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")

        return base64.b64encode(buffered.getvalue()).decode()

    def create_avatar(self, competitor_name: str) -> str:
        """
        Cria ou carrega avatar do competidor

        Args:
            competitor_name: Nome do competidor

        Returns:
            String base64 do avatar
        """
        # Nome do arquivo
        avatar_name = competitor_name.lower().replace(' ', '_')
        avatar_file = self.avatars_path / f"{avatar_name}.png"

        # Se já existe, carrega
        if avatar_file.exists():
            try:
                with open(avatar_file, 'rb') as f:
                    return base64.b64encode(f.read()).decode()
            except:
                pass

        # Busca configuração SEM chamar get_competitor_info (evita recursão)
        info = None
        for comp_id, comp_config in self.competitors_config.get('competidores', {}).items():
            if (comp_config.get('nome') == competitor_name or
                    comp_config.get('apelido') == competitor_name):
                info = comp_config
                break

        # Se não encontrou, usa padrão
        if info is None:
            color_index = hash(competitor_name) % len(self.avatar_colors)
            info = {
                'cor': self.avatar_colors[color_index],
                'emoji': '👤'
            }

        # Gera avatar
        initials = self._get_initials(competitor_name)
        color = info.get('cor', '#3498db')
        emoji = info.get('emoji', None)

        avatar_base64 = self._create_avatar_image(initials, color, emoji)

        # Salva arquivo
        if avatar_base64:
            try:
                img_data = base64.b64decode(avatar_base64)
                with open(avatar_file, 'wb') as f:
                    f.write(img_data)
            except:
                pass

        return avatar_base64

    def get_competitor_info(self, competitor_name: str) -> Dict:
        """
        Obtém informações completas de um competidor

        Args:
            competitor_name: Nome do competidor

        Returns:
            Dicionário com informações
        """
        config = self.competitors_config.get('competidores', {})

        for comp_id, comp_config in config.items():
            if (comp_config.get('nome') == competitor_name or
                    comp_config.get('apelido') == competitor_name):
                return {
                    **comp_config,
                    'id': comp_id,
                    'avatar_base64': self.create_avatar(competitor_name)
                }

        # Não encontrou, retorna padrão
        color_index = hash(competitor_name) % len(self.avatar_colors)

        return {
            'id': 'desconhecido',
            'nome': competitor_name,
            'apelido': competitor_name,
            'cor': self.avatar_colors[color_index],
            'emoji': '👤',
            'ativo': True,
            'avatar_base64': self.create_avatar(competitor_name)
        }

    def get_all_competitors(self) -> Dict:
        """
        Retorna todos os competidores ativos

        Returns:
            Dicionário com competidores
        """
        config = self.competitors_config.get('competidores', {})

        ativos = {}
        for comp_id, comp_config in config.items():
            if comp_config.get('ativo', True):
                ativos[comp_id] = {
                    **comp_config,
                    'id': comp_id,
                    'avatar_base64': self.create_avatar(comp_config.get('nome', comp_id))
                }

        return ativos

    def get_country_code(self, country_name: str) -> str:
        """
        Obtém código ISO do país

        Args:
            country_name: Nome do país

        Returns:
            Código ISO de 2 letras
        """
        return self.country_flags.get(country_name, 'unknown')

    def get_flag_html(self, country_name: str, width: int = 30) -> str:
        """
        Gera HTML para exibir bandeira

        Args:
            country_name: Nome do país
            width: Largura em pixels

        Returns:
            String HTML com a bandeira
        """
        flag_base64 = self.get_flag_base64(country_name)

        if flag_base64:
            return f'<img src="data:image/png;base64,{flag_base64}" width="{width}" style="vertical-align: middle; border-radius: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">'

        return f'<span style="font-size: {width}px;">🏳️</span>'

    def get_avatar_html(self, competitor_name: str, size: int = 40) -> str:
        """
        Gera HTML para exibir avatar

        Args:
            competitor_name: Nome do competidor
            size: Tamanho em pixels

        Returns:
            String HTML com o avatar
        """
        avatar_base64 = self.create_avatar(competitor_name)

        if avatar_base64:
            return f'<img src="data:image/png;base64,{avatar_base64}" width="{size}" height="{size}" style="border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">'

        # Fallback com iniciais
        initials = self._get_initials(competitor_name)
        info = self.get_competitor_info(competitor_name)
        color = info.get('cor', '#3498db')

        return f'<div style="width: {size}px; height: {size}px; border-radius: 50%; background: {color}; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: {size // 2}px; border: 2px solid white;">{initials}</div>'

    def has_flag(self, country_name: str) -> bool:
        """
        Verifica se a bandeira existe localmente

        Args:
            country_name: Nome do país

        Returns:
            True se existe
        """
        return self.get_flag_path(country_name) is not None


# ============================================
# TESTE
# ============================================
def test_assets_manager():
    """Testa o gerenciador de assets"""

    print("\n" + "=" * 60)
    print("🧪 TESTE DO GERENCIADOR DE ASSETS")
    print("=" * 60)

    assets = AssetsManager()

    # Testa bandeiras
    print("\n🏳️ Bandeiras:")
    paises_teste = ['Brasil', 'Argentina', 'Alemanha', 'França', 'Japão']

    for pais in paises_teste:
        tem_bandeira = assets.has_flag(pais)
        status = "✅" if tem_bandeira else "❌ (baixe com: python utils/download_flags.py)"
        codigo = assets.get_country_code(pais)
        print(f"   {status} {pais} ({codigo})")

    # Testa competidores com tratamento de erro
    print("\n👤 Competidores:")
    try:
        nomes_teste = ['Arthur', 'Bruno', 'Gabriel', 'Lorenzo', 'Miguel']
        for nome in nomes_teste:
            try:
                info = assets.get_competitor_info(nome)
                print(f"   {info.get('emoji', '👤')} {info.get('nome', nome)} - Cor: {info.get('cor', '#999')}")
            except Exception as e:
                print(f"   ❌ {nome}: {str(e)[:50]}")
    except Exception as e:
        print(f"   ⚠️  Erro ao carregar competidores: {str(e)[:80]}")

    # Verifica quantas bandeiras existem
    try:
        flags_path = Path("assets/flags")
        if flags_path.exists():
            total_flags = len(list(flags_path.glob('*.png')))
            print(f"\n📊 Total de bandeiras baixadas: {total_flags}/48")
            if total_flags < 48:
                print("   ⚠️  Execute: python utils/download_flags.py")
        else:
            print("\n⚠️  Pasta assets/flags não encontrada!")
    except Exception as e:
        print(f"\n⚠️  Erro ao verificar bandeiras: {str(e)[:50]}")

    print("\n✅ Teste concluído!")
    return assets


if __name__ == "__main__":
    # Configura path manualmente para evitar erro
    import os

    os.chdir(Path(__file__).parent.parent)

    test_assets_manager()