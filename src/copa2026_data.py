"""Módulo: copa2026_data.py"""
# Em desenvolvimento...
# copa2026_data.py
"""
DADOS OFICIAIS DA COPA DO MUNDO 2026
12 Grupos (A-L) | 48 Seleções | 72 jogos na fase de grupos
Sede: Canadá, México e Estados Unidos
"""

# ============================================
# GRUPOS OFICIAIS
# ============================================
GRUPOS_COPA_2026 = {
    'A': {
        'nome': 'Grupo A',
        'selecoes': ['México', 'África do Sul', 'Coreia do Sul', 'República Tcheca'],
        'sedes_principais': ['Cidade do México', 'Guadalajara', 'Atlanta', 'Monterrey']
    },
    'B': {
        'nome': 'Grupo B',
        'selecoes': ['Canadá', 'Bósnia-Herzegovina', 'Catar', 'Suíça'],
        'sedes_principais': ['Toronto', 'Santa Clara', 'Los Angeles', 'Vancouver', 'Seattle']
    },
    'C': {
        'nome': 'Grupo C',
        'selecoes': ['Brasil', 'Marrocos', 'Haiti', 'Escócia'],
        'sedes_principais': ['Nova Jersey', 'Boston', 'Filadélfia', 'Atlanta', 'Miami']
    },
    'D': {
        'nome': 'Grupo D',
        'selecoes': ['Estados Unidos', 'Paraguai', 'Austrália', 'Turquia'],
        'sedes_principais': ['Los Angeles', 'Vancouver', 'Seattle', 'São Francisco']
    },
    'E': {
        'nome': 'Grupo E',
        'selecoes': ['Alemanha', 'Curaçao', 'Costa do Marfim', 'Equador'],
        'sedes_principais': ['Houston', 'Filadélfia', 'Toronto', 'Kansas City', 'Nova Jersey']
    },
    'F': {
        'nome': 'Grupo F',
        'selecoes': ['Holanda', 'Japão', 'Suécia', 'Tunísia'],
        'sedes_principais': ['Dallas', 'Monterrey', 'Houston', 'Kansas City']
    },
    'G': {
        'nome': 'Grupo G',
        'selecoes': ['Bélgica', 'Egito', 'Irã', 'Nova Zelândia'],
        'sedes_principais': ['Seattle', 'Los Angeles', 'Vancouver']
    },
    'H': {
        'nome': 'Grupo H',
        'selecoes': ['Espanha', 'Cabo Verde', 'Arábia Saudita', 'Uruguai'],
        'sedes_principais': ['Atlanta', 'Miami', 'Houston', 'Guadalajara']
    },
    'I': {
        'nome': 'Grupo I',
        'selecoes': ['França', 'Senegal', 'Iraque', 'Noruega'],
        'sedes_principais': ['Nova Jersey', 'Boston', 'Filadélfia', 'Toronto']
    },
    'J': {
        'nome': 'Grupo J',
        'selecoes': ['Argentina', 'Argélia', 'Áustria', 'Jordânia'],
        'sedes_principais': ['Kansas City', 'Santa Clara', 'Dallas', 'São Francisco']
    },
    'K': {
        'nome': 'Grupo K',
        'selecoes': ['Portugal', 'RD Congo', 'Uzbequistão', 'Colômbia'],
        'sedes_principais': ['Houston', 'Cidade do México', 'Guadalajara', 'Miami', 'Atlanta']
    },
    'L': {
        'nome': 'Grupo L',
        'selecoes': ['Inglaterra', 'Croácia', 'Gana', 'Panamá'],
        'sedes_principais': ['Dallas', 'Toronto', 'Boston', 'Filadélfia', 'Nova Jersey']
    }
}

