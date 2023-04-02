import pytest
from src.db.schemas.post import *
from pydantic import ValidationError


def test_content_post():
    data = TextBlock(type="text", text="test")
    expected = ContentPost(data=data, order=1)
    assert expected.order == 1
    assert expected.data == data


def test_content_post_wrong_literal_type():
    with pytest.raises(ValidationError):
        TextBlock(type="image", text="test")


def test_content_post_negative_order():
    data = TextBlock(type="text", text="test")
    with pytest.raises(ValidationError):
        ContentPost(data=data, order=-1)


def test_content_post_unique_order_values():
    block1 = ContentPost(data=TextBlock(type="text", text="test"), order=1)
    block2 = ContentPost(data=TextBlock(type="text", text="test"), order=2)
    PostIn(content=[block1, block2], title="test")


def test_content_post_unique_order_values_error():
    block1 = ContentPost(data=TextBlock(type="text", text="test"), order=1)
    block2 = ContentPost(data=TextBlock(type="text", text="test"), order=1)
    with pytest.raises(ValidationError):
        PostIn(content=[block1, block2], title="test")


def test_post_update():
    post = PostUpdate(
        title="test",
        update_content=[ContentPost(data=TextBlock(type="text", text="test"), order=1)],
        delete_content=[2],
    )


def test_post_update_intersect_order_values_update_and_delete():
    with pytest.raises(ValidationError):
        PostUpdate(
            title="test",
            update_content=[
                ContentPost(data=TextBlock(type="text", text="test"), order=1)
            ],
            delete_content=[1],
        )


def test_post_update_delete_duplicate():
    with pytest.raises(ValidationError):
        PostUpdate(delete_content=[1, 1])
