from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = False
    description: str | None = Field(default=None, max_length=1000)


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    """作成時に受け取るデータ"""


class TodoPublic(TodoBase):
    id: int


class TodoUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None
    description: str | None = Field(default=None, max_length=1000)
