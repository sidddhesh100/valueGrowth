from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.authtoken.models import Token
import requests
from bs4 import BeautifulSoup

# Create your views here.
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    url = "https://results.eci.gov.in/AcResultByeJan2024/candidateswise-S203.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    lost_candidate = soup.find_all("div", attrs={"class": "status lost"})
    win_condidate = soup.find_all("div", attrs={"class": "status won"})
    score = [int(candidate.contents[3].contents[0]) for candidate in win_condidate+lost_candidate]
    return Response(data={"status": True, "lost_count": len(lost_candidate), "win_count": len(win_condidate), "score": sorted(score)}, status=HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    token_details = Token.objects.get(key=request.auth.key)
    token_details.delete()
    return Response(data={"status": True, "message": "User sing-out"}, status=HTTP_200_OK)