from django.shortcuts import render
from .core import classify_image
import base64

# Create your views here.
def home(request):
    return render(request, 'home.html')

def results(request):
    if request.method == 'POST':
        image_data = request.FILES.get('image_data')

        if image_data:
            image_bytes = image_data.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            result = classify_image(base64_image)

            for item in result:
                class_names = list(item['class_dictionary'].keys())
                class_probabilities = item['class_probability']

                item['class_data'] = list(zip(class_names, class_probabilities))

            return render(request, 'results.html', {'result': result})
    return render(request, 'results.html')

