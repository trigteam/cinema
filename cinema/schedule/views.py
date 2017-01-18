from datetime import datetime, timedelta
from django.shortcuts import render
from ..schedule.models import Seance, Hall
from ..catalog.models import Movie

def generateDateList():
    futureDaysNumber = 4
    dateList = []

    for dayNumber in range(0,futureDaysNumber):
        date = datetime.today() + timedelta(dayNumber)
        date = date.strftime('%d-%m')
        dateList.append(date)

    return dateList

def createSeancesDict(seancesList):
    movieTitleList = []
    seancesDict = {}

    for seance in seancesList:
        movieTitle = seance.movie.title
        movieTitleList.append(movieTitle)

    movieTitleList = list(set(movieTitleList))

    for movieTitle in movieTitleList:
        seanceTimeList = []
        for seance in seancesList:
            if (seance.movie.title == movieTitle):
                movie = seance.movie
                seance_id = seance.id
                seanceTimeList.append([seance.start_time.strftime('%H-%M'), seance_id])

        seancesDict.update({movie:seanceTimeList})

    return seancesDict


def show_schedule(request, day=0, month=0):
    dateList = generateDateList()
    context = {'dateList' : dateList}

    return render(request, 'schedule/schedule.html', context)

def show_concrete_schedule(request, day=0, month=0):
    dateList = generateDateList()
    seancesDict = []

    seancesExists = Seance.objects.filter(start_time__month=month, start_time__day=day).exists()

    if (seancesExists):
        seancesList = list(Seance.objects.filter(start_time__month=month, start_time__day=day))
        seancesDict = createSeancesDict(seancesList)

    context = {'dateList' : dateList, 'seancesExists' : seancesExists, 'seancesDict' : seancesDict}
    
    return render(request, 'schedule/schedule.html', context)