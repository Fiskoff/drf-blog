from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .schemas import PostSerializer, PostCreateSerializer
from .repository import PostRepository


class PostListCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = PostRepository()

    async def get(self, request):
        posts = await self.repository.get_all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    async def post(self, request):
        serializer = PostCreateSerializer(data=request.data)

        is_valid = await sync_to_async(serializer.is_valid)()
        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = await self.repository.create(
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content']
        )

        response_serializer = PostSerializer(post)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = PostRepository()

    async def get(self, request, post_id):
        post = await self.repository.get_by_id(post_id)
        if not post:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post)
        return Response(serializer.data)

    async def put(self, request, post_id):
        serializer = PostCreateSerializer(data=request.data)

        is_valid = await sync_to_async(serializer.is_valid)()
        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = await self.repository.update(post_id, **serializer.validated_data)
        if not post:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        response_serializer = PostSerializer(post)
        return Response(response_serializer.data)

    async def delete(self, request, post_id):
        deleted = await self.repository.delete(post_id)
        if not deleted:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)