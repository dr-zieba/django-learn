from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ..models import WatchList, Platform, Review
from .serializers import WatchListSerializer, PlatformSerializer, ReviewSerializer
from .permisions import IsAdminOrReadOnly, IsReviewOwnerPermission
from .pagination import WatchListPagination
from rest_framework.throttling import UserRateThrottle


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.kwargs['username']
    #     return Review.objects.filter(user__username=user)
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Review.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset


class ReviewList(generics.ListAPIView):
    permission_classes = [IsReviewOwnerPermission]
    throttle_classes = [UserRateThrottle]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewOwnerPermission]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        watchlist = WatchList.objects.get(pk=pk)

        user = self.request.user
        review = Review.objects.filter(user=user, watchlist=watchlist)
        if review.exists():
            raise ValidationError("Already reviewed")

        if watchlist.number_of_rates == 0:
            watchlist.number_of_rates += 1
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.number_of_rates += 1
            watchlist.avg_rating = (
                watchlist.avg_rating
                + serializer.validated_data["rating"] / watchlist.number_of_rates
            )

        watchlist.save()

        serializer.save(watchlist=watchlist, user=user)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
#                 ):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class WatchListAll(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = WatchListPagination


# class WatchListAll(APIView):
#     permission_classes = [IsAdminOrReadOnly]
#     pagination_class = WatchListPagination
#
#     def get(self, request):
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(
#             movies, many=True, context={"request": request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListById(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            movie.delete()
            return Response({"msg": "deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


# class PlatformAll1(viewsets.ModelViewSet):
#     queryset = Platform.objects.all()
#     serializer_class = PlatformSerializer


class PlatformAll(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = Platform.objects.all()
        serializer = PlatformSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Platform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serilizer = PlatformSerializer(platform)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = Platform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PlatformAll(APIView):
#     def get(self, request):
#         platform = Platform.objects.all()
#         serializer = PlatformSerializer(
#             platform, many=True, context={"request": request}
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = PlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PlatformById(APIView):
#     def get(self, request, pk):
#         platform = Platform.objects.get(pk=pk)
#         serializer = PlatformSerializer(platform, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         try:
#             platform = Platform.objects.get(pk=pk)
#         except Exception as e:
#             raise ValueError("Not found")
#         serializer = PlatformSerializer(platform, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             platform = Platform.objects.get(pk=pk)
#         except Exception as e:
#             raise ValueError("Not found")
#
#         serializer = PlatformSerializer(platform, request.data)
#         if serializer.is_valid():
#             platform.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#
# @api_view(["GET", "POST"])
# def movie_list(request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     if request.method == "POST":
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def get_movie(request, pk):
#     if request.method == "GET":
#         try:
#             movie = Movie.objects.get(id=pk)
#         except Movie.DoesNotExists:
#             return Response({'error': 'Not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == "PUT":
#         movie = Movie.objects.get(id=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == "DELETE":
#         movie = Movie.objects.get(id=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
