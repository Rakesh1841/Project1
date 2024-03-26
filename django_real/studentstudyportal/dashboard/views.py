from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch 
import requests
import json
import wikipedia


def home(request):

    return render(request, 'home.html/')


def notes(request): #it is for creating
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Notes( user=request. user,title=request.POST['title'],discription=request.POST['discription'])
            notes.save()
        messages.success(request, f"data addaed  successfully for  the user : {request.user.username}")
        
    else: 
        form = NoteForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'notes.html',context)

def delete_note(request,pk=None):
    note1= Notes.objects.get(pk=pk)
    note1.delete()
    messages.error(request,f"Note deleted Successfully by {request.user.username}")   

    return redirect('notes')

class Note_detail_view(generic.DetailView):
    model = Notes
    template_name = 'notes_detail.html'


def homework(request):
    if request.method=="POST":
        form = Homework_Form(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['finished']
                if  finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(

                user = request.user,
                subject = request.POST['subject'],
                title= request.POST['title'], 
                description = request.POST['description'],
                due =  request.POST['due'],
                is_finished = finished
            )  
            homework.save()
            messages.success(request,f"Home Work added successfully from {request.user.username}")    
    else:
        form = Homework_Form()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    contex ={'homework':homework,'homework_done':homework_done, 'form':form}
    return render(request,"homework.html",contex)

def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:

        homework.is_finished == False
    else:
        homework.is_finished == True
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    homework.delete()
    return redirect('homework')



def youtube(request):
    if request.method=='POST':
        form = DashboardForms(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=20)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
                                            
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'youtube.html',context)    

    else:
        form = DashboardForms()
        context={'form':form}
    return render(request,'youtube.html',context)



def todo(request):
    if  request.method == "POST":
        form = Todo_Form(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['finished']
                if  finished=='on': 
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todo.save()
            messages.success(request,f"Task added successfully by the {request.user.username }")
    else:
        form = Todo_Form()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {'todo':todo, 'form':form,'todos_done':todos_done}
    return render(request,"todo.html",context)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished == False
    else:
        todo.is_finished == True
    todo.save()
    return redirect('todo')

def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect('todo')



def books(request):
    if request.method == 'POST':
        form = DashboardForms(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        
        if r.status_code == 200:
            answer = r.json()
            result_list = []
            for item in answer.get('items', [])[:10]:
                volume_info = item.get('volumeInfo', {})
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
                result_dict = {
                    'title': volume_info.get('title', ''),
                    'subtitle': volume_info.get('subtitle', ''),
                    'description': volume_info.get('description', ''),
                    'count': volume_info.get('count', ''),
                    'categories': volume_info.get('categories', ''),
                    'rating': volume_info.get('pagerating', ''),
                    'thumbnail': thumbnail,
                    'preview': volume_info.get('previewLink', '')  # Check the correct key for the preview link
                }
                result_list.append(result_dict)
            
            context = {'form': form, 'results': result_list}
            return render(request, 'books.html', context)
        else:
            # Handle API request failure
            return HttpResponse("Failed to fetch data from Google Books API")
    else:
        form = DashboardForms()
        context = {'form': form}
        return render(request, 'books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForms(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0].get('example', '')
            synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', '')
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except (KeyError, IndexError):
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dictionary.html', context)
    else:
        form = DashboardForms()
        context = {'form': form}
        return render(request, 'dictionary.html', context)


def wiki(request):
    if request.method=='POST':
        text =request.POST['text']
        form = DashboardForms(request.POST)
        search = wikipedia.page(text)
        context ={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
            }

        return render(request,'wiki.html',context)
    else:
        form = DashboardForms()
    context = {
        'form': form
    }
    return render(request, 'wiki.html',context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if form.is_valid():
            measurement = form.cleaned_data.get('measurement')
            context = {'form': form, 'input': True}

            if measurement == 'length':
                measurement_form =conversionLengthForm()
                context['m_form'] = measurement_form

                if 'input' in request.POST:
                    first = request.POST.get('measure1')
                    second = request.POST.get('measure2')
                    input_value = request.POST.get('input')

                    if input_value and int(input_value) >= 0:
                        if first == 'yard' and second == 'foot':
                            answer = f'{input_value} yard = {int(input_value) * 3} foot'
                        elif first == 'foot' and second == 'yard':
                            answer = f'{input_value} foot = {int(input_value) / 3} yard'
                        else:
                            answer = 'Invalid conversion for length'
                    else:
                        answer = 'Invalid input value'

                    context['answer'] = answer

            elif measurement == 'mass':
                measurement_form = conversionMassForm()
                context['m_form'] = measurement_form

                if 'input' in request.POST:
                    first = request.POST.get('measure1')
                    second = request.POST.get('measure2')
                    input_value = request.POST.get('input')

                    if input_value and int(input_value) >= 0:
                        if first == 'pound' and second == 'kilogram':
                            answer = f'{input_value} pound = {float(input_value) * 0.453592} kilogram'
                        elif first == 'kilogram' and second == 'pound':
                            answer = f'{input_value} kilogram = {float(input_value) * 2.20462} pound'
                        else:
                            answer = 'Invalid conversion for mass'
                    else:
                        answer = 'Invalid input value'

                    context['answer'] = answer

            else:
                context['input'] = False  # Hide input fields if no measurement is selected

        else:
            context = {'form': form, 'input': False}  # Show form with errors
    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}

    return render(request, "conversion.html", context)



def userregistration