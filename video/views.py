from django.shortcuts import render

# Create your views here.
def main_view(request):
    context = {}

    return render(request, 'video/main.html', context=context)

def zoom_view(request):
    context = {}
    return render(request, 'video/zoom.html', context=context)