from my_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))
