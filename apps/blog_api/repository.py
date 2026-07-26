from typing import List
from .models import Post


class PostRepository:
    async def get_by_id(self, post_id: int) -> Post | None:
        try:
            return await Post.objects.aget(id=post_id)
        except Post.DoesNotExist:
            return None

    async def get_all(self) -> List[Post]:
        return [post async for post in Post.objects.all()]

    async def create(self, title: str, content: str) -> Post:
        return await Post.objects.acreate(
            title=title,
            content=content
        )

    async def update(self, post_id: int, **kwargs) -> Post | None:
        post = await self.get_by_id(post_id)
        if not post:
            return None

        for key, value in kwargs.items():
            setattr(post, key, value)

        await post.asave()
        return post

    async def delete(self, post_id: int) -> bool:
        post = await self.get_by_id(post_id)
        if not post:
            return False

        await post.adelete()
        return True

    async def exists(self, post_id: int) -> bool:
        return await Post.objects.filter(id=post_id).aexists()