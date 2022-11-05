from fastapi import FastAPI, HTTPException

from .serializers import CategorySerializer
from .models import database, Category, Notes

app = FastAPI(title="Notes-to-do-list")


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/category/")
async def get_all_category() -> Category:
    return await Category.objects.all()


@app.get("/category/{cat_id}")
async def get_item_category(cat_id: int) -> Category:
    try:
        return await Category.objects.get(pk=cat_id)
    except Exception:
        return HTTPException(status_code=404)


@app.post("/category/")
async def create_category(category: CategorySerializer) -> Category:
    return await Category.objects.create(**category.dict())


@app.put("/category/{cat_id}")
async def update_category(cat_id: int, category: Category) -> Category:
    try:
        instance = await Category.objects.get(pk=cat_id, raise_exception=True)
        return await instance.update(**category.dict())
    except Exception:
        raise HTTPException(status_code=404)


@app.delete("/category/{cat_id}")
async def drop_category(cat_id: int) -> Category:
    try:
        instance = await Category.objects.get(pk=cat_id)
        await instance.delete()
        return {"deleted_row": instance}
    except Exception:
        raise HTTPException(status_code=404)


@app.get("/notes/")
async def get_all_notes():
    return await Notes.objects.all()


@app.get("/notes/{note_id}")
async def get_item_notes(note_id: int):
    try:
        return await Notes.objects.get(pk=note_id)
    except Exception:
        raise HTTPException(status_code=404)


@app.post("/notes/")
async def create_note(notes: Notes) -> Notes:
    return await Notes.objects.create(**notes.dict())


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
