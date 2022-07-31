import os
from pathlib import Path
import tempfile
from typing import Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from git import Repo
GITHUBDEPLOY = os.environ['GITHUBDEPLOY']
app = FastAPI()


class Form(BaseModel):
    title: str
    initiate: str
    process: str
    bestpractices: str

def _create_file(form: Form, filepath: Path):
    print(filepath.absolute())
    with filepath.open('w') as f:
        f.write("test")

def process(form: Form):
    tmpdir = "test"
    os.makedirs(tmpdir, exist_ok=True)
    folder = os.path.join(tmpdir, "commonFraudsIndia")
    cmtname = "Created by bot using google form: " + form.title
    repo = Repo.clone_from(f"https://rusiaaman:{GITHUBDEPLOY}@github.com/rusiaaman/commonFraudsIndia.git", folder)
    repo.config_writer().set_value("user", "name", "Aman Rusia").release()
    repo.config_writer().set_value("user", "email", "rusia.aman@gmail.com").release()

    new_branch = str(uuid4())
    current = repo.create_head(new_branch)
    current.checkout()
    master = repo.heads.master
    repo.git.pull('origin', master)

    new_file = Path(folder) / "list" / form.title 
    _create_file(form, new_file)

    repo.git.add(A=True)
    repo.git.commit(m=cmtname)
    repo.git.push('--set-upstream', 'origin', current)


@app.post("/")
def create_new_pr(form: Form):

    if not form.title.strip():
        return HTTPException(400, "Missing title")
    process(form)
    return "ok"
