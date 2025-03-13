from pydantic import BaseModel

# Esquema para crear un partido
class MatchCreate(BaseModel):
    competition_id: int
    player1_id: int
    player2_id: int

# Esquema para leer un partido
class MatchRead(BaseModel):
    id: int
    competition_id: int
    player1_id: int
    player2_id: int
    player1_score: int
    player2_score: int
    round_number: int

    class Config:
        from_attributes = True  

# Esquema para actualizar el marcador
class MatchUpdateScore(BaseModel):
    player1_score: int
    player2_score: int
