# view_api/apps_api/posts/search/search_apis.py

import logging

from django_elasticsearch_dsl.search import Search

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)

from posts.documents import PostDocument
from posts.models import Post

from view_api.apps_api.search.search_serializer import PostSearchOutputSerializer

logger = logging.getLogger(__name__)


class SearchAPIView(APIView):

    @extend_schema(
        summary="Search Posts",
        description="""
Search posts using Elasticsearch.

Fields searched:

- title
- category

Example:

`/api/posts/search/?q=django`
""",
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                required=True,
                location=OpenApiParameter.QUERY,
                description="Search keyword",
            )
        ],
        responses={
            200: PostSearchOutputSerializer(many=True),
            400: OpenApiResponse(description="Query parameter is required"),
        },
        tags=["Posts Search"],
    )
    def get(self, request: Request):

        query = request.query_params.get("q")

        if not query:
            return Response(
                {"detail": "query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search = (
            PostDocument.search()
            .query(
                "multi_match",
                query=query,
                fields=[
                    "title",
                    "category",
                ],
            )
        )

        result = search.execute()

        ids = [hit.meta.id for hit in result]

        posts = Post.objects.filter(id__in=ids)

        serializer = PostSearchOutputSerializer(posts, many=True)

        logger.info("Search '%s' returned %s results", query, len(posts))

        return Response(serializer.data)