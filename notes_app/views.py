from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from notes_app.models import Diary, Category
# Create your views here.
def get_all_entries():
    entries = list(Diary.objects.all())
    formattedEntries = []
    for i in entries:
        formattedEntries.append((i.id, i.note, i.date_time_issued.strftime("%A"),
                                 i.date_time_issued.strftime("%x"),
                                 i.date_time_issued.strftime("%H:%M"), i.category))
    return formattedEntries

class HomeView(View):
    def get(self, request):
        print(get_all_entries())
        projects = get_all_entries()
        return render(request, 'projects.html', {"projects": projects})


    def post(self, request):
        print(request.POST)
        try:
            note = request.POST["note"]
            print(type(request.POST["date_issued"]))
            newDate = datetime.datetime.strptime(request.POST["date_issued"], '%Y-%m-%dT%H:%M')
            print(type(newDate))
            category = request.POST["category"]
            category_instance = Category.objects.create(name=category)
            Diary.objects.create(note=note, date_time_issued=newDate, day= newDate.strftime("%A"), category=category_instance)
            user_message = "note added successfully"


        except ValueError:
            user_message = "you didn't enter the details correctly"

            return render(request, 'add_project.html', {"message": get_all_entries(), "user_message": user_message})

        return redirect('home')


class AddNoteView(View):
    def get(self, request):
        return render(request, 'add_project.html')


    def post(self, request):
        print(request.POST)
        try:
            note = request.POST["note"]
            print(type(request.POST["date_issued"]))
            newDate = datetime.strptime(request.POST["date_issued"], '%Y-%m-%dT%H:%M')
            print(type(newDate))
            category = request.POST["category"]
            category_instance = Category.objects.create(name=category)
            Diary.objects.create(note=note, date_time_issued=newDate, day= newDate.strftime("%A"), category=category_instance)
            user_message = "note added successfully"


        except ValueError:
            user_message = "you didn't enter the details correctly"

            return render(request, 'add_project.html', {"user_message": user_message})

        return redirect('home')

class EditNoteView(View):
    def get(self, request, **kwargs):
        note_id = self.kwargs["id"]
        print(note_id)
        note = Diary.objects.get(id=note_id)

        return render(request, 'edit_project.html', {'note': note})

    def post(self, request, **kwargs):
        note_id = self.kwargs["id"]
        diary = get_object_or_404(Diary, id=note_id)
        try:
            note = request.POST["note"]
            newDate = datetime.strptime(request.POST["date_issued"], '%Y-%m-%dT%H:%M')
            category = request.POST["category"]
            category_instance, _ = Category.objects.get_or_create(name=category)
            diary.note = note
            diary.date_time_issued = newDate
            diary.day = newDate.strftime("%A")
            diary.category = category_instance
            diary.save()
            user_message = "note updated successfully"
            return render(request, 'edit_project.html', {"user_message": user_message})
        except ValueError:
            user_message = "you didn't enter the details correctly"
            return render(request, 'edit_project.html', {"user_message": user_message})

