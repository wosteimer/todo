import pytest

from todo.entity.entity import Entity
from todo.entity.todo import Todo
from todo.repository.in_memory_todo_repository import InMemoryTodoRepository
from todo.use_case.add import AddUseCase
from todo.use_case.change import ChangeUsecase
from todo.use_case.home import HomeUseCase
from todo.use_case.remove import RemoveUseCase


async def create_repository():
    repository = InMemoryTodoRepository.create()
    for i in range(10):
        await repository.save(Entity.create(Todo(f"value {i + 1}", "", "")))

    return repository


@pytest.mark.asyncio
async def test_home_use_case():
    repository = await create_repository()
    use_case = HomeUseCase.create(repository)
    entities = await use_case.perform()

    assert len(entities) == 10

    for i in range(10):
        assert entities[i].data.text == f"value {i + 1}"


@pytest.mark.asyncio
async def test_add_use_case():
    repository = InMemoryTodoRepository.create()
    use_case = AddUseCase.create(repository)
    text = "value"
    entity = await use_case.perform(text)

    match await repository.get_by_id(entity.id):
        case None:
            assert False

        case entity:
            assert entity.data.text == text


@pytest.mark.asyncio
async def test_remove_use_case():
    repository = InMemoryTodoRepository.create()
    use_case = RemoveUseCase.create(repository)
    entity = Entity.create(Todo("Value", "", ""))
    await repository.save(entity)

    await use_case.perform(entity.id)

    assert await repository.get_by_id(entity.id) == None


@pytest.mark.asyncio
async def test_change_use_case():
    repository = InMemoryTodoRepository.create()
    use_case = ChangeUsecase.create(repository)
    entity = Entity.create(Todo("Value", "", "", False))
    await repository.save(entity)
    await use_case.perform(entity.id)

    match await repository.get_by_id(entity.id):
        case None:
            assert False

        case entity:
            assert entity.data.its_done == True
