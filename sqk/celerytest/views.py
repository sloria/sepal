from django.shortcuts import render
from tasks import add

def test_celery(request):
    result = add.delay(7, 6)
    result_sum = result.get()
    return render(request, 'celerytest/test.html', {
        'result': result, 
        'ready': result.ready(),
        'sum': result_sum,
        })



