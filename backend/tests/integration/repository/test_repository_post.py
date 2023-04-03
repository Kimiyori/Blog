from bson import ObjectId
import pytest
from src.db.schemas.post import (
    PostCreate,
    ContentPost,
    TextBlock,
    PostUpdate,
    ImageBlock,
)
from src.repository.post import PostRepository
from tests.conftest import session_mock, mock_settings, client


@pytest.fixture
async def repo(session_mock, mock_settings):
    return PostRepository(
        session_mock[0], session_mock[1], mock_settings.MONGODB_DATABASE
    )


POST_CREATE = PostCreate(
    user_id=ObjectId(),
    title="test",
    content=[
        ContentPost(order=1, data=TextBlock(type="text", text="test")),
        ContentPost(order=2, data=TextBlock(type="text", text="test2")),
    ],
)


@pytest.fixture
async def post(repo):
    id = await repo.add(POST_CREATE.dict())
    await repo.session.commit_transaction()
    return id


async def test_repository_update_post(repo, post, session_mock):
    expected = PostUpdate(
        title="new_title",
        update_content=[
            ContentPost(order=1, data=TextBlock(type="text", text="test2")),
            ContentPost(order=3, data=ImageBlock(type="image", url="test_url")),
        ],
        delete_content=[2],
    )
    await repo.update_post(post, expected)
    updated_post = await session_mock[0].test.posts.find_one(
        {"_id": post}, session=session_mock[1]
    )
    assert updated_post["title"] == expected.title
    assert len(updated_post["content"]) == 2
    for block_upd, block_exp in zip(updated_post["content"], expected.update_content):
        assert block_upd["order"] == block_exp.order


async def test_repository_update_post_only_delete(repo, post, session_mock):
    expected = PostUpdate(
        delete_content=[2],
    )
    await repo.update_post(post, expected)
    updated_post = await session_mock[0].test.posts.find_one(
        {"_id": post}, session=session_mock[1]
    )
    assert len(updated_post["content"]) == 1
    assert updated_post["content"][0]["order"] == 1


async def test_repository_update_post_only_update(repo, post, session_mock):
    expected = PostUpdate(
        update_content=[
            ContentPost(order=3, data=ImageBlock(type="image", url="test_url")),
        ]
    )
    await repo.update_post(post, expected)
    updated_post = await session_mock[0].test.posts.find_one(
        {"_id": post}, session=session_mock[1]
    )
    assert len(updated_post["content"]) == 3
    for i, block in enumerate(updated_post["content"]):
        assert block["order"] == i + 1


async def test_repository_update_post_only_main(repo, post, session_mock):
    expected = PostUpdate(title="new_title")
    await repo.update_post(post, expected)
    updated_post = await session_mock[0].test.posts.find_one(
        {"_id": post}, session=session_mock[1]
    )
    assert len(updated_post["content"]) == 2
    assert updated_post["title"] == expected.title


async def test_repository_update_post_empty(repo, post, session_mock):
    expected = PostUpdate()
    await repo.update_post(post, expected)
    updated_post = await session_mock[0].test.posts.find_one(
        {"_id": post}, session=session_mock[1]
    )
    assert updated_post["title"] == POST_CREATE.title
    assert len(updated_post["content"]) == 2
    for block_upd, block_exp in zip(updated_post["content"], POST_CREATE.content):
        assert block_upd["order"] == block_exp.order


async def test_get_full_post(repo, post, client, mock_settings):
    old_post = await repo.get_by_id(post)
    assert old_post["views"] == 1
    result = await repo.get_full_post(post)
    assert result["views"] == 2
    async with await client.start_session() as session:
        async with session.start_transaction():
            new_repo = PostRepository(client, session, mock_settings.MONGODB_DATABASE)
            result = await new_repo.get_full_post(post)
            assert result["views"] == 3
