from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import *
from datetime import datetime
import threading
import requests
import uuid
from sudoku_generator import generate_new_puzzle
import json
connect("sudoku")


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Puzzles(Document):
    id  = StringField(primary_key = True, default = str(uuid.uuid4().hex))
    puzzle = DictField()
    solution  = DictField()
    timestamp = DateTimeField(default=datetime.now())


@app.get("/new-puzzle")
async def get_new_puzzle():

    puzzle, solution = generate_new_puzzle()

    db_puzzle = {}
    db_solution = {}
    for i in range(9):
        db_puzzle[str(i)] = {}
        db_solution[str(i)] = {}
        for j in range(9):
            db_solution[str(i)][str(j)] = solution[i][j]
            db_puzzle[str(i)][str(j)] = puzzle[i][j]

    Puzzles(**{"puzzle":db_puzzle, "solution":db_solution}).save()
    return JSONResponse({"puzzle":db_puzzle, "solution":db_solution})