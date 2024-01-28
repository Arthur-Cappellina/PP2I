def fichierauto(namefichier):
    extension = namefichier.split('.')[-1]
    return (extension in {'jpg','jpeg','png'})

def test_valid():
    assert fichierauto('patate.jpg') == True

def test_valid2():
    assert fichierauto('ararar.wbep') == False

def test_valid3():
    assert fichierauto('affafa.jpeg') == True

def test_valid4():
    assert fichierauto('test.py') == False

def test_valid5():
    assert fichierauto('carotte.png') == True