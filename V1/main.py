
# Proste wykorzystanie biblioteki FastAPI
from fastapi import FastAPI, Response, status, Query, Path, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
from employee import Employee
from typing import List, Optional
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()

security = HTTPBasic()
def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# dane inicjalne
employees: List[Employee] = []
emp = Employee(id=1, fname="Jan", lname="Kowalski", pesel="80121212345", manager=False, acl=[101, 102, 103])
employees.append(emp)
emp = Employee(id=2, fname="Elvis", lname="Presley", pesel="80121212346", manager=True, acl=[101, 102, 103])
employees.append(emp)
emp = Employee(id=3, fname="Zygmunt", lname="Nowak", pesel="80121212344", manager=True, acl=[234, 555, 666])
employees.append(emp)

@app.get("/secret")
async def secret(username : str = Depends(check_auth)):
    return {"message":"secret endpoint"}

@app.get("/items", response_model=List[Employee])
async def get_list():
    return employees

@app.get("/item/{emp_id}")
async def get_employee(emp_id:int, response: Response):
    emp = list(filter(lambda x: x.id == emp_id, employees))
    if len(emp):
        return emp[0]

    #response.status_code = status.HTTP_404_NOT_FOUND
    #return {"message":"not found"}
    raise HTTPException(status_code=404, detail="not found")

@app.post("/item", status_code=status.HTTP_201_CREATED)
async def add_employee(emp: Employee, response : Response):
    obj = max(employees, key=lambda p: p.id)
    if obj:
        emp.id = obj.id + 1
        emp.create_ts = datetime.now()
        employees.append(emp)
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { "message" : "ERROR"}

@app.get("/find", description="Wyszukiwanie pracownika")
async def find_employee(response: Response, q:Optional[str]= Query(None,
                                                 title="Nazwisko",
                                                 alias="query",
                                                 description="Podaj poszukiwaną frazę",
                                                 min_length=3, max_length=50)):
    emp = list(filter(lambda x: q.upper() in x.lname.upper(), employees))
    if len(emp):
        return emp[0]
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Not found"}



@app.get("/img")
async def get_image():
    fd = open("cat.png", mode="rb")
    return StreamingResponse(fd, media_type="image/png")

@app.get("/html")
async def get_html():
    html_content = """
    <html>
        <body>
            <h1>Hello FastAPI</h1>
        </body>
    </html>
    """
    return HTMLResponse(html_content, status_code=200)

@app.get("/")
async def main():
    return {"message" : "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)