# ============================================
# CALENDÁRIO OFICIAL DE JOGOS
# ============================================
JOGOS_FASE_GRUPOS = [
    # ============ GRUPO A ============
    {'grupo': 'A', 'rodada': 1, 'data': '2026-06-11', 'hora': '16:00', 'casa': 'México', 'visitante': 'África do Sul',
     'cidade': 'Cidade do México', 'placar_casa': 2, 'placar_visitante': 0, 'status': 'Realizado'},
    {'grupo': 'A', 'rodada': 2, 'data': '2026-06-11', 'hora': '23:00', 'casa': 'Coreia do Sul',
     'visitante': 'República Tcheca', 'cidade': 'Guadalajara', 'placar_casa': 2, 'placar_visitante': 1,
     'status': 'Realizado'},
    {'grupo': 'A', 'rodada': 3, 'data': '2026-06-18', 'hora': '13:00', 'casa': 'República Tcheca',
     'visitante': 'África do Sul', 'cidade': 'Atlanta', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'A', 'rodada': 4, 'data': '2026-06-18', 'hora': '22:00', 'casa': 'México', 'visitante': 'Coreia do Sul',
     'cidade': 'Guadalajara', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'A', 'rodada': 5, 'data': '2026-06-24', 'hora': '22:00', 'casa': 'República Tcheca',
     'visitante': 'México', 'cidade': 'Cidade do México', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'A', 'rodada': 6, 'data': '2026-06-24', 'hora': '22:00', 'casa': 'África do Sul',
     'visitante': 'Coreia do Sul', 'cidade': 'Monterrey', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},

    # ============ GRUPO B ============
    {'grupo': 'B', 'rodada': 1, 'data': '2026-06-12', 'hora': '16:00', 'casa': 'Canadá',
     'visitante': 'Bósnia-Herzegovina', 'cidade': 'Toronto', 'placar_casa': 1, 'placar_visitante': 1,
     'status': 'Realizado'},
    {'grupo': 'B', 'rodada': 2, 'data': '2026-06-13', 'hora': '16:00', 'casa': 'Catar', 'visitante': 'Suíça',
     'cidade': 'Santa Clara', 'placar_casa': 1, 'placar_visitante': 1, 'status': 'Realizado'},
    {'grupo': 'B', 'rodada': 3, 'data': '2026-06-18', 'hora': '16:00', 'casa': 'Suíça',
     'visitante': 'Bósnia-Herzegovina', 'cidade': 'Los Angeles', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'B', 'rodada': 4, 'data': '2026-06-18', 'hora': '19:00', 'casa': 'Canadá', 'visitante': 'Catar',
     'cidade': 'Vancouver', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'B', 'rodada': 5, 'data': '2026-06-24', 'hora': '16:00', 'casa': 'Suíça', 'visitante': 'Canadá',
     'cidade': 'Vancouver', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'B', 'rodada': 6, 'data': '2026-06-24', 'hora': '16:00', 'casa': 'Bósnia-Herzegovina',
     'visitante': 'Catar', 'cidade': 'Seattle', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO C ============
    {'grupo': 'C', 'rodada': 1, 'data': '2026-06-13', 'hora': '19:00', 'casa': 'Brasil', 'visitante': 'Marrocos',
     'cidade': 'Nova Jersey', 'placar_casa': 1, 'placar_visitante': 1, 'status': 'Realizado'},
    {'grupo': 'C', 'rodada': 2, 'data': '2026-06-13', 'hora': '22:00', 'casa': 'Haiti', 'visitante': 'Escócia',
     'cidade': 'Boston', 'placar_casa': 0, 'placar_visitante': 1, 'status': 'Realizado'},
    {'grupo': 'C', 'rodada': 3, 'data': '2026-06-19', 'hora': '19:00', 'casa': 'Escócia', 'visitante': 'Marrocos',
     'cidade': 'Boston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'C', 'rodada': 4, 'data': '2026-06-19', 'hora': '22:00', 'casa': 'Brasil', 'visitante': 'Haiti',
     'cidade': 'Filadélfia', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'C', 'rodada': 5, 'data': '2026-06-24', 'hora': '19:00', 'casa': 'Marrocos', 'visitante': 'Haiti',
     'cidade': 'Atlanta', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'C', 'rodada': 6, 'data': '2026-06-24', 'hora': '19:00', 'casa': 'Escócia', 'visitante': 'Brasil',
     'cidade': 'Miami', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO D ============
    {'grupo': 'D', 'rodada': 1, 'data': '2026-06-12', 'hora': '22:00', 'casa': 'Estados Unidos',
     'visitante': 'Paraguai', 'cidade': 'Los Angeles', 'placar_casa': 4, 'placar_visitante': 1, 'status': 'Realizado'},
    {'grupo': 'D', 'rodada': 2, 'data': '2026-06-14', 'hora': '01:00', 'casa': 'Austrália', 'visitante': 'Turquia',
     'cidade': 'Vancouver', 'placar_casa': 2, 'placar_visitante': 0, 'status': 'Realizado'},
    {'grupo': 'D', 'rodada': 3, 'data': '2026-06-19', 'hora': '16:00', 'casa': 'Estados Unidos',
     'visitante': 'Austrália', 'cidade': 'Seattle', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'D', 'rodada': 4, 'data': '2026-06-20', 'hora': '01:00', 'casa': 'Turquia', 'visitante': 'Paraguai',
     'cidade': 'São Francisco', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'D', 'rodada': 5, 'data': '2026-06-25', 'hora': '23:00', 'casa': 'Turquia', 'visitante': 'Estados Unidos',
     'cidade': 'Los Angeles', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'D', 'rodada': 6, 'data': '2026-06-25', 'hora': '23:00', 'casa': 'Paraguai', 'visitante': 'Austrália',
     'cidade': 'São Francisco', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO E ============
    {'grupo': 'E', 'rodada': 1, 'data': '2026-06-14', 'hora': '14:00', 'casa': 'Alemanha', 'visitante': 'Curaçao',
     'cidade': 'Houston', 'placar_casa': 7, 'placar_visitante': 1, 'status': 'Realizado'},
    {'grupo': 'E', 'rodada': 2, 'data': '2026-06-14', 'hora': '20:00', 'casa': 'Costa do Marfim',
     'visitante': 'Equador', 'cidade': 'Filadélfia', 'placar_casa': 1, 'placar_visitante': 0, 'status': 'Realizado'},
    {'grupo': 'E', 'rodada': 3, 'data': '2026-06-20', 'hora': '17:00', 'casa': 'Alemanha',
     'visitante': 'Costa do Marfim', 'cidade': 'Toronto', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'E', 'rodada': 4, 'data': '2026-06-20', 'hora': '21:00', 'casa': 'Equador', 'visitante': 'Curaçao',
     'cidade': 'Kansas City', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'E', 'rodada': 5, 'data': '2026-06-25', 'hora': '17:00', 'casa': 'Curaçao',
     'visitante': 'Costa do Marfim', 'cidade': 'Filadélfia', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'E', 'rodada': 6, 'data': '2026-06-25', 'hora': '17:00', 'casa': 'Equador', 'visitante': 'Alemanha',
     'cidade': 'Nova Jersey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO F ============
    {'grupo': 'F', 'rodada': 1, 'data': '2026-06-14', 'hora': '17:00', 'casa': 'Holanda', 'visitante': 'Japão',
     'cidade': 'Dallas', 'placar_casa': 2, 'placar_visitante': 2, 'status': 'Realizado'},
    {'grupo': 'F', 'rodada': 2, 'data': '2026-06-14', 'hora': '23:00', 'casa': 'Suécia', 'visitante': 'Tunísia',
     'cidade': 'Monterrey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'F', 'rodada': 3, 'data': '2026-06-20', 'hora': '14:00', 'casa': 'Holanda', 'visitante': 'Suécia',
     'cidade': 'Houston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'F', 'rodada': 4, 'data': '2026-06-21', 'hora': '01:00', 'casa': 'Tunísia', 'visitante': 'Japão',
     'cidade': 'Monterrey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'F', 'rodada': 5, 'data': '2026-06-25', 'hora': '20:00', 'casa': 'Japão', 'visitante': 'Suécia',
     'cidade': 'Dallas', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'F', 'rodada': 6, 'data': '2026-06-25', 'hora': '20:00', 'casa': 'Tunísia', 'visitante': 'Holanda',
     'cidade': 'Kansas City', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO G ============
    {'grupo': 'G', 'rodada': 1, 'data': '2026-06-15', 'hora': '16:00', 'casa': 'Bélgica', 'visitante': 'Egito',
     'cidade': 'Seattle', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'G', 'rodada': 2, 'data': '2026-06-15', 'hora': '22:00', 'casa': 'Irã', 'visitante': 'Nova Zelândia',
     'cidade': 'Los Angeles', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'G', 'rodada': 3, 'data': '2026-06-21', 'hora': '16:00', 'casa': 'Bélgica', 'visitante': 'Irã',
     'cidade': 'Los Angeles', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'G', 'rodada': 4, 'data': '2026-06-21', 'hora': '22:00', 'casa': 'Nova Zelândia', 'visitante': 'Egito',
     'cidade': 'Vancouver', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'G', 'rodada': 5, 'data': '2026-06-27', 'hora': '00:00', 'casa': 'Egito', 'visitante': 'Irã',
     'cidade': 'Seattle', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'G', 'rodada': 6, 'data': '2026-06-27', 'hora': '00:00', 'casa': 'Nova Zelândia', 'visitante': 'Bélgica',
     'cidade': 'Vancouver', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO H ============
    {'grupo': 'H', 'rodada': 1, 'data': '2026-06-15', 'hora': '13:00', 'casa': 'Espanha', 'visitante': 'Cabo Verde',
     'cidade': 'Atlanta', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'H', 'rodada': 2, 'data': '2026-06-15', 'hora': '19:00', 'casa': 'Arábia Saudita', 'visitante': 'Uruguai',
     'cidade': 'Miami', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'H', 'rodada': 3, 'data': '2026-06-21', 'hora': '13:00', 'casa': 'Espanha', 'visitante': 'Arábia Saudita',
     'cidade': 'Atlanta', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'H', 'rodada': 4, 'data': '2026-06-21', 'hora': '19:00', 'casa': 'Uruguai', 'visitante': 'Cabo Verde',
     'cidade': 'Miami', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'H', 'rodada': 5, 'data': '2026-06-26', 'hora': '21:00', 'casa': 'Cabo Verde',
     'visitante': 'Arábia Saudita', 'cidade': 'Houston', 'placar_casa': None, 'placar_visitante': None,
     'status': 'Pendente'},
    {'grupo': 'H', 'rodada': 6, 'data': '2026-06-26', 'hora': '21:00', 'casa': 'Uruguai', 'visitante': 'Espanha',
     'cidade': 'Guadalajara', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO I ============
    {'grupo': 'I', 'rodada': 1, 'data': '2026-06-16', 'hora': '16:00', 'casa': 'França', 'visitante': 'Senegal',
     'cidade': 'Nova Jersey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'I', 'rodada': 2, 'data': '2026-06-16', 'hora': '19:00', 'casa': 'Iraque', 'visitante': 'Noruega',
     'cidade': 'Boston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'I', 'rodada': 3, 'data': '2026-06-22', 'hora': '18:00', 'casa': 'França', 'visitante': 'Iraque',
     'cidade': 'Filadélfia', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'I', 'rodada': 4, 'data': '2026-06-22', 'hora': '21:00', 'casa': 'Noruega', 'visitante': 'Senegal',
     'cidade': 'Nova Jersey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'I', 'rodada': 5, 'data': '2026-06-26', 'hora': '16:00', 'casa': 'Noruega', 'visitante': 'França',
     'cidade': 'Boston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'I', 'rodada': 6, 'data': '2026-06-26', 'hora': '16:00', 'casa': 'Senegal', 'visitante': 'Iraque',
     'cidade': 'Toronto', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO J ============
    {'grupo': 'J', 'rodada': 1, 'data': '2026-06-16', 'hora': '22:00', 'casa': 'Argentina', 'visitante': 'Argélia',
     'cidade': 'Kansas City', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'J', 'rodada': 2, 'data': '2026-06-17', 'hora': '01:00', 'casa': 'Áustria', 'visitante': 'Jordânia',
     'cidade': 'Santa Clara', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'J', 'rodada': 3, 'data': '2026-06-22', 'hora': '14:00', 'casa': 'Argentina', 'visitante': 'Áustria',
     'cidade': 'Dallas', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'J', 'rodada': 4, 'data': '2026-06-23', 'hora': '00:00', 'casa': 'Jordânia', 'visitante': 'Argélia',
     'cidade': 'São Francisco', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'J', 'rodada': 5, 'data': '2026-06-27', 'hora': '23:00', 'casa': 'Argélia', 'visitante': 'Áustria',
     'cidade': 'Kansas City', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'J', 'rodada': 6, 'data': '2026-06-27', 'hora': '23:00', 'casa': 'Jordânia', 'visitante': 'Argentina',
     'cidade': 'Dallas', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO K ============
    {'grupo': 'K', 'rodada': 1, 'data': '2026-06-17', 'hora': '14:00', 'casa': 'Portugal', 'visitante': 'RD Congo',
     'cidade': 'Houston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'K', 'rodada': 2, 'data': '2026-06-17', 'hora': '23:00', 'casa': 'Uzbequistão', 'visitante': 'Colômbia',
     'cidade': 'Cidade do México', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'K', 'rodada': 3, 'data': '2026-06-23', 'hora': '14:00', 'casa': 'Portugal', 'visitante': 'Uzbequistão',
     'cidade': 'Houston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'K', 'rodada': 4, 'data': '2026-06-23', 'hora': '23:00', 'casa': 'Colômbia', 'visitante': 'RD Congo',
     'cidade': 'Guadalajara', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'K', 'rodada': 5, 'data': '2026-06-27', 'hora': '20:30', 'casa': 'Colômbia', 'visitante': 'Portugal',
     'cidade': 'Miami', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'K', 'rodada': 6, 'data': '2026-06-27', 'hora': '20:30', 'casa': 'RD Congo', 'visitante': 'Uzbequistão',
     'cidade': 'Atlanta', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},

    # ============ GRUPO L ============
    {'grupo': 'L', 'rodada': 1, 'data': '2026-06-17', 'hora': '17:00', 'casa': 'Inglaterra', 'visitante': 'Croácia',
     'cidade': 'Dallas', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'L', 'rodada': 2, 'data': '2026-06-17', 'hora': '20:00', 'casa': 'Gana', 'visitante': 'Panamá',
     'cidade': 'Toronto', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'L', 'rodada': 3, 'data': '2026-06-23', 'hora': '17:00', 'casa': 'Inglaterra', 'visitante': 'Gana',
     'cidade': 'Boston', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'L', 'rodada': 4, 'data': '2026-06-23', 'hora': '20:00', 'casa': 'Panamá', 'visitante': 'Croácia',
     'cidade': 'Toronto', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'L', 'rodada': 5, 'data': '2026-06-27', 'hora': '18:00', 'casa': 'Croácia', 'visitante': 'Gana',
     'cidade': 'Filadélfia', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
    {'grupo': 'L', 'rodada': 6, 'data': '2026-06-27', 'hora': '18:00', 'casa': 'Panamá', 'visitante': 'Inglaterra',
     'cidade': 'Nova Jersey', 'placar_casa': None, 'placar_visitante': None, 'status': 'Pendente'},
]

# ============================================
# MAPEAMENTO DE BANDEIRAS (CÓDIGOS ISO)
# ============================================
BANDEIRAS_SELECOES = {
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

# ============================================
# CORES DAS SELEÇÕES
# ============================================
CORES_SELECOES = {
    'México': ['#006847', '#CE1126'],
    'África do Sul': ['#007A4D', '#FFB81C'],
    'Coreia do Sul': ['#C60C30', '#003478'],
    'República Tcheca': ['#11457E', '#D7141A'],
    'Canadá': ['#FF0000', '#FFFFFF'],
    'Bósnia-Herzegovina': ['#001489', '#FFCD00'],
    'Catar': ['#8A1538', '#FFFFFF'],
    'Suíça': ['#FF0000', '#FFFFFF'],
    'Brasil': ['#009C3B', '#FFDF00'],
    'Marrocos': ['#C1272D', '#006233'],
    'Haiti': ['#00209F', '#D21034'],
    'Escócia': ['#0065BF', '#FFFFFF'],
    'Estados Unidos': ['#002868', '#BF0A30'],
    'Paraguai': ['#D52B1E', '#FFFFFF'],
    'Austrália': ['#00843D', '#FFCD00'],
    'Turquia': ['#E30A17', '#FFFFFF'],
    'Alemanha': ['#000000', '#DD0000'],
    'Curaçao': ['#0055A4', '#FFD700'],
    'Costa do Marfim': ['#F77F00', '#FFFFFF'],
    'Equador': ['#FFD700', '#0033A0'],
    'Holanda': ['#FF6600', '#FFFFFF'],
    'Japão': ['#BC002D', '#FFFFFF'],
    'Suécia': ['#005B99', '#FECC00'],
    'Tunísia': ['#E70013', '#FFFFFF'],
    'Bélgica': ['#000000', '#FDDA24'],
    'Egito': ['#CE1126', '#FFFFFF'],
    'Irã': ['#239F40', '#FFFFFF'],
    'Nova Zelândia': ['#000000', '#FFFFFF'],
    'Espanha': ['#C60B1E', '#FFC400'],
    'Cabo Verde': ['#003893', '#FFFFFF'],
    'Arábia Saudita': ['#006C35', '#FFFFFF'],
    'Uruguai': ['#7CC0F0', '#0038A8'],
    'França': ['#0055A4', '#EF4135'],
    'Senegal': ['#00853F', '#FDEF42'],
    'Iraque': ['#CE1126', '#FFFFFF'],
    'Noruega': ['#BA0C2F', '#FFFFFF'],
    'Argentina': ['#75AADB', '#FFFFFF'],
    'Argélia': ['#006633', '#FFFFFF'],
    'Áustria': ['#EF3340', '#FFFFFF'],
    'Jordânia': ['#CE1126', '#FFFFFF'],
    'Portugal': ['#006600', '#FF0000'],
    'RD Congo': ['#007FFF', '#CE1021'],
    'Uzbequistão': ['#0099B5', '#CE1126'],
    'Colômbia': ['#FCD116', '#003893'],
    'Inglaterra': ['#FFFFFF', '#CF081F'],
    'Croácia': ['#FF0000', '#FFFFFF'],
    'Gana': ['#CE1126', '#FCD116'],
    'Panamá': ['#005293', '#D21034'],
}

# ============================================
# ESTATÍSTICAS GERAIS
# ============================================
INFO_COPA = {
    'nome': 'Copa do Mundo FIFA 2026',
    'sedes': ['Canadá', 'México', 'Estados Unidos'],
    'data_inicio': '11 de junho de 2026',
    'data_fim': '19 de julho de 2026',
    'total_selecoes': 48,
    'total_grupos': 12,
    'jogos_fase_grupos': 72,
    'jogos_mata_mata': 32,
    'total_jogos': 104,
    'estadios': 16,
    'cidades_sede': [
        'Atlanta', 'Boston', 'Dallas', 'Filadélfia', 'Guadalajara',
        'Houston', 'Kansas City', 'Los Angeles', 'Miami', 'Monterrey',
        'Nova Jersey', 'São Francisco', 'Santa Clara', 'Seattle',
        'Toronto', 'Vancouver', 'Cidade do México'
    ]
}
