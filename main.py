import numpy as np
import math
from main_task import interpolate_newton_forward_diff, interpolate_newton_backward_diff, \
    interpolate_newton_divided_diff, interpolate_lagrange
from plot_and_tables import print_difference_table
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class InterpolationRequest(BaseModel):
    points: list[dict]
    inter: float


class SecondFormRequest(BaseModel):
    func: str
    start: float
    end: float
    n: int
    inter: float


def are_nodes_equally_spaced(x):
    return all(math.isclose(x[i + 1] - x[i], x[1] - x[0]) for i in range(len(x) - 1))


app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def linspace(start, end, num):
    if num == 1:
        return [start]
    step = (end - start) / (num - 1)
    return [start + i * step for i in range(num)]


@app.post("/secondForm")
async def second(data: SecondFormRequest):
    print(data)
    functions = {
        "sin": np.sin,
        "cos": np.cos
    }
    x = linspace(data.start, data.end, data.n)
    y = [functions[data.func](i) for i in x]
    x_interp = data.inter
    res = get_solution(x, y, x_interp)
    arr = []
    for i in range(len(x)):
        arr.append({"x": x[i], "y": y[i]})
    res["points"] = arr
    return res


@app.post("/interpol")
async def interpolate(data: InterpolationRequest):
    x = []
    y = []
    print(data)
    for i in data.points:
        x.append(i["x"])
        y.append(i["y"])
    x_interp = data.inter
    return get_solution(x, y, x_interp)


def get_solution(x, y, x_interp):
    equally_spaced = are_nodes_equally_spaced(x)
    table = print_difference_table(x, y)
    if equally_spaced:
        if x[0] <= x_interp <= x[1]:
            y_interp_newton = interpolate_newton_forward_diff(x, y, x_interp)
        else:
            y_interp_newton = interpolate_newton_backward_diff(x, y, x_interp)
    else:
        y_interp_newton = interpolate_newton_divided_diff(x, y, x_interp)

    y_interp_lagrange = interpolate_lagrange(x, y, np.array(x_interp).reshape(1, ))[0]
    response = {
        "newton_result": y_interp_newton,
        "lagrange_result": y_interp_lagrange,
        "table": table
    }
    return response
