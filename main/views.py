from django.http import HttpResponse
from django.db.models import Count
from .models import User, Tweet


def user_recommendation(request):
    user_id = request.GET.get("user_id")
    contact_type = request.GET.get("type")
    phrase = request.GET.get("phrase")
    hashtag = request.GET.get("hashtag")

    results = User.objects.exclude(id=user_id).order_by("-followers_count")[:10]

    response_data = "TeamCoolCloud,1234-0000-0001\n"
    for user in results:
        response_data += f"{user.id}\t{user.screen_name}\t{user.description}\t{user.tweet_set.first().text}\n"

    return HttpResponse(response_data, content_type="text/plain")


def data_statistics(request):
    total_users = User.objects.count()
    total_tweets = Tweet.objects.count()

    return HttpResponse(f"Total tweets: {total_tweets}\tTotal users: {total_users}")
